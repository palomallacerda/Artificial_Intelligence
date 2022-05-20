"Atividade Feita pela aluna de graduação: Paloma Lacerda | Disciplina: IA"

# Conjunto das regras
# R1: SE Fadiga = sim E Dor_de_cabeça= sim E Dores_no_corpo = sim E  Ocasionais_dores_garganta = sim E Ocasionais_tosse = sim ENTÃO Covid19 = sim  
# R2: SE Dor_de_cabeça = Sim E Garganta_inflamada = Sim E Tosse = Sim  ENTÃO Diagnóstico = Gripe  
# R3: SE Cansaço = Sim E Dor_de_cabeça = Sim ENTÃO Diagnóstico = Mononucleose infecciosa  
# R4: SE Cansaço = Sim E Garganta_inflamada = Sim ENTÃO Diagnóstico = Amigdalite  
# R5: SE Cansaço = Sim ENTÃO Diagnóstico = Estresse 
# R6: SE Fadiga = sim E Dor_de_cabeça = sim E Pulsação_elevada = sim E  Baixo_nível_de_oxigênio = sim E Perda de olfato = sim E Perda de paladar = sim  ENTÃO Covid19 = sim  

# ############################# DICIONARIO ##############################
# Fadiga = f 
# dor de cabeça = d 
# dores no corpo = D 
# ocasionais dores garganta = g 
# ocasionais tosses = t 
# covid 19 = c 
# gargante inflamada = i 
# mononucleose infecciosa = M
# tosse = T 
# gripe = G 
# cansaço = C 
# Amigdalite = A 
# Estresse = E 
# fadiga = F 
# pulsação elevada = p 
# baixo nivel de oxigenio = o 
# perda de olfato = O 
# perda e paladar = P
import sys

import shell


def main() -> None:
    try:
        if sys.argv[1:]:
            return shell.fparse(sys.argv[1])
        print("####################################################")
        print("############# WELCOME TO YOUR DIAGNOSES SYSTEAM - ENTER THE RULES ############")
        print("Grammar SHOULD BE:")
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