import copy
import typing as t

import interpreter
import parse


class CycleError(Exception):
    """Error thrown when recursion causes an overflow due to an infinite cycle"""


class ContradictionError(Exception):
    """Error thrown when a hypothesis is both TRUE and FALSE."""


class InferenceEngine:
    """Inference engine using backward chaining to infer
    if a hypothesis is true, starting from the hypothesis
    to check if data confirms the rule."""

    def __init__(self):
        self.facts: t.Dict[str, bool] = {}
        self.rules: t.Dict[str, interpreter.Rule] = {}

    def add_fact(self, fact: interpreter.Fact) -> None:
        self.facts[fact.name] = True

    def add_rule(self, rule: interpreter.Rule) -> None:
        """Add a rule to the map, pipe it into the graph with an OR if a rule already exists."""

        if rule.target not in self.rules:
            self.rules[rule.target] = rule
        else:
            self.rules[rule.target] |= rule

    def _ast(self, s: str) -> t.Optional[parse.AST]:
        """Returns the corresponding ast or None if no rule is found."""
        rule = self.rules.get(s)
        return rule.ast if rule else None

    def infer_hypothesis(self, h: str) -> bool:
        """Infer the result of the hypothesis."""
        return self._infer(h, set())

    def infer(self, ast: t.Optional[parse.AST], seen) -> bool:
        """Operator dispatcher."""
        if not ast:
            return False
        if ast.name == "+":
            return self.infer(ast.operands[0], copy.copy(seen)) and self.infer(
                ast.operands[1], seen
            )
        if ast.name == "|":
            try:
                loperand = self.infer(ast.operands[0], copy.copy(seen))
            except CycleError:
                loperand = False
            return loperand or self.infer(ast.operands[1], seen)
        if ast.name == "!":
            return not self.infer(ast.operands[0], seen)
        return self._infer(ast.name, seen)

    def _infer(self, hypothesis: str, seen: t.Set[str]) -> bool:
        """Internal implementation of the inference."""
        nhypothesis = (
            "!" + hypothesis if not hypothesis.startswith("!") else hypothesis[1:]
        )
        exists = self.facts.get(hypothesis, False)
        nexists = self.facts.get(nhypothesis, False)
        if hypothesis in seen:
            raise CycleError("Cycle detected.")
        seen.add(hypothesis)
        exists = exists or self.infer(self._ast(hypothesis), copy.copy(seen))
        try:
            nexists = nexists or self.infer(self._ast(nhypothesis), seen)
        except CycleError as e:
            if exists:
                return exists
            raise CycleError(*e.args)
        if exists and nexists:
            raise ContradictionError(
                "Cannot infer hypothesis, {} and {} are both True.".format(
                    hypothesis, nhypothesis
                )
            )
        return exists