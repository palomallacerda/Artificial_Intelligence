import typing as t

OPERATOR_SET = frozenset(("(", ")", "!", "+", "|", "^", "=>", "<=>"))

def lex(stream: str) -> t.List[str]:
    i = 0
    tokens = []
    N = len(stream)
    while i < N:
        for s in OPERATOR_SET:
            if stream[i:].startswith(s):
                i += len(s)
                tokens.append(s)
                break
        else:
            if stream[i] == "#":
                return tokens
            if stream[i].isspace():
                pass
            else:
                tokens.append(stream[i])
            i += 1
    return tokens


def lex_file(filename: str) -> t.List[t.List[str]]:
    with open(filename) as f:
        return [*map(lex, f)]