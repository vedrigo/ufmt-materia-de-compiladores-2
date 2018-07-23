import copy

# atributos dos tokens
token, linha, coluna, tipo = 0, 1, 2, 3
C, D = [], []


class MaqHipo:
    token = []
    tokens = []
    linhaToken = 0
    pilha = []
    escopo = []
    pilha_execucao = []
    semente = 0
    tabela = []
    msg = ''
    sinaliza_tipo = False
    sinaliza_inserir = False
    sinaliza_procedimento = None
    sequencia_parametros = []
    ultimo_token_buscado = []
    tabela_hipo = []

    def __init__(self, tokens_de_entrada):
        self.tokens = tokens_de_entrada
        self.escopo.append(['0', 'livre'])
        linha = ['cadeia', ['escopo'], 'categoria e tipo', 'end_rel', 'prim_instr']
        self.tabela.append(copy.deepcopy(linha))
        if (self.programa()):
            print("\n########MAQHIPO COM SUCESSO!!!##########\n")
            for x in range(len(self.tabela)):
                print(x, self.tabela[x])
        else:
            print("\n########ERRO NA MAQHIPO########")
            print(self.pilha[-1])
            print(self.msg)

    def programa(self):
        self.nextToken()

        if (self.token[token] == "program"):
            self.semente += 1
            self.escopo.append([self.semente, 'estrito'])
            self.nextToken()

            if (self.token[tipo] == "Identificador"):
                self.pilha += ['Erro ao inserir o token: ' + str(self.token)]
                if(self.inserir([self.token[token], self.escopo, 'program', ''], True)):
                    self.pilha.pop()
                    self.nextToken()
                    if (self.corpo()):
                        self.nextToken()

                        if (self.token[token] == '.'):
                            self.escopo.pop()
                            return True

        return False

    #simbolo, escopo([semente, tipo]), tipo, valor
    def buscar(self, linha):
        lista = list()
        flag = False

        for x in self.pilha_execucao:
            if(x[0] == linha[0]):
                if(flag):
                    lista.append(x)
                else:
                    flag = True

        for x in self.tabela:
            if(x[0] == linha[0]):
                lista.append(x)

        c_linha = copy.deepcopy(linha)
        # for faz do tamanha da pilha de escopo menos 1 até chegar na raiz
        for x in range(len(c_linha[1]) - 1):
            #c_linha na ultima posição de escopo em tipo
            if(c_linha[1][-1][1] == 'livre'):
                for y in lista:
                    if(c_linha[1] == y[1]):
                        self.msg = 'Token ' + c_linha[0] + ' já declarada!'
                        self.ultimo_token_buscado = y
                        if(not self.sinaliza_tipo):
                            self.sinaliza_tipo = y
                        return True
                c_linha[1].pop()
            else:
                for y in lista:
                    if (c_linha[1] == y[1]):
                        self.msg = 'Token ' + c_linha[0] + ' já declarada!'
                        self.ultimo_token_buscado = y
                        if (not self.sinaliza_tipo):
                            self.sinaliza_tipo = y
                        return True

        return False

    def buscar2(self, nome):
        for x in self.tabela:
            if(x[0] == nome):
                return x
        return False

    def inserir(self, linha, tabela):
        if(tabela):
            if(self.buscar(linha)):
                return False
            else:
                self.tabela.append(copy.deepcopy(linha))
                #verifica se é sinaliza procedimento
                if(self.sinaliza_procedimento is not None):
                    #busca na tabela de simbolos o sinaliza procedimento
                    x = self.buscar2(self.sinaliza_procedimento)
                    #recupera tabela de simbolos os tipos dos sinaliza procedimento e concateno o novo atual
                    #atualiza tabela de simbolos
                    x[2] += ',' + linha[2]

                return True
        else:
            if (self.buscar(linha)):
                return False
            else:
                self.pilha_execucao.append(copy.deepcopy(linha))
                return True

    def aplicarTipo(self, tipo):
        for x in self.pilha_execucao:
            x[2] = tipo
            if(not self.inserir(x, True)):
                self.pilha += ['erro ao inserir os tokens da linha: ' + str(self.token[linha])]
                self.msg += '\nerro em aplicarTipo'
                return False
        self.pilha_execucao.clear()
        return True

    def comparar(self, tipo):
        if(not self.sinaliza_tipo):
            self.sinaliza_tipo = copy.deepcopy(tipo)
            return True
        elif(tipo[2] != self.sinaliza_tipo[2]):
            self.msg = 'operação com tipos diferentes'
            return False
        return True

    def nextToken(self):
        self.token = self.tokens[self.linhaToken]
        self.linhaToken += 1
        if (self.token[tipo] == "Comentário"):
            self.nextToken()

    def prevToken(self):
        self.linhaToken -= 1
        self.token = self.tokens[self.linhaToken]

    def corpo(self):

        if (self.dc()):
            self.nextToken()

            if (self.token[token] == "begin"):
                self.nextToken()
                self.semente += 1
                self.escopo.append([self.semente, 'livre'])

                if (self.comandos()):
                    self.escopo.pop()
                    self.nextToken()

                    if (self.token[token] == "end"):
                        return True

        return False

    def dc(self):
        dc_v = self.dc_v()
        if (dc_v or dc_v == 'Deu ruim'):
            if (dc_v == 'Deu ruim'):
                return False
            else:
                self.nextToken()
                if (self.mais_dc()):
                    return True

                return False

        elif (not dc_v):
            dc_p = self.dc_p()
            if (dc_p or dc_p == 'Deu ruim'):

                if (dc_p == 'Deu ruim'):
                    return False
                else:
                    self.nextToken()
                    if (self.mais_dc()):
                        return True

                    return False

            elif (' '):
                self.prevToken()
                return True

    def mais_dc(self):

        if (self.token[token] == ';'):
            self.nextToken()
            if (self.dc()):
                return True
            return False

        elif (' '):
            self.prevToken()
            return True

    def dc_v(self):

        if (self.token[token] == "var"):
            self.pilha_execucao.clear()
            self.nextToken()

            self.sinaliza_inserir = True
            if (self.variaveis()):
                self.sinaliza_inserir = False
                self.nextToken()

                if (self.token[token] == ':'):
                    self.nextToken()

                    if (self.tipo_var()):
                        return True
            return 'Deu ruim'

        return False

    def tipo_var(self):

        if (self.token[token] == "real"):
            if(self.aplicarTipo('real')):
                return True

        elif (self.token[token] == "integer"):
            if(self.aplicarTipo('integer')):
                return True

        return False

    def variaveis(self):

        if (self.token[tipo] == "Identificador"):
            if (self.sinaliza_inserir):
                self.pilha += ['erro ao inserir o token: ' + str(self.token)]
                if(self.inserir([self.token[token], self.escopo, 'ident', ''], False)):
                    self.pilha.pop()
                    self.nextToken()
                    if (self.mais_var()):
                        return True
            else:
                self.nextToken()
                if (self.mais_var()):
                    return True

        return False

    def mais_var(self):
        if (self.token[token] == ','):
            self.nextToken()

            if (self.variaveis()):
                return True
            return False

        elif (' '):
            self.prevToken()
            return True

    def dc_p(self):

        if (self.token[token] == "procedure"):
            self.nextToken()

            if (self.token[tipo] == "Identificador"):
                self.pilha += ['erro ao inserir o token:' + str(self.token)]
                if(self.inserir([self.token[token], self.escopo, 'procedure', ''], True)):
                    self.pilha.pop()

                    self.semente += 1
                    self.escopo.append([self.semente, 'estrito'])
                    self.sinaliza_procedimento = self.token[token]
                    self.nextToken()

                    if (self.parametros()):
                        self.nextToken()
                        self.sinaliza_procedimento = None
                        if (self.corpo()):
                            self.escopo.pop()
                            return True
            return 'Deu ruim'

        return False

    def parametros(self):

        if (self.token[token] == '('):
            self.nextToken()

            if (self.lista_par()):
                self.nextToken()

                if (self.token[token] == ')'):
                    return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def lista_par(self):

        self.sinaliza_inserir = True
        if (self.variaveis()):
            self.sinaliza_inserir = False
            self.nextToken()

            if (self.token[token] == ':'):
                self.nextToken()

                if (self.tipo_var()):
                    self.nextToken()

                    if (self.mais_par()):
                        return True

        return False

    def mais_par(self):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.lista_par()):
                return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def corpo_p(self):

        if (self.dc_loc()):
            self.nextToken()

            if (self.token[token] == "begin"):
                self.nextToken()

                if (self.comandos()):
                    self.nextToken()

                    if (self.token[token] == "end"):
                        return True

        return False

    def dc_loc(self):

        if (self.dc_v()):
            self.nextToken()

            if (self.mais_dcloc()):
                return True

            return False

        elif (' '):
            return True

    def mais_dcloc(self):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.dc_loc()):
                return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def lista_arg(self):

        if (self.token[token] == '('):
            self.nextToken()

            if (self.ultimo_token_buscado[2].startswith('procedure')):
                self.sequencia_parametros = self.ultimo_token_buscado[2].split(',')
                self.sequencia_parametros.pop(0)

            if (self.argumentos()):
                self.nextToken()
                self.sequencia_parametros.clear

                if (self.token[token] == ')'):
                    return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def argumentos(self):

        if(self.sequencia_parametros != []):
            if (self.token[tipo] == 'Identificador'):
                self.pilha += ['erro ao buscar o token: ' + str(self.token)]
                self.msg = 'Token ' + str(self.token[token]) + ' ainda não foi declarado!'
                if(self.buscar([self.token[token], self.escopo, 'ident', ''])):
                    self.pilha.pop()
                    if(self.ultimo_token_buscado[2] == self.sequencia_parametros.pop(0)):
                        self.nextToken()
                        if (self.mais_ident()):
                            return True
            exit('Erro na linha ' + str(self.token[1]) + ' Parametro do procedimento incorreto')

        elif (self.token[tipo] == 'Identificador'):
            exit('\nErro na linha ' + str(self.token[1]) + ' Parametro sobrando.')

        elif(' '):
            self.prevToken()
            return True

    def mais_ident(self):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.argumentos()):
                return True

            return False
        elif(self.sequencia_parametros != []):
            exit('Erro na linha ' + str(self.token[1]) + ' Parametro do procedimento faltando')
        elif (' '):
            self.prevToken()
            return True

    def pfalsa(self):

        if (self.token[token] == "else"):
            self.nextToken()

            if (self.comandos()):
                return True
            return False

        elif (' '):
            self.prevToken()
            return True

    def comandos(self):

        if (self.comando()):
            self.nextToken()

            if (self.mais_comandos()):
                return True

        return False

    def mais_comandos(self):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.comandos()):
                return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def comando(self):
        self.sinaliza_tipo = False
        if (self.token[token] == "read"):
            self.nextToken()

            if (self.token[token] == "("):
                self.nextToken()

                if (self.variaveis()):
                    self.nextToken()

                    if (self.token[token] == ")"):
                        return True

        elif (self.token[token] == "write"):
            self.nextToken()

            if (self.token[token] == "("):
                self.nextToken()

                if (self.variaveis()):
                    self.nextToken()

                    if (self.token[token] == ")"):
                        return True

        elif (self.token[token] == "while"):
            self.semente += 1
            self.escopo.append([self.semente, 'livre'])
            self.nextToken()

            if (self.condicao()):
                self.nextToken()

                if (self.token[token] == "do"):
                    self.nextToken()

                    if (self.comandos()):
                        self.nextToken()

                        if (self.token[token] == '$'):
                            self.escopo.pop()
                            return True

        elif (self.token[token] == "if"):
            self.semente += 1
            self.escopo.append([self.semente, 'livre'])
            self.nextToken()

            if (self.condicao()):
                self.nextToken()

                if (self.token[token] == "then"):
                    self.nextToken()

                    if (self.comando()):
                        self.nextToken()

                        if (self.pfalsa()):
                            self.nextToken()

                            if (self.token[token] == '$'):
                                self.escopo.pop()
                                return True

        elif (self.token[tipo] == "Identificador"):
            self.pilha += ['erro ao buscar o token: ' + str(self.token)]
            self.msg = 'Token ' + str(self.token[token]) + ' ainda não foi declarado!'
            if (self.buscar([self.token[token], self.escopo, 'ident', ''])):
                self.pilha.pop()
                if(self.ultimo_token_buscado[2] == 'procedure'):
                    self.nextToken()
                    self.pilha += ['Esperado: (\nEncontrado: ' + str(self.token)]
                    self.msg = 'Chamada de Procedimento'
                    if(self.token[token] == "("):
                        self.pilha.pop()
                        self.nextToken()
                        self.pilha += ['parâmetros não passados']
                        if (self.argumentos()):
                            self.pilha.pop()
                            self.nextToken()
                            self.pilha += ['Esperado: )\nEncontrado: ' + str(self.token)]
                            if(self.token[token] == ")"):
                                self.pilha.pop()
                                return True
                else:
                    self.nextToken()
                    if (self.restoident()):
                        return True

        return False

    def restoident(self):

        if (self.token[token] == ":="):
            self.nextToken()

            if (self.expressao()):
                return True

        elif (self.lista_arg()):
            return True

        return False

    def condicao(self):

        if (self.expressao()):
            self.nextToken()

            if (self.relacao()):
                self.nextToken()

                if (self.expressao()):
                    return True

        return False

    def relacao(self):

        if (self.token[token] == '='):
            return True

        elif (self.token[token] == "<>"):
            return True

        elif (self.token[token] == ">="):
            return True

        elif (self.token[token] == "<="):
            return True

        elif (self.token[token] == '>'):
            return True

        elif (self.token[token] == '<'):
            return True

        return False

    def expressao(self):

        if (self.termo()):
            self.nextToken()

            if (self.outros_termos()):
                return True

        return False

    def op_un(self):

        if (self.token[token] == '+'):
            return True

        elif (self.token[token] == '-'):
            return True

        elif (' '):
            self.prevToken()
            return True

    def outros_termos(self):

        if (self.op_ad()):
            self.nextToken()

            if (self.termo()):
                self.nextToken()
                if (self.outros_termos()):
                    return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def op_ad(self):

        if (self.token[token] == '+'):
            return True

        elif (self.token[token] == '-'):
            return True

        return False

    def termo(self):

        if (self.op_un()):
            self.nextToken()

            if (self.fator()):
                self.nextToken()

                if (self.mais_fatores()):
                    return True

        return False

    def mais_fatores(self):

        if (self.op_mul()):
            self.nextToken()

            if (self.fator()):
                self.nextToken()

                if (self.mais_fatores()):
                    return True
            return False

        elif (' '):
            self.prevToken()
            return True

    def op_mul(self):

        if (self.token[token] == '*'):
            return True

        elif (self.token[token] == '/'):
            return True

        return False

    def fator(self):

        if (self.token[tipo] == "Identificador"):
            self.pilha += ['erro ao buscar o token:' + str(self.token)]
            self.msg = 'Token ' + str(self.token[token]) + ' ainda não foi declarado!'
            if(self.buscar([self.token[token], self.escopo, 'ident', ''])):
                self.pilha.pop()
                self.pilha += ['erro ao comparar o token:' + str(self.token)]
                if(self.comparar(self.ultimo_token_buscado)):
                    self.pilha.pop()
                    return True

        elif (self.token[tipo] == "Numero inteiro"):
            self.pilha += ['erro ao comparar o token:' + str(self.token)]
            if (self.comparar([self.token[token], self.escopo, 'integer', self.token[token]])):
                self.pilha.pop()
                return True

        elif (self.token[tipo] == "Numero de ponto flutuante"):
            self.pilha += ['erro ao comparar o token:' + str(self.token)]
            if (self.comparar([self.token[token], self.escopo, 'real', self.token[token]])):
                self.pilha.pop()
                return True

        elif (self.token[token] == '('):
            self.nextToken()

            if (self.expressao()):
                self.nextToken()

                if (self.token[token] == ')'):
                    return True

        return False
