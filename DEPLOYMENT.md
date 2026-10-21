# Studio Next deployment

- Contract: [0x359A5B7ad784d4B02B61Dd3d73eF877D0eA4d920](https://explorer-studio-next.genlayer.com/address/0x359A5B7ad784d4B02B61Dd3d73eF877D0eA4d920)
- Deployment: [0x0f365322…](https://explorer-studio-next.genlayer.com/tx/0x0f365322e74ec024fd9450eeed1eedbc3e324f553a3d1f54234000b2bff89c6f)
- Deployment outcome observed on October 21, 2026: FINALIZED, GenVM SUCCESS.
- Execution mode: Normal (Full Consensus), not leader-only.
- Contract version: 1.0.0; receipt schema: creditfence-v1.
- RPC: https://studio-next.genlayer.com/api
- Chain ID: 61997.

The full code rendered in Explorer's Contract -> Code tab was compared by SHA-256
against this repository's CreditFence.py, after CRLF-to-LF normalization and trimming
surrounding whitespace. Both hashes match:

```text
7f90f31bf621077f5487d2d343d06eb268a83b99ce862a06deed720895b432be
```

The constructor and write methods do not hold or distribute funds. Any demonstration
work descriptions and artifact fingerprints are synthetic test fixtures, not proof
that a feature exists or that a person is entitled to rewards.

## Observed live consensus demo

Registry 0 uses explicitly synthetic descriptions and fingerprints. Claim 0 seeded
entry 0 through `EMPTY_REGISTER`; this is deliberately not a semantic assessment.

- Claim 1 paraphrased the seeded CSV-export feature but supplied a different
  artifact fingerprint. Independent semantic evaluation returned `DUPLICATE`,
  relation `SAME_WORK`, `append_allowed=false`, and no new entry.
  [Finalized evaluation](https://explorer-studio-next.genlayer.com/tx/0x828d211b90f70f082a24ad3150f2cc9a5212a6a2339e3cccd232fb949aeb4823).
- Claim 2 described an unrelated keyboard-accessible dark-mode settings panel.
  Independent semantic evaluation returned `NOVEL`, relation `DISTINCT`, and
  appended entry 1. The persisted receipt records `semantic_complete=true` and
  `prompt_truncated=false`.
  [Finalized evaluation](https://explorer-studio-next.genlayer.com/tx/0x4471dcc575434685469dde23114fa101298f04c7179789fe8b16bc5087e9599b).

These are two observed network examples, not a reliability benchmark. The 16
local unit tests use deterministic test doubles, not live model calls.
