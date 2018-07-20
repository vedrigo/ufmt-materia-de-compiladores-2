from sintatico import Sintatico
from lexico import Lexico
from semantico import Semantico
from maqhipo import MaqHipo

tokens = Lexico('Entrada/teste1.txt').lista_de_tokens

if (Sintatico(tokens).resultado):
    if(Semantico(tokens).resultado):
        MaqHipo(tokens)
