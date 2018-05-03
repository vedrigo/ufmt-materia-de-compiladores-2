from colors import Colors
import sys

# atributos dos tokens
token = 0
linha = 1
coluna = 2
tipo = 3


class Sintatico(object):
    token = list()
    tokens = list()
    linhaToken = 0
    msg = ""
    pilha = list()

    def __init__(self, tokens_de_entrada):
        self.tokens = tokens_de_entrada

        if (self.programa()):
            print(Colors().sucess, "\n########SINTÁICO COM SUCESSO!!!##########\n", Colors().reset)
        else:
            print(Colors().danger, "\n\n########ERRO NO SINTÁTICO########")
            print("Token: ", self.token)
            print("Lista de tokens posição", self.linhaToken)
            print(Colors().pink, "\nO token esperado era", self.pilha[-1])
            self.pilha.reverse()
            print(self.pilha)

    def nextToken(self):
        print("função nextToken")
        self.token = self.tokens[self.linhaToken]
        self.linhaToken += 1
        if (self.token[tipo] == "Comentário"):
            print("encontrado", Colors().blue, "Comentário", Colors().reset)
            self.nextToken()

    def prevToken(self):
        print("função prevToken")
        self.linhaToken -= 1
        self.token = self.tokens[self.linhaToken]

    def programa(self):
        print("função programa")
        self.nextToken()
        self.pilha += ['.', 'CORPO', 'ident', 'program']

        if (self.token[token] == "program"):
            print("encontrado", Colors().blue, "program", Colors().reset)
            print("sai da pilha:", self.pilha.pop())
            self.nextToken()

            if (self.token[tipo] == "Identificador"):
                print("encontrado", Colors().blue, self.token[token], Colors().reset)
                print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.corpo()):
                    self.nextToken()
                    print("sai da pilha:", self.pilha.pop())

                    if (self.token[token] == '.'):
                        print("encontrado", Colors().blue, " .", Colors().reset)
                        print("sai da pilha:", self.pilha.pop())
                        print("sai da pilha:", self.pilha)
                        return True

        print(Colors().warning, "não é programa", Colors().reset)
        return False

    def corpo(self):
        print("função corpo")
        self.pilha += ['end', 'COMANDOS', 'begin', 'DC']

        if (self.dc()):
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.token[token] == "begin"):
                print("encontrado", Colors().blue, " begin", Colors().reset)
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.comandos()):
                    self.nextToken()
                    print("sai da pilha:", self.pilha.pop())

                    if (self.token[token] == "end"):
                        print("encontrado", Colors().blue, " end", Colors().reset)
                        print("sai da pilha:", self.pilha.pop())
                        return True

        print(Colors().warning, "não é corpo", Colors().reset)
        return False

    def dc(self):
        print("função dc")

        if (self.dc_v()):
            self.nextToken()
            self.pilha += ['MAIS_DC']

            if (self.mais_dc()):
                print("sai da pilha:", self.pilha.pop())
                return True

            return False

        elif (self.dc_p()):
            self.nextToken()
            self.pilha += ['MAIS_DC']

            if (self.mais_dc()):
                print("sai da pilha:", self.pilha.pop())
                return True

            return False

        elif (' '):
            print("dc passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def mais_dc(self):
        print("função mais_dc")

        if (self.token[token] == ';'):
            print("encontrado", Colors().blue, " ;", Colors().reset)
            self.pilha += ['DC']
            self.nextToken()
            if (self.dc()):
                print("sai da pilha:", self.pilha.pop())
                return True
            return False

        elif (' '):
            print(Colors().warning, "não é mais_dc", Colors().reset)
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def dc_v(self):
        print("função dc_v")
        self.pilha += ['TIPO_VAR', ':', 'VARIAVEIS', 'var']

        if (self.token[token] == "var"):
            print("encontrado", Colors().blue, " var", Colors().reset)
            print("sai da pilha:", self.pilha.pop())
            self.nextToken()

            if (self.variaveis()):
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.token[token] == ':'):
                    print("encontrado", Colors().blue, " :", Colors().reset)
                    print("sai da pilha:", self.pilha.pop())
                    self.nextToken()

                    if (self.tipo_var()):
                        print("sai da pilha:", self.pilha.pop())
                        return True

        print(Colors().warning, "não é dc_v", Colors().reset)
        return False

    def tipo_var(self):
        print("função tipo_var")

        if (self.token[token] == "real"):
            print("encontrado", Colors().blue, " real", Colors().reset)
            return True

        elif (self.token[token] == "integer"):
            print("encontrado", Colors().blue, " integer", Colors().reset)
            return True

        print(Colors().warning, "não é tipo_var", Colors().reset)
        return False

    def variaveis(self):
        print("função variaveis")
        self.pilha += ['MAIS_VAR', 'ident']

        if (self.token[tipo] == "Identificador"):
            print("encontrado", Colors().blue, self.token[token], Colors().reset)
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.mais_var()):
                print("sai da pilha:", self.pilha.pop())
                return True

        print(Colors().warning, "não é variaveis", Colors().reset)
        return False

    def mais_var(self):
        print("função mais_var")
        if (self.token[token] == ','):
            print("encontrado", Colors().blue, " ,", Colors().reset)
            self.nextToken()

            if (self.variaveis()):
                return True
            return False

        elif (' '):
            print("mais_var passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def dc_p(self):
        print("função dc_p")
        self.pilha += ['CORPO_P', 'PARAMETROS', 'ident', 'procedure']

        if (self.token[token] == "procedure"):
            print("encontrado", Colors().blue, " procedure", Colors().reset)
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.token[tipo] == "Identificador"):
                print("encontrado", Colors().blue, self.token[token], Colors().reset)
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.parametros()):
                    self.nextToken()
                    print("sai da pilha:", self.pilha.pop())

                    if (self.corpo()):
                        print("sai da pilha:", self.pilha.pop())
                        return True

        print(Colors().warning, "não é dc_p", Colors().reset)
        return False

    def parametros(self):
        print("função parametros")

        if (self.token[token] == '('):
            print("encontrado", Colors().blue, " ( ", Colors().reset)
            self.nextToken()

            if (self.lista_par()):
                self.nextToken()

                if (self.token[token] == ')'):
                    print("encontrado", Colors().blue, " )", Colors().reset)
                    return True

            return False

        elif (' '):
            print("parametros passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def lista_par(self):
        print("função lista_par")
        self.pilha += ['MAIS_PAR', 'TIPO_VAR', ':', 'VARIAVEIS']

        if (self.variaveis()):
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.token[token] == ':'):
                print("encontrado", Colors().blue, " : ", Colors().reset)
                print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.tipo_var()):
                    self.nextToken()
                    print("sai da pilha:", self.pilha.pop())

                    if (self.mais_par()):
                        print("sai da pilha:", self.pilha.pop())
                        return True

        print(Colors().warning, "não é lista_par", Colors().reset)
        return False

    def mais_par(self):
        print("função mais_par")

        if (self.token[token] == ';'):
            print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()

            if (self.lista_par()):
                return True

            return False

        elif (' '):
            print("mais_par passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def corpo_p(self):
        print("função corpo_p")
        self.pilha += ['end', 'COMANDOS', 'begin', 'DC_LOC']

        if (self.dc_loc()):
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.token[token] == "begin"):
                print("encontrado", Colors().blue, " begin", Colors().reset)
                print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.comandos()):
                    self.nextToken()
                    print("sai da pilha:", self.pilha.pop())

                    if (self.token[token] == "end"):
                        print("encontrado", Colors().blue, " end", Colors().reset)
                        print("sai da pilha:", self.pilha.pop())
                        return True

        print(Colors().warning, "não é corpo_p", Colors().reset)
        return False

    def dc_loc(self):
        print("função dc_loc")

        if (self.dc_v()):
            self.nextToken()

            if (self.mais_dcloc()):
                return True

            return False

        elif (' '):
            print("dc_loc passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            return True

    def mais_dcloc(self):
        print("função mais_dcloc")

        if (self.token[token] == ';'):
            print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()
            self.pilha += ['DC_LOC']

            if (self.dc_loc()):
                print("sai da pilha:", self.pilha.pop())
                return True

            return False

        elif (' '):
            print("mais_dcloc passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def lista_arg(self):
        print("função lista_arg")

        if (self.token[token] == ';'):
            print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()
            self.pilha += ['DC_LOC']

            if (self.dc_loc()):
                print("sai da pilha:", self.pilha.pop())
                return True

            return False

        elif (' '):
            print("lista_arg")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def argumentos(self):
        print("função argumentos")
        self.pilha += ['MAIS_IDENT', 'ident']

        if (self.token[tipo] == 'Identificador'):
            print("encontrado", Colors().blue, self.token[token], Colors().reset)
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.mais_ident()):
                print("sai da pilha:", self.pilha.pop())
                return True

        return False

    def mais_ident(self):
        print("função mais_ident")

        if (self.token[token] == ';'):
            print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()
            self.pilha += ['ARGUMENTOS']

            if (self.argumentos()):
                print("sai da pilha:", self.pilha.pop())
                return True

            return False

        elif (' '):
            print("mais_ident passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def pfalsa(self):
        print("função pfalsa")

        if (self.token[token] == "else"):
            print("encontrado", Colors().blue, " else", Colors().reset)
            self.nextToken()
            self.pilha += ['COMANDOS']

            if (self.comandos()):
                print("sai da pilha:", self.pilha.pop())
                return True
            return False

        elif (' '):
            print("pfalsa passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def comandos(self):
        print("função comandos")
        self.pilha += ['MAIS_COMANDOS', 'COMANDO']

        if (self.comando()):
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.mais_comandos()):
                print("sai da pilha:", self.pilha.pop())
                return True

        return False

    def mais_comandos(self):
        print("função mais_comandos")

        if (self.token[token] == ';'):
            print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()
            self.pilha += ['COMANDOS']

            if (self.comandos()):
                print("sai da pilha:", self.pilha.pop())
                return True

            return False

        elif (' '):
            print("mais_comandos passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def comando(self):
        print("função comando")

        if (self.token[token] == "read"):
            print("encontrado", Colors().blue, " read", Colors().reset)
            self.nextToken()
            self.pilha += [')', 'VARIAVEIS', '(']

            if (self.token[token] == "("):
                print("encontrado", Colors().blue, " (", Colors().reset)
                print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.variaveis()):
                    print("sai da pilha:", self.pilha.pop())
                    self.nextToken()

                    if (self.token[token] == ")"):
                        print("encontrado", Colors().blue, " )", Colors().reset)
                        print("sai da pilha:", self.pilha.pop())
                        return True

        elif (self.token[token] == "write"):
            print("encontrado", Colors().blue, " write", Colors().reset)
            self.nextToken()
            self.pilha += [')', 'VARIAVEIS', '(']

            if (self.token[token] == "("):
                print("encontrado", Colors().blue, " (", Colors().reset)
                print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.variaveis()):
                    print("sai da pilha:", self.pilha.pop())
                    self.nextToken()

                    if (self.token[token] == ")"):
                        print("encontrado", Colors().blue, " )", Colors().reset)
                        print("sai da pilha:", self.pilha.pop())
                        return True

        elif (self.token[token] == "while"):
            print("encontrado", Colors().blue, " while", Colors().reset)
            self.nextToken()
            self.pilha += ['$', 'COMANDOS', 'do', 'CONDICAO']

            if (self.condicao()):
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.token[token] == "do"):
                    print("encontrado", Colors().blue, " do", Colors().reset)
                    print("sai da pilha:", self.pilha.pop())
                    self.nextToken()

                    if (self.comandos()):
                        print("sai da pilha:", self.pilha.pop())
                        self.nextToken()

                        if (self.token[token] == '$'):
                            print("encontrado", Colors().blue, " $", Colors().reset)
                            print("sai da pilha:", self.pilha.pop())
                            return True

        elif (self.token[token] == "if"):
            self.nextToken()
            self.pilha += ['$', 'PFALSA', 'COMANDOS', 'the', 'CONDICAO']

            if (self.condicao()):
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.token[token] == "then"):
                    print("encontrado", Colors().blue, " then", Colors().reset)
                    self.nextToken()
                    print("sai da pilha:", self.pilha.pop())

                    if (self.comando()):
                        self.nextToken()
                        print("sai da pilha:", self.pilha.pop())

                        if (self.pfalsa()):
                            self.nextToken()
                            print("sai da pilha:", self.pilha.pop())

                            if (self.token[token] == '$'):
                                print("encontrado", Colors().blue, " $", Colors().reset)
                                print("sai da pilha:", self.pilha.pop())
                                return True

        elif (self.token[tipo] == "Identificador"):
            print("encontrado", Colors().blue, self.token[token], Colors().reset)
            self.nextToken()
            self.pilha += ['RESTOIDENT']

            if (self.restoident()):
                print("sai da pilha:", self.pilha.pop())
                return True

        print(Colors().warning, "não é comando", Colors().reset)
        return False

    def restoident(self):
        print("função restoident")

        if (self.token[token] == ":="):
            print("encontrado", Colors().blue, " :=", Colors().reset)
            self.nextToken()
            self.pilha += ['EXPRESSAO']

            if (self.expressao()):
                print("sai da pilha:", self.pilha.pop())
                return True

        elif (self.lista_arg()):
            return True

        print(Colors().warning, "não é restoident", Colors().reset)
        return False

    def condicao(self):
        print("função condicao")
        self.pilha += ['EXPRESSAO', 'RELACAO', 'EXPRESSAO']

        if (self.expressao()):
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.relacao()):
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.expressao()):
                    print("sai da pilha:", self.pilha.pop())
                    return True

        print(Colors().warning, "não é condicao", Colors().reset)
        return False

    def relacao(self):
        print("função relacao")

        if (self.token[token] == '='):
            print("encontrado", Colors().blue, " =", Colors().reset)
            return True

        elif (self.token[token] == "<>"):
            print("encontrado", Colors().blue, " <>", Colors().reset)
            return True

        elif (self.token[token] == ">="):
            print("encontrado", Colors().blue, " >=", Colors().reset)
            return True

        elif (self.token[token] == "<="):
            print("encontrado", Colors().blue, " <=", Colors().reset)
            return True

        elif (self.token[token] == '>'):
            print("encontrado", Colors().blue, " >", Colors().reset)
            return True

        elif (self.token[token] == '<'):
            print("encontrado", Colors().blue, " <", Colors().reset)
            return True

        print(Colors().warning, "não é relacao", Colors().reset)
        return False

    def expressao(self):
        print("função expressao")
        self.pilha += ['OUTROS_TERMOS', 'TERMO']

        if (self.termo()):
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.outros_termos()):
                print("sai da pilha:", self.pilha.pop())
                return True

        print(Colors().warning, "não é expressao", Colors().reset)
        return False

    def op_un(self):
        print("função relacao")

        if (self.token[token] == '+'):
            print("encontrado", Colors().blue, " +", Colors().reset)
            return True

        elif (self.token[token] == '-'):
            print("encontrado", Colors().blue, " -", Colors().reset)
            return True

        elif (' '):
            print("op_un passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def outros_termos(self):
        print("função outros_termos")

        if (self.op_ad()):
            self.nextToken()
            self.pilha += ['OUTROS_TERMOS', 'TERMO']

            if (self.termo()):
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.outros_termos()):
                    print("sai da pilha:", self.pilha.pop())
                    return True

            return False

        elif (' '):
            print("outros_termos passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def op_ad(self):
        print("função op_ad")

        if (self.token[token] == '+'):
            print("encontrado", Colors().blue, " +", Colors().reset)
            return True

        elif (self.token[token] == '-'):
            print("encontrado", Colors().blue, " -", Colors().reset)
            return True

        print(Colors().warning, "não é op_ad", Colors().reset)
        return False

    def termo(self):
        print("função termo")
        self.pilha += ['MAIS_FATORES', 'FATOR', 'OP_UN']

        if (self.op_un()):
            self.nextToken()
            print("sai da pilha:", self.pilha.pop())

            if (self.fator()):
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.mais_fatores()):
                    print("sai da pilha:", self.pilha.pop())
                    return True

        print(Colors().warning, "não é termo", Colors().reset)
        return False

    def mais_fatores(self):
        print("função mais_fatores")

        if (self.op_mul()):
            self.nextToken()

            if (self.fator()):
                self.nextToken()

                if (self.mais_fatores()):
                    return True
            return False

        elif (' '):
            print("mais_fatores passou em branco")
            print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def op_mul(self):
        print("função op_mul")

        if (self.token[token] == '*'):
            print("encontrado", Colors().blue, " *", Colors().reset)
            return True

        elif (self.token[token] == '/'):
            print("encontrado", Colors().blue, " /", Colors().reset)
            return True

        print(Colors().warning, "não é op_mul", Colors().reset)
        return False

    def fator(self):
        print("função fator")

        if (self.token[tipo] == "Identificador"):
            print("encontrado", Colors().blue, self.token[token], Colors().reset)
            return True

        elif (self.token[tipo] == "Numero inteiro"):
            print("encontrado", Colors().blue, " Numero inteiro", Colors().reset)
            return True

        elif (self.token[tipo] == "Numero de ponto flutuante"):
            print("encontrado", Colors().blue, " Numero de ponto flutuante", Colors().reset)
            return True

        elif (self.token[token] == '('):
            print("encontrado", Colors().blue, " (", Colors().reset)
            self.nextToken()
            self.pilha += [')', 'EXPRESSAO']

            if (self.expressao()):
                self.nextToken()
                print("sai da pilha:", self.pilha.pop())

                if (self.token[token] == ')'):
                    print("encontrado", Colors().blue, " )", Colors().reset)
                    print("sai da pilha:", self.pilha.pop())
                    return True

        print(Colors().warning, "não é fator", Colors().reset)
        return False
