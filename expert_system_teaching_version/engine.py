from dataclasses import dataclass
from typing import Any


@dataclass
class Rule:
    antecedents: list[str]
    consequent: str
    priority: int = 0
    name: str = ""


class ForwardChainingEngine:
    def __init__(self, rules: list[Rule]):
        self.rules = rules
        self.facts: set[str] = set()
        self.trace: list[dict[str, Any]] = []

    def assert_facts(self, initial: list[str]) -> None:
        """Store initial facts in working memory."""
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        """Check if a rule can fire."""
        return (
            all(fact in self.facts for fact in rule.antecedents)
            and rule.consequent not in self.facts
        )

    def run(self) -> None:
        """Run forward chaining."""
        while True:
            fired = False

            for rule in self.rules:
                if self.can_fire(rule):
                    self.facts.add(rule.consequent)

                    self.trace.append(
                        {"rule": rule.name, "conclusion": rule.consequent}
                    )

                    fired = True
                    break

            if not fired:
                break

    def conclusions(self) -> dict[str, list[str]]:
        """Separate conclusions into categories."""
        results = {"recommendations": [], "specs": [], "other_facts": []}

        for fact in self.facts:
            if fact.startswith("recommend:"):
                results["recommendations"].append(fact)
            elif fact.startswith("spec:"):
                results["specs"].append(fact)
            else:
                results["other_facts"].append(fact)

        return results
