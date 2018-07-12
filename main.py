from sintatico import Sintatico
from lexico import Lexico
from semantico import Semantico

tokens = Lexico('Entrada/teste1.txt').lista_de_tokens
if (Sintatico(tokens).resultado):
    Semantico(tokens)
