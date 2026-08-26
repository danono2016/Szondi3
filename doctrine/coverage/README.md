# P2A coverage ledgers

Coverage records are append-only batch witnesses. Early `SZ_SA_1948` batches are stored as JSONL records in `SZ_SA_1948.jsonl`; later batches may use source-and-batch-specific JSONL files (for example `SZ_SA_1948_BATCH_005.jsonl`) to keep review diffs atomic. File layout does not change authority: each JSON object must identify its `batchId`, admitted `sourceId`, canonical range, evidence witness, doctrine IDs, intentional no-entry units, visual-arbitration units, unresolved ambiguities, and review notes.

Coverage ledgers are accountability witnesses. They do not establish doctrinal truth and do not authorize P2B execution.
