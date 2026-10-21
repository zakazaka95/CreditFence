# CreditFence

**A new description or file hash should not turn the same accomplishment into new credit.**

CreditFence is a standalone GenLayer **scoped semantic-nullifier registry** for grant,
contribution and research programs. An issuer fixes what one credit means. Before a
new record can append, independent validators compare it with the complete history
of credited work in that registry, including subsequently withdrawn credits.

## The trust problem

Exact hashes catch an identical artifact. They cannot catch the same implementation
renamed, reworded or repackaged with a different hash. A generic per-claim AI decision
is insufficient too: skipping one earlier award, racing pending claims, or deleting
withdrawn work can manufacture apparent novelty. CreditFence couples semantic
comparison to a bounded, append-only history and deterministic authority rules.

## Decisions and consequences

| Decision | Meaning | State consequence |
| --- | --- | --- |
| `NOVEL` | No material reuse is identified within the pinned registry | Append one immutable credit and extend the hash chain |
| `DUPLICATE` | Same artifact or same underlying accomplishment | Final refusal to append |
| `OVERLAP` | Candidate materially reuses already credited work | Final refusal; split the old/new work into a new scoped claim |
| `INCONCLUSIVE` | Supplied descriptions do not establish distinctness | Final refusal; no credit is created |
| `UNRESOLVED` | Inference/schema/budget could not be used | Retry, at most three attempts, then final refusal |

The first entry is explicitly marked `EMPTY_REGISTER`: there is no prior work to
compare, and no semantic or factual assessment is claimed. Identical artifact hashes
use an explicit deterministic `EXACT_ARTIFACT` path. Other comparisons use GenLayer
consensus, not these shortcuts.

## Full-history consensus

Every evaluation loads **all currently credited entries**, not a subset selected by
the submitter or a stale proposal-time snapshot. Validators independently evaluate
the complete same inputs and rebuild the entire canonical receipt. Exact equality
binds registry identity, chain head, prior-entry count and hash, candidate identity,
beneficiary, work hash, artifact digest, every comparison, inspection mode, prompt
hash/coverage and append permission. There is no unvalidated narrative field.

All prior descriptions are provided in full, without prompt slicing. Both proposal-
time and evaluation-time total-budget checks fail closed. A full registry refuses
further credit; it never evicts old entries to make a duplicate appear new.

## State and authority

```text
Registry: OPEN -> CLOSED
Claim: PROPOSED -> NOVEL / DUPLICATE / OVERLAP / INCONCLUSIVE
               -> RETRYABLE -> UNRESOLVED_FINAL
Credit: appended once -> beneficiary acknowledgment / issuer withdrawal
```

Only the registry issuer can propose or assess credit, preventing strangers from
poisoning the program's history. A successful assessment and append are atomic.
The beneficiary can acknowledge the exact receipt hash once; this proves only
control of that wallet. Withdrawal changes its visible status but does **not** erase
history or restore the consumed novelty slot. Closing blocks new credit permanently.

## Reproduce

Python 3.12+; no third-party packages are needed for deterministic unit tests:

```sh
python -m unittest -v test_creditfence.py
```

`16` tests cover exact and semantic duplication, partial reuse, ambiguity, stale
pending claims, full-history coverage, maximum-sized inputs, bounded retries,
independent validator disagreement, complete receipt tampering, authority,
withdrawal laundering, acknowledgment and finality. `testsupport.py` is a clearly
labeled test double, not GenVM, a live-model benchmark, or a production audit.

See [STUDIO-TEST.md](STUDIO-TEST.md) and [DEPLOYMENT.md](DEPLOYMENT.md) for deployment
and live transaction evidence. The contract constructor takes no arguments.

## Public interface

Write: `open_registry`, `propose_credit`, `evaluate_credit`, `acknowledge_credit`,
`withdraw_credit`, `close_registry`.

Read: `get_registry`, `get_claim`, `get_entry`, `get_attempt`, `get_stats`.

All methods are nonpayable; send **0 GEN** as value. Transaction fees are separate.

## Honest scope and limitations

This is **not proof of performance, authorship, identity, safety or legal entitlement**.
It compares issuer-supplied descriptions and artifact fingerprints. A novel fabricated
description can still be novel. Issuers must verify factual work and authenticity
outside this primitive, before credit admission; consumers must pin the intended
contract, registry, issuer and credit unit. This is not global Sybil resistance or
cross-registry deduplication. Creating a different registry is outside the pinned scope.

At most 16 entries and 1,500 characters per description keep full-history inspection
bounded and auditable. Different validators can disagree on ambiguous semantic
overlap; this can reject a transaction rather than invent agreement. All input and
accepted state are public. Do not submit confidential or personal information.
