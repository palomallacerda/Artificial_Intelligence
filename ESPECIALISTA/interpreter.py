from __future__ import annotations
import typing as t

import parse


class TargetNand(Exception):
    """Exception raised if the user tries to infer a NAND."""


class TargetOrXor(Exception):
    """Exception raised if the user tries to infer a (X)OR."""


class Fact:
    """Representation of a fact, will be set to TRUE."""

    def __init__(self, ast: parse.AST) -> None:
        self.name = ast.name


class Hypothesis:
    """Representation of a hypothesis, will be the target we want to infer."""

    def __init__(self, ast: parse.AST) -> None:
        self.name = ast.name


class Rule:
    """Representation of a rule, will contain a function to infer it."""

    def __init__(self, target: str, ast: parse.AST) -> None:
        self.target = target
        self.ast = ast

    @staticmethod
    def _ast_to_func(
        ast: parse.AST
    ) -> t.Callable[[t.Dict[str, bool], t.Dict[str, Rule]], bool]:
        """Return a function that will check for facts and rules
        if a hypothesis is true."""
        if ast.name == "+":
            return lambda facts, rules: Rule._ast_to_func(ast.operands[0])(
                facts, rules
            ) and Rule._ast_to_func(ast.operands[1])(facts, rules)
        if ast.name == "|":
            return lambda facts, rules: Rule._ast_to_func(ast.operands[0])(
                facts, rules
            ) or Rule._ast_to_func(ast.operands[1])(facts, rules)
        if ast.name == "!":
            return lambda facts, rules: not Rule._ast_to_func(*ast.operands)(
                facts, rules
            )
        return lambda facts, rules: facts.get(ast.name) or rules.get(
            ast.name, lambda *_: False
        )(facts, rules)

    def __call__(self, facts: t.Dict[str, bool], rules: t.Dict[str, Rule]) -> bool:
        """Call the function returned by _ast_to_func."""
        return Rule._ast_to_func(self.ast)(facts, rules)

    def __or__(self, other: Rule) -> Rule:
        """Union of two rules, will be merged with an OR."""
        if self.target != other.target:
            raise NameError("Two rules' targets must be the same to be combined.")
        return Rule(self.target, parse.AST("|", [self.ast, other.ast]))


def coercenot(xs: t.List[parse.AST]) -> t.List[parse.AST]:
    """Reduce the amount of NOT in the AST by negating them together."""

    def _coercenot(ast: parse.AST, neg: t.Optional[bool] = False) -> parse.AST:
        if ast.name == "!":
            return _coercenot(ast.operands[0], not neg)
        return parse.AST(("!" if neg else "") + ast.name, [])

    return [
        parse.AST("=>", [stmt.operands[0], _coercenot(stmt.operands[1])]) for stmt in xs
    ]


def sanitizenand(xs: t.List[parse.AST]) -> t.List[parse.AST]:
    """Throw an exception if the rule has a NAND gate as a target."""
    for ast in xs:
        if "+" in ast.operands[1]:
            raise TargetNand(
                "Ambiguous rule, cannot have a NAND gate as a rule target."
            )
    return xs


def simplifyand(lhs: parse.AST, rhs: parse.AST) -> t.List[parse.AST]:
    """Throw an exception if the rule has an OR gate as a target.
    Convert each operand of AND into a separate rule."""
    if rhs.name == "|":
        raise TargetOrXor("Ambiguous rule, cannot have a (X)OR gate as a rule target.")
    if rhs.name == "+":
        return simplifyand(lhs, rhs.operands[0]) + simplifyand(lhs, rhs.operands[1])
    return [parse.AST("=>", [lhs, rhs])]


Statement = t.Union[Fact, Hypothesis, Rule]


def run(ast: parse.AST) -> t.List[Statement]:
    if ast.name == "?":
        return [*map(Hypothesis, ast.operands)]
    if ast.name == "=":
        return [*map(Fact, ast.operands)]
    return [
        Rule(stmt.operands[1].name, stmt.operands[0])
        for stmt in coercenot(sanitizenand(simplifyand(*ast.operands)))
    ]