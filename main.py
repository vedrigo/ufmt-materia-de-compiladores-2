from sintatico import Sintatico
from lexico import Lexico
from semantico import Semantico
from maqhipo import MaqHipo
import os
import sys

os.system('cls' if os.name == 'nt' else 'clear')
if(len(sys.argv) > 1):
    tokens = Lexico(str(sys.argv[1])).lista_de_tokens
else:
    tokens = Lexico('Entrada/teste1.txt').lista_de_tokens

if (Sintatico(tokens).resultado):
    if(Semantico(tokens).resultado):
        MaqHipo(tokens)
