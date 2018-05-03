import sys
from pprint import pprint
from sintatico import Sintatico
from lexico import Lexico

Sintatico(
    Lexico('Entrada/teste1.txt').lista_de_tokens
)
