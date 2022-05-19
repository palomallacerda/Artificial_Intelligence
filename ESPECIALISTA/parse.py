from __future__ import annotations
import sys
import typing as t


class AST:

    def __init__(self, name: str, operands: t.Optional[t.List[AST]] = None) -> None:
        self.name = name
        self.operands = operands or []

    def __contains__(self, name: str) -> bool:
        if self.name == name:
            return True
        for ast in self.operands:
            if name in ast:
                return True
        return False

    def __str__(self) -> str:
        if self.name in ("=", "?"):
            return "{} {}".format(self.name, self.operands)
        if self.name in ("=>", "<=>"):
            return "{1} {0} {2}".format(self.name, *self.operands)
        return ["{}", "({} {})", "({1} {0} {2})"][len(self.operands)].format(
            self.name, *self.operands
        )

    def __repr__(self):
        return str(self)


class RecursionHelper:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.old = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, *_):
        sys.setrecursionlimit(self.old)


def atom(stream: t.List[str]) -> t.Tuple[int, AST]:
    if stream[0].isalpha():
        return 1, AST(stream[0])
    if stream[0] == "(":
        n, ast = expr(stream[1:])
        if stream[n + 1] == ")":
            return n + 2, ast
        raise SyntaxError("Expected ')'")
    raise SyntaxError("Unexpected token '{}'".format(stream[0]))


def notop(stream: t.List[str]) -> t.Tuple[int, AST]:
    if stream[0] == "!":
        n, ast = notop(stream[1:])
        if not n:
            raise SyntaxError("Unexpected EOF.")
        return n + 1, AST("!", [ast])
    return atom(stream)


def andop(
    stream: t.List[str], n: t.Optional[int] = None, last: t.Optional[AST] = None
) -> t.Tuple[int, AST]:
    if n is None:
        n, last = notop(stream)
    if n == len(stream) or stream[n] != "+":
        return n, last
    m, rast = notop(stream[n + 1 :])
    return andop(stream, n + m + 1, AST("+", [last, rast]))


def orop(
    stream: t.List[str], n: t.Optional[int] = None, last: t.Optional[AST] = None
) -> t.Tuple[int, AST]:
    if n is None:
        n, last = andop(stream)
    if n == len(stream) or stream[n] != "|":
        return n, last
    m, rast = andop(stream[n + 1 :])
    return orop(stream, n + m + 1, AST("|", [last, rast]))


def xorop(
    stream: t.List[str], n: t.Optional[int] = None, last: t.Optional[AST] = None
) -> t.Tuple[int, AST]:
    if n is None:
        n, last = orop(stream)
    if n == len(stream) or stream[n] != "^":
        return n, last
    m, rast = orop(stream[n + 1 :])
    # x ^ y <=> (x + !y) | (!x + y)
    return xorop(
        stream,
        n + m + 1,
        AST(
            "|",
            [AST("+", [last, AST("!", [rast])]), AST("+", [AST("!", [last]), rast])],
        ),
    )


def expr(stream: t.List[str]) -> t.Tuple[int, AST]:
    try:
        with RecursionHelper(8000):
            return xorop(stream)
    except IndexError:
        raise SyntaxError("Unexpected EOL.")


def ifop(stream: t.List[str]) -> AST:
    n, last = expr(stream)
    if not stream[n:] or stream[n] not in ("=>", "<=>"):
        raise SyntaxError("Expected => or <=>.")
    if not stream[n + 1 :]:
        raise SyntaxError("Expected expression.")
    m, rast = expr(stream[n + 1 :])
    if stream[n + 1 + m :]:
        raise SyntaxError("Unexpected character '{}'.".format(stream[n + 1 + m]))
    return AST(stream[n], [last, rast])


def ident_serie(stream: t.List[str]) -> t.List[AST]:
    if [*filter(lambda s: not s.isalpha(), stream)]:
        raise SyntaxError("Unexpected character.")
    return [*map(AST, stream)]