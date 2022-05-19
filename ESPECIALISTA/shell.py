import typing as t

import engine
import interpreter as interp
import lexer
import parse

def process(
    eng: engine.InferenceEngine,
    stmts: t.List[interp.Statement],
    ln: t.Optional[int] = 0,
) -> None:
    for stmt in stmts:
        if isinstance(stmt, interp.Fact):
            eng.add_fact(stmt)
        elif isinstance(stmt, interp.Rule):
            eng.add_rule(stmt)
        else:
            if ln:
                print("Line {}: ".format(ln), end="")
            try:
                print("Rule {}, {}".format(stmt.name, eng.infer_hypothesis(stmt.name)))
            except (engine.ContradictionError, engine.CycleError) as e:
                print("Rule {}, False ({})".format(stmt.name, e))

def stdin_parse() -> None:
    eng = engine.InferenceEngine()
    while True:
        user_input = input("#=> ").strip()
        try:
            if user_input == "quit":
                print("Goodbye !")
                break
            if user_input == "reset":
                eng = engine.InferenceEngine()
                continue
            processed_input = lexer.lex(user_input)
            if not processed_input:
                continue
            if processed_input[0] in ("=", "?"):
                process(
                    eng,
                    interp.run(
                        parse.AST(
                            processed_input[0], parse.ident_serie(processed_input[1:])
                        )
                    ),
                )
            else:
                stmt = parse.ifop(processed_input)
                if stmt.name == "<=>":
                    process(
                        eng,
                        interp.run(parse.AST("=>", stmt.operands))
                        + interp.run(parse.AST("=>", stmt.operands[::-1])),
                    )
                else:
                    process(eng, interp.run(stmt))
        except RuntimeError:
            print(
                "Maximum recursion depth reached, "
                "please make the expression simpler."
            )
        except Exception as e:
            print(e)


def fparse(filename: str) -> None:
    eng = engine.InferenceEngine()
    with open(filename) as f:
        for i, line in enumerate(f, 1):
            try:
                if line.strip() == "reset":
                    eng = engine.InferenceEngine()
                    continue
                if line.strip().startswith("display "):
                    print(line.strip()[8:])
                    continue
                if not line.strip():
                    continue
                processed_input = lexer.lex(line)
                if not processed_input:
                    continue
                if processed_input[0] in ("=", "?"):
                    process(
                        eng,
                        interp.run(
                            parse.AST(
                                processed_input[0],
                                parse.ident_serie(processed_input[1:]),
                            )
                        ),
                        i,
                    )
                else:
                    stmt = parse.ifop(processed_input)
                    if stmt.name == "<=>":
                        process(
                            eng,
                            interp.run(parse.AST("=>", stmt.operands))
                            + interp.run(parse.AST("=>", stmt.operands[::-1])),
                        )
                    else:
                        process(eng, interp.run(stmt))
            except RuntimeError:
                print(
                    "Line {}: Maximum recursion depth reached, "
                    "please make the expression simpler.".format(i + 1)
                )
            except Exception as e:
                print(e)