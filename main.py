from sintatico import Sintatico
from lexico import Lexico
from semantico import Semantico
from maqhipo import MaqHipo
from interpretador import Interpretador
import os
import sys

os.system('cls' if os.name == 'nt' else 'clear')
if(len(sys.argv) > 1):
    tokens = Lexico(str(sys.argv[1])).lista_de_tokens
else:
    tokens = Lexico('Entrada/Ex2.txt').lista_de_tokens

if (Sintatico(tokens).resultado):
    if(Semantico(tokens).resultado):
        maqHipo = MaqHipo(tokens)
        if(maqHipo.resultado):
            Interpretador(maqHipo.codigo_inter)
