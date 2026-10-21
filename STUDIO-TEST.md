# CreditFence reviewer walkthrough

Import the exact tracked CreditFence.py into Studio or use the deployment in
DEPLOYMENT.md. Select **Normal (Full Consensus)**. Constructor: no arguments.
Every write has transaction value 0 GEN; normal network fees still apply.

1. As issuer wallet A, call `open_registry`:
   - title: `Open tools credit ledger`
   - scope: `Credit improvements to our public open-source research tools.`
   - credit_unit: `One credit per distinct implemented feature; renaming, reformatting and partial reuse are not new work.`
2. Read the returned registry ID. All IDs are zero-based; do not assume 0 on a
   shared deployment.
3. Call `propose_credit(registry_id, B, work, artifact_sha256)` with:
   - work: `Implemented an offline CSV export for the public weather dataset, including tests and a usage guide.`
   - artifact_sha256: 64 lowercase `a` characters (a labeled synthetic demo fingerprint).
4. Call `evaluate_credit(claim_id)`. With an empty register, expect `NOVEL` and
   `inspection.mode = EMPTY_REGISTER`. This first entry is not claimed as an AI verdict.
5. Propose a second candidate with a different fingerprint, 64 lowercase `b` characters:
   `Shipped weather data CSV downloads for offline users, complete with a test suite and documentation.`
6. Evaluate that claim through full consensus. The same accomplishment is described;
   expect `DUPLICATE` (or a conservative refusal if the models disagree/abstain),
   `append_allowed = false`, and the original credit count unchanged.
7. Propose a separate feature with fingerprint 64 lowercase `c` characters:
   `Added a keyboard-accessible dark mode settings panel to the documentation website with accessibility tests.`
8. Evaluate. Expect `NOVEL` when validators agree the feature is distinct. Inspect
   the complete per-entry comparisons, `base_chain_hash`, new entry ID and chain head.
9. As B, call `acknowledge_credit(entry_id, receipt_hash)` using the exact hash from
   `get_entry`. Repeating it, or using another wallet, must fail.
10. As A, `withdraw_credit` the first entry, then propose its artifact again. Expect
    deterministic `DUPLICATE`, not a new credit. Withdrawal never erases prior use.

## Integration check

A consuming program must pin this specific issuer and registry. Never accept an
arbitrary fresh registry as evidence that a contribution was not already credited.
The demonstration fingerprints are synthetic; the contract does not download or
authenticate artifacts and does not assert that this demo work exists in the world.
