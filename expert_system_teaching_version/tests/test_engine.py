import unittest
from engine import Rule, ForwardChainingEngine
from kb_loader import load_rules


class TestExpertSystem(unittest.TestCase):
    def test_can_fire(self):
        rule = Rule(["gaming", "budget_high"], "recommend:gaming")
        engine = ForwardChainingEngine([rule])
        engine.assert_facts(["gaming", "budget_high"])

        self.assertTrue(engine.can_fire(rule))

    def test_missing_fact(self):
        rule = Rule(["gaming", "budget_high"], "recommend:gaming")
        engine = ForwardChainingEngine([rule])
        engine.assert_facts(["gaming"])

        self.assertFalse(engine.can_fire(rule))

    def test_already_known(self):
        rule = Rule(["gaming"], "recommend:gaming")
        engine = ForwardChainingEngine([rule])
        engine.assert_facts(["gaming", "recommend:gaming"])

        self.assertFalse(engine.can_fire(rule))

    def test_forward_chaining(self):
        rules = [
            Rule(["needs_gpu"], "spec:dedicated_gpu"),
            Rule(["gaming"], "needs_gpu"),
        ]

        engine = ForwardChainingEngine(rules)
        engine.assert_facts(["gaming"])
        engine.run()

        self.assertIn("needs_gpu", engine.facts)
        self.assertIn("spec:dedicated_gpu", engine.facts)

    def test_conclusions(self):
        engine = ForwardChainingEngine([])
        engine.assert_facts(
            ["budget_high", "recommend:premium_ultrabook", "spec:ram_16_plus"]
        )

        results = engine.conclusions()

        self.assertIn("recommend:premium_ultrabook", results["recommendations"])
        self.assertIn("spec:ram_16_plus", results["specs"])
        self.assertIn("budget_high", results["other_facts"])

    def test_laptop_rules(self):
        rules = load_rules("kb/laptop_rules.json")
        engine = ForwardChainingEngine(rules)

        engine.assert_facts(["budget_high", "portable", "long_battery"])

        engine.run()

        self.assertIn("recommend:premium_ultrabook", engine.facts)


if __name__ == "__main__":
    unittest.main()
