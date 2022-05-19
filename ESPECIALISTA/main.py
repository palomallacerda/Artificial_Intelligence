# Conjunto das regras

# voa & bota ovos -> ave:
# mamifero & come carne -> carnivoro
# mamifero & dentes pontudos & garras & olhos frontais -> carnivoro.
# mamifero & casco -> ungulado
# mamifero & rumina & dedos pares -> ungulado
# carnivoro & cor amerelo tostado & manchas escuras -> leopardo

# Canivoro & cor amarelo tostato & listras pretas -> Tigre
# ungulado & pernas longas & pescoço comprido & cor amarelo tostado & manchas escuras -> girafa

# ungulado & cor branca & listas pretas -> zebra
# ave & pernas longas & pescoço comprido & preto e branco -> avestruz
# ave & não voa & nada & é preto e branco -> peguim
# ave & bom voador -> albatroz

# ############################# DICIONARIO ##############################
# Pelo = P
# Mamifero = M
# Leite = L
# penas = e
# ave = a
# voa = v
# bota ovos = b
# come carne = c
# carnivoro = k
# dentes pontudos = d
# garras = g
# olhos frontais = o
# casco = C
# ungulado = u
# rumina = r
# dedos pares = D
# cor amarelo tostado = A
# manchas escutas = m
# leopardo = l
# listras pretas = p
# Tigre = t
# pernas longas = E
# pescoço comprido = s
# girafa = G
# cor branca = B
# zebra = z
# preto e branco = R
# avestruz = V
# não voa = Y
# nada = n
# peguim = U
# bom voador = X
# albatroz = H
# INSIRA AS REGRAS 

import sys

import shell


def main() -> None:
    try:
        if sys.argv[1:]:
            return shell.fparse(sys.argv[1])
        print("####################################################")
        print("############# WELCOME - ENTER THE RULES ############")
        print("Grammar:")
        print("(+ = binary and) (| = binary or) (^ = binary xor) (! = unary not)")
        print("(=> = implication) (<=> = bi-diretinal implication) (=ARGS  = fact list) (?ARGS = hypothesis list)")
        print("")
        print('Type "quit" to exit the program.')
        return shell.stdin_parse()
    except (EOFError, KeyboardInterrupt):
        exit("Goodbye !")
    except Exception as e:
        exit(e)


if __name__ == "__main__":
    main()  