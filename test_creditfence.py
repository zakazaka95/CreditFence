import unittest
from testsupport import load, UserError

A = "0x" + "1" * 40
B = "0x" + "2" * 40
C = "0x" + "3" * 40
FIRST = "Implemented an offline CSV export for the public weather dataset, including tests and a usage guide."
SECOND = "Added a keyboard-accessible dark mode settings panel to the documentation website with accessibility tests."


class CreditTests(unittest.TestCase):
    def setUp(self):
        self.m, self.c, self.r = load("CreditFence.py")
        self.key = self.c.open_registry("Open tools credit ledger", "Credit improvements to our public open-source research tools.",
                                       "One credit per distinct implemented feature; renaming, reformatting and partial reuse are not new work.")

    def propose(self, text=FIRST, digest="a" * 64, beneficiary=B):
        return self.c.propose_credit(0, beneficiary, text, digest)

    def seed(self):
        key = self.propose()
        receipt = self.c.evaluate_credit(key)
        return key, receipt

    def distinct(self):
        self.r.output = {"relations": [{"entry_id": 0, "relation": "DISTINCT"}]}
        key = self.propose(SECOND, "b" * 64)
        receipt = self.c.evaluate_credit(key)
        return key, receipt

    def test_first_entry_is_explicitly_not_a_semantic_or_factual_assessment(self):
        _, receipt = self.seed()
        self.assertEqual(receipt["inspection"]["mode"], "EMPTY_REGISTER")
        self.assertFalse(receipt["inspection"]["semantic_complete"])
        self.assertEqual(self.r.calls, 0)
        self.assertEqual(self.c.get_registry(0)["entry_ids"], [0])

    def test_distinct_work_is_consensus_appended(self):
        self.seed()
        _, receipt = self.distinct()
        self.assertEqual(receipt["decision"], "NOVEL")
        self.assertTrue(receipt["inspection"]["semantic_complete"])
        self.assertEqual(self.c.get_registry(0)["entry_ids"], [0, 1])
        self.assertEqual(self.c.get_stats()["credits"], 2)

    def test_identical_artifact_is_deterministic_duplicate_even_new_beneficiary(self):
        self.seed()
        receipt = self.c.evaluate_credit(self.propose(SECOND, "a" * 64, C))
        self.assertEqual(receipt["decision"], "DUPLICATE")
        self.assertEqual(receipt["inspection"]["mode"], "EXACT_ARTIFACT")
        self.assertFalse(receipt["append_allowed"])
        self.assertEqual(self.r.calls, 0)

    def test_paraphrase_new_hash_does_not_bypass_semantic_nullifier(self):
        self.seed()
        self.r.output = {"relations": [{"entry_id": 0, "relation": "SAME_WORK"}]}
        key = self.propose("Shipped weather data CSV downloads for offline users, complete with a test suite and documentation.", "b" * 64, C)
        self.assertEqual(self.c.evaluate_credit(key)["decision"], "DUPLICATE")
        self.assertEqual(self.c.get_registry(0)["entry_ids"], [0])

    def test_partial_reuse_and_uncertainty_cannot_append(self):
        self.seed()
        for relation, decision in [("OVERLAPPING_WORK", "OVERLAP"), ("UNCERTAIN", "INCONCLUSIVE")]:
            self.r.output = {"relations": [{"entry_id": 0, "relation": relation}]}
            receipt = self.c.evaluate_credit(self.propose(SECOND, "b" * 64))
            self.assertEqual(receipt["decision"], decision)
            self.assertFalse(receipt["append_allowed"])

    def test_pending_claim_reads_all_credits_added_after_proposal(self):
        self.seed()
        pending = self.propose(SECOND, "c" * 64)
        self.distinct()
        self.r.output = {"relations": [{"entry_id": 0, "relation": "DISTINCT"},
                                       {"entry_id": 1, "relation": "SAME_WORK"}]}
        receipt = self.c.evaluate_credit(pending)
        self.assertEqual(receipt["base_entry_count"], 2)
        self.assertEqual(receipt["decision"], "DUPLICATE")
        self.assertIn(SECOND, self.r.prompts[-1])

    def test_withdrawal_never_restores_consumed_novelty(self):
        self.seed()
        self.c.withdraw_credit(0)
        receipt = self.c.evaluate_credit(self.propose(SECOND, "a" * 64))
        self.assertEqual(receipt["decision"], "DUPLICATE")
        self.assertTrue(self.c.get_entry(0)["withdrawn"])
        self.assertEqual(self.c.get_registry(0)["entry_ids"], [0])

    def test_issuer_authority_prevents_third_party_ledger_poisoning(self):
        key = self.propose()
        self.r.as_sender(C)
        for operation in [lambda: self.propose(), lambda: self.c.evaluate_credit(key), lambda: self.c.close_registry(0)]:
            with self.assertRaises(UserError):
                operation()
        self.assertEqual(self.c.get_stats()["credits"], 0)

    def test_recipient_acknowledges_exact_receipt_only_once(self):
        _, receipt = self.seed()
        receipt_hash = self.c.get_entry(0)["receipt_hash"]
        with self.assertRaises(UserError):
            self.c.acknowledge_credit(0, receipt_hash)
        self.r.as_sender(B)
        with self.assertRaises(UserError):
            self.c.acknowledge_credit(0, "wrong")
        self.c.acknowledge_credit(0, receipt_hash)
        with self.assertRaises(UserError):
            self.c.acknowledge_credit(0, receipt_hash)

    def test_model_failure_has_bounded_attempt_history(self):
        self.seed()
        key = self.propose(SECOND, "b" * 64)
        self.r.output = RuntimeError("model unavailable")
        for attempt in range(1, 4):
            receipt = self.c.evaluate_credit(key)
            self.assertFalse(receipt["append_allowed"])
            self.assertEqual(self.c.get_attempt(key, attempt), receipt)
        self.assertEqual(self.c.get_claim(key)["status"], "UNRESOLVED_FINAL")
        with self.assertRaises(UserError):
            self.c.evaluate_credit(key)

    def test_validator_disagreement_rejects_without_append(self):
        self.seed()
        self.r.output = {"relations": [{"entry_id": 0, "relation": "DISTINCT"}]}
        self.r.validator_output = {"relations": [{"entry_id": 0, "relation": "SAME_WORK"}]}
        key = self.propose(SECOND, "b" * 64)
        with self.assertRaises(AssertionError):
            self.c.evaluate_credit(key)
        self.assertEqual(self.c.get_registry(0)["entry_ids"], [0])

    def test_every_consequential_receipt_field_is_bound(self):
        self.seed()
        self.r.output = {"relations": [{"entry_id": 0, "relation": "DISTINCT"}]}
        key = self.propose(SECOND, "b" * 64)
        changes = {"schema": "bad", "registry_id": 99, "claim_id": 99, "registry_hash": "bad",
                   "base_chain_hash": "bad", "base_entry_count": 99, "previous_entries_hash": "bad",
                   "claim_hash": "bad", "beneficiary": C, "work_hash": "bad", "artifact_sha256": "bad",
                   "matching_artifact_entries": [0], "relations": [], "decision": "DUPLICATE", "append_allowed": False}
        for field, value in changes.items():
            with self.subTest(field=field):
                self.r.mutate = lambda receipt, f=field, v=value: dict(receipt, **{f: v})
                with self.assertRaises(AssertionError):
                    self.c.evaluate_credit(key)
        for field in ["mode", "semantic_complete", "prompt_chars", "prompt_sha256", "prompt_truncated"]:
            with self.subTest(inspection=field):
                def mutate(receipt, f=field):
                    receipt["inspection"][f] = "tampered"
                    return receipt
                self.r.mutate = mutate
                with self.assertRaises(AssertionError):
                    self.c.evaluate_credit(key)

    def test_maximum_history_keeps_all_input_and_tail(self):
        tail = "FINAL TEXT MUST NOT BE SILENTLY DROPPED."
        for index in range(16):
            self.r.output = {"relations": [{"entry_id": i, "relation": "DISTINCT"} for i in range(index)]}
            description = str(index) + "x" * (1500 - len(str(index)) - len(tail)) + tail
            key = self.propose(description, format(index + 1, "064x"))
            receipt = self.c.evaluate_credit(key)
            self.assertTrue(receipt["append_allowed"])
            self.assertFalse(receipt["inspection"]["prompt_truncated"])
        self.assertEqual(self.r.prompts[-1].count(tail), 16)
        with self.assertRaisesRegex(UserError, "capacity"):
            self.propose(SECOND, "f" * 64)

    def test_prompt_budget_failure_cannot_append(self):
        self.seed()
        key = self.propose(SECOND, "b" * 64)
        self.m.MAX_PROMPT_CHARS = 1
        receipt = self.c.evaluate_credit(key)
        self.assertTrue(receipt["inspection"]["prompt_truncated"])
        self.assertFalse(receipt["append_allowed"])
        self.assertEqual(self.r.calls, 0)

    def test_duplicate_missing_boolean_and_out_of_order_comparisons_fail_closed(self):
        self.seed()
        for raw in [{"relations": []}, {"relations": [{"entry_id": False, "relation": "DISTINCT"}]},
                    {"relations": [{"entry_id": 99, "relation": "DISTINCT"}]}]:
            self.r.output = raw
            receipt = self.c.evaluate_credit(self.propose(SECOND, "b" * 64))
            self.assertFalse(receipt["append_allowed"])

    def test_final_claim_and_closed_registry_cannot_reopen(self):
        first, _ = self.seed()
        with self.assertRaises(UserError):
            self.c.evaluate_credit(first)
        self.c.close_registry(0)
        with self.assertRaises(UserError):
            self.propose(SECOND, "b" * 64)


if __name__ == "__main__":
    unittest.main()
