#!/usr/bin/env python3
"""Independent P0 verifier for generated canonical-access artifacts.

The verifier does not reuse extractor traversal helpers. It rereads admitted DOCX
OOXML directly and checks schema/provenance/order plus structural witness counts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"

def qn(ns, local): return f"{{{ns}}}{local}"

def split_tag(tag):
    if tag.startswith("{") and "}" in tag:
        return tuple(tag[1:].split("}",1))
    return "", tag

class VerifyError(RuntimeError): pass

def require(ok, msg):
    if not ok: raise VerifyError(msg)

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def load_jsonl(path):
    out=[]
    with path.open(encoding='utf-8') as f:
        for n,line in enumerate(f,1):
            require(line.endswith('\n'), f"{path.name}:{n} lacks LF terminator")
            out.append(json.loads(line))
    return out

def walk_json(obj):
    yield obj
    if isinstance(obj,dict):
        for v in obj.values(): yield from walk_json(v)
    elif isinstance(obj,list):
        for v in obj: yield from walk_json(v)

def canonical_feature_counts(records):
    c=Counter()
    for node in walk_json(records):
        if not isinstance(node,dict): continue
        if 'fieldEvents' in node and isinstance(node['fieldEvents'],list):
            for ev in node['fieldEvents']: c[f"fldChar:{ev.get('event','').lower()}"] += 1
        if 'hyperlinks' in node and isinstance(node['hyperlinks'],list): c['hyperlink'] += len(node['hyperlinks'])
        if 'bookmarks' in node and isinstance(node['bookmarks'],list): c['bookmarkStart'] += len(node['bookmarks'])
        if 'references' in node and isinstance(node['references'],list):
            for ref in node['references']: c[ref.get('kind','reference')] += 1
        if 'visuals' in node and isinstance(node['visuals'],list):
            for visual in node['visuals']:
                kind=visual.get('kind')
                if kind in {'DRAWING','LEGACY_PICTURE','EMBEDDED_OBJECT'}: c[kind] += 1
        if node.get('kind') == 'TAB': c['tab'] += 1
        if node.get('kind') == 'BREAK': c['break'] += 1
        if node.get('kind') == 'CARRIAGE_RETURN': c['carriageReturn'] += 1
    return c

def direct_feature_counts(zf, emitted_parts):
    c=Counter()
    fld_map={'begin':'fldChar:begin','separate':'fldChar:separate','end':'fldChar:end'}
    for part in emitted_parts:
        root=ET.fromstring(zf.read(part))
        parent={child:par for par in root.iter() for child in par}
        for el in root.iter():
            ns,local=split_tag(el.tag)
            if ns != W: continue
            if local == 'fldChar':
                typ=el.attrib.get(qn(W,'fldCharType'))
                if typ in fld_map: c[fld_map[typ]] += 1
            elif local == 'tab':
                # w:tab is overloaded: under w:r it is a visible tab character;
                # under w:tabs it defines a paragraph tab stop (structural formatting).
                par=parent.get(el)
                if par is not None and par.tag == qn(W,'r'): c['tab'] += 1
            elif local in {'hyperlink','bookmarkStart','footnoteReference','endnoteReference','commentReference','br','cr','drawing','pict','object'}:
                key={
                    'br':'break','cr':'carriageReturn','drawing':'DRAWING','pict':'LEGACY_PICTURE','object':'EMBEDDED_OBJECT'
                }.get(local,local)
                c[key]+=1
    return c

def body_signature(zf):
    root=ET.fromstring(zf.read('word/document.xml'))
    body=root.find(qn(W,'body'))
    require(body is not None,'Missing w:body')
    sig=[]; tables=[]; simple=[]
    for ch in body:
        ns,local=split_tag(ch.tag)
        if ns==W and local=='sectPr': continue
        if ns==W and local=='p':
            sig.append('PARAGRAPH')
            forbidden={'fldChar','instrText','hyperlink','drawing','pict','object','txbxContent','tab','br','cr','footnoteReference','endnoteReference','commentReference'}
            locals_={split_tag(e.tag)[1] for e in ch.iter()}
            if not (locals_ & forbidden):
                simple.append((len(sig)-1,''.join((e.text or '') for e in ch.iter() if e.tag==qn(W,'t'))))
        elif ns==W and local=='tbl':
            sig.append('TABLE')
            rows=[]
            for tr in ch:
                if tr.tag != qn(W,'tr'): continue
                rows.append(sum(1 for tc in tr if tc.tag==qn(W,'tc')))
            tables.append((len(sig)-1,rows))
        elif ns==MC and local=='AlternateContent': sig.append('ALTERNATE_CONTENT')
        else: raise VerifyError(f"Unsupported direct body block during verification: {ch.tag}")
    return sig,tables,simple

def verify_source(repo,out,source,manifest_files):
    sid=source['sourceId']; jsonl=out/f'{sid}.jsonl'; invp=out/f'{sid}.inventory.json'
    require(jsonl.is_file() and invp.is_file(),f'{sid}: missing outputs')
    require(set(manifest_files)=={jsonl.name,invp.name},f'{sid}: manifest file set mismatch')
    require(sha256(jsonl)==manifest_files[jsonl.name],f'{sid}: JSONL hash mismatch')
    require(sha256(invp)==manifest_files[invp.name],f'{sid}: inventory hash mismatch')
    records=load_jsonl(jsonl); inv=json.loads(invp.read_text(encoding='utf-8'))
    expected_sha=source['docxSha256'].lower(); src=repo/source['docxPath']
    require(sha256(src)==expected_sha,f'{sid}: source SHA mismatch')
    required={'canonicalSchemaVersion','extractorVersion','sourceId','layer','inputSourceFilename','inputSourceSha256','stream','unitId','kind','path'}
    per_stream=Counter()
    for i,r in enumerate(records,1):
        require(required <= set(r),f'{sid}: record {i} missing required keys {sorted(required-set(r))}')
        require(r['canonicalSchemaVersion']==1,f'{sid}: record {i} schema')
        require(r['sourceId']==sid and r['layer']==source['layer'],f'{sid}: record {i} provenance identity')
        require(r['inputSourceFilename']==source['docxPath'] and r['inputSourceSha256']==expected_sha,f'{sid}: record {i} input provenance')
        per_stream[r['stream']]+=1
        require(r['unitId']==f"U{per_stream[r['stream']]:06d}",f"{sid}: nonmonotonic unit {r['stream']}:{r['unitId']}")
    require(inv['sourceId']==sid and inv['inputSourceSha256']==expected_sha,f'{sid}: inventory provenance')
    require(dict(sorted(per_stream.items()))==inv['recordCountsByStream'],f'{sid}: inventory stream counts')
    with zipfile.ZipFile(src) as zf:
        names=sorted(zf.namelist()); word_xml=sorted(n for n in names if n.startswith('word/') and n.endswith('.xml'))
        inv_parts=inv['parts']; require([p['part'] for p in inv_parts]==word_xml,f'{sid}: part inventory mismatch')
        require(all(p['classification']!='UNSUPPORTED_POSSIBLY_MEANINGFUL' for p in inv_parts),f'{sid}: unsupported part in accepted inventory')
        emitted=[p['part'] for p in inv_parts if p.get('stream')]
        direct=direct_feature_counts(zf,emitted); canon=canonical_feature_counts(records)
        keys={'fldChar:begin','fldChar:separate','fldChar:end','hyperlink','bookmarkStart','footnoteReference','endnoteReference','commentReference','tab','break','carriageReturn','DRAWING','LEGACY_PICTURE','EMBEDDED_OBJECT'}
        for key in sorted(keys): require(canon[key]==direct[key],f'{sid}: feature count mismatch {key}: canonical={canon[key]} source={direct[key]}')
        sig,tables,simple=body_signature(zf); body=[r for r in records if r['stream']=='BODY']
        require([r['kind'] for r in body]==sig,f'{sid}: body block order/kinds mismatch')
        for pos,row_counts in tables:
            rec=body[pos]; require(len(rec['rows'])==len(row_counts),f'{sid}: table {pos} row count')
            require([len(r['cells']) for r in rec['rows']]==row_counts,f'{sid}: table {pos} cell counts')
        spots=(simple[:5]+simple[-5:]) if len(simple)>5 else simple
        for pos,text in spots: require(body[pos].get('text','')==text,f'{sid}: simple paragraph text mismatch at body index {pos}')
        for stream,pat in [('HEADER',re.compile(r'^word/header\d+\.xml$')),('FOOTER',re.compile(r'^word/footer\d+\.xml$'))]:
            source_parts=[n for n in word_xml if pat.match(n)]
            story=[r['storyPart'] for r in records if r['stream']==stream]
            require(story==source_parts,f'{sid}: {stream} story-part identity/order mismatch')
    return {'records':len(records),'streams':dict(sorted(per_stream.items())),'featureCounts':dict(sorted(canonical_feature_counts(records).items()))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo',default='.'); ap.add_argument('--output-dir',required=True); args=ap.parse_args()
    repo=Path(args.repo).resolve(); out=Path(args.output_dir); out=out if out.is_absolute() else repo/out
    catalog=json.loads((repo/'config/source_catalog.json').read_text(encoding='utf-8'))
    manifest=json.loads((out/'canonical-hashes.json').read_text(encoding='utf-8'))
    require(manifest.get('canonicalSchemaVersion')==1,'manifest schema')
    require(len(manifest.get('sources',{}))==len(catalog['sources'])==10,'expected exactly 10 sources')
    summary={}
    for source in catalog['sources']:
        sid=source['sourceId']; require(sid in manifest['sources'],f'{sid}: absent from manifest')
        summary[sid]=verify_source(repo,out,source,manifest['sources'][sid])
    print(json.dumps({'verification':'PASS','sources':summary},ensure_ascii=False,sort_keys=True,indent=2))
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (VerifyError,OSError,zipfile.BadZipFile,json.JSONDecodeError,ET.ParseError) as exc:
        print(f'CANONICAL VERIFICATION FAIL: {exc}',file=sys.stderr); raise SystemExit(1)
