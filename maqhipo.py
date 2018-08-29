import copy

# atributos dos tokens
token, linha, coluna, tipo = 0, 1, 2, 3
# pilhas para a maqhipo
C, D = [], []


class Parametro:

    def __init__(self, booleano=False, herdado=[], retorno=[]):
        self.herdado = herdado
        self.booleano = booleano
        self.retorno = retorno


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
    codigo_inter = []
    end_rel = 0
    prim_instr = 0
    posicoesDesviosProc = []
    endereco = 0
    resultado = False

    def __init__(self, tokens_de_entrada):
        par = Parametro()
        self.tokens = tokens_de_entrada
        self.escopo.append(['0', 'livre'])
        linha = ['NOME', ['escopo'], 'categoria/tipo', 'D', 'C']
        self.tabela.append(copy.deepcopy(linha))
        if (self.programa(par)):
            print("\n########MAQHIPO COM SUCESSO!!!##########\n")
            print("Tabela de Simbolos:")
            for x in range(len(self.tabela)):
                print(x, "\t:", self.tabela[x][0], "\t", self.tabela[x][3], "\t", self.tabela[x][4])
            print("\n")
            print("Código Intermediário:")
            for x in range(len(self.codigo_inter)):
                print(x, "\t:", self.codigo_inter[x])
            self.resultado = True

        else:
            print("\n########ERRO NA MAQHIPO########")
            print(self.pilha[-1])
            print(self.msg)
            self.resultado = False

    def programa(self, par):
        self.nextToken()

        if (self.token[token] == "program"):
            self.semente += 1
            self.escopo.append([self.semente, 'estrito'])
            self.nextToken()

            if (self.token[tipo] == "Identificador"):
                self.pilha += ['Erro ao inserir o token: ' + str(self.token)]
                if(self.inserir([self.token[token], self.escopo, 'program', '', ''], True)):
                    self.codigo_inter.append("INPP")
                    self.pilha.pop()
                    self.nextToken()
                    if (self.corpo(par)):
                        self.nextToken()

                        if (self.token[token] == '.'):
                            self.codigo_inter.append("PARA")
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
            x[3] = self.end_rel
            if(not self.inserir(x, True)):
                self.pilha += ['erro ao inserir os tokens da linha: ' + str(self.token[linha])]
                self.msg += '\nerro em aplicarTipo'
                return False
            if(self.sinaliza_inserir is True):
                self.endereco += 1
                self.codigo_inter.append("ALME 1")
            self.end_rel += 1

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

    def corpo(self, par):

        if (self.dc(par)):
            self.nextToken()

            if (self.token[token] == "begin"):
                self.nextToken()
                self.semente += 1
                self.escopo.append([self.semente, 'livre'])
                for x in self.posicoesDesviosProc:
                    self.codigo_inter[x] = "DSVI " + str(len(self.codigo_inter))

                if (self.comandos(par)):
                    self.escopo.pop()
                    self.nextToken()

                    if (self.token[token] == "end"):
                        return True

        return False

    def dc(self, par):
        dc_v = self.dc_v(par)
        if (dc_v or dc_v == 'Deu ruim'):
            if (dc_v == 'Deu ruim'):
                return False
            else:
                self.nextToken()
                if (self.mais_dc(par)):
                    return True

                return False

        elif (not dc_v):
            dc_p = self.dc_p(par)
            if (dc_p or dc_p == 'Deu ruim'):

                if (dc_p == 'Deu ruim'):
                    return False
                else:
                    self.nextToken()
                    if (self.mais_dc(par)):
                        return True

                    return False

            elif (' '):
                self.prevToken()
                return True

    def mais_dc(self, par):

        if (self.token[token] == ';'):
            self.nextToken()
            if (self.dc(par)):
                return True
            return False

        elif (' '):
            self.prevToken()
            return True

    def dc_v(self, par):

        if (self.token[token] == "var"):
            self.pilha_execucao.clear()
            self.nextToken()

            self.sinaliza_inserir = True
            if (self.variaveis(par)):
                self.nextToken()

                if (self.token[token] == ':'):
                    self.nextToken()

                    if (self.tipo_var(par)):
                        self.sinaliza_inserir = False
                        return True
            return 'Deu ruim'

        return False

    def tipo_var(self, par):

        if (self.token[token] == "real"):
            if(self.aplicarTipo('real')):
                return True

        elif (self.token[token] == "integer"):
            if(self.aplicarTipo('integer')):
                return True

        return False

    def variaveis(self, par):

        if (self.token[tipo] == "Identificador"):
            if (self.sinaliza_inserir):
                #print('Iniciado inserir em: variaveis > ident')
                self.pilha += ['erro ao inserir o token: ' + str(self.token)]
                if(self.inserir([self.token[token], self.escopo, 'ident', '', ''], False)):
                    self.pilha.pop()
                    #print('Terminado inserir em: variaveis > ident\n')
                    self.nextToken()
                    if (self.mais_var(par)):
                        return True
            elif(self.buscar([self.token[token], self.escopo, 'ident', ''])):
                if(par.herdado == "c_read"):
                    par.retorno.append(self.ultimo_token_buscado)
                elif(par.herdado == "c_write"):
                    par.retorno.append(self.ultimo_token_buscado)
                self.nextToken()
                if (self.mais_var(par)):
                    return True
            else:
                exit('\nErro na linha ' + str(self.token[linha]) + '. Variavel ' + str(self.token[token]) + ' não existe.')

        return False

    def mais_var(self, par):
        if (self.token[token] == ','):
            self.nextToken()

            if (self.variaveis(par)):
                return True
            return False

        elif (' '):
            self.prevToken()
            return True

    def dc_p(self, par):

        if (self.token[token] == "procedure"):
            self.nextToken()

            if (self.token[tipo] == "Identificador"):
                self.pilha += ['erro ao inserir o token:' + str(self.token)]
                if(self.inserir([self.token[token], self.escopo, 'procedure', '', ''], True)):
                    escopoBackup = self.escopo
                    self.pilha.pop()

                    self.semente += 1
                    self.escopo.append([self.semente, 'estrito'])
                    self.sinaliza_procedimento = self.token[token]
                    posDesvio = len(self.codigo_inter)
                    self.posicoesDesviosProc.append(posDesvio)
                    self.codigo_inter.append("DSVI ")
                    self.tabela[-1][4] = str(len(self.codigo_inter))
                    self.nextToken()
                    endVar = self.endereco + 1

                    if (self.parametros(par)):
                        self.nextToken()
                        self.sinaliza_procedimento = None
                        if (self.corpo(par)):
                            desalocar = 0
                            for x in self.tabela:
                                if escopoBackup == x[1]:
                                    desalocar += 1
                            self.codigo_inter.append("DESM " + str(desalocar))
                            self.codigo_inter.append("RTPR")
                            self.endereco = endVar
                            self.escopo.pop()
                            return True
            return 'Deu ruim'

        return False

    def parametros(self, par):

        if (self.token[token] == '('):
            self.nextToken()

            if (self.lista_par(par)):
                self.nextToken()

                if (self.token[token] == ')'):
                    return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def lista_par(self, par):

        self.sinaliza_inserir = True
        if (self.variaveis(par)):
            self.sinaliza_inserir = False
            self.nextToken()

            if (self.token[token] == ':'):
                self.nextToken()

                if (self.tipo_var(par)):
                    self.nextToken()

                    if (self.mais_par(par)):
                        return True

        return False

    def mais_par(self, par):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.lista_par(par)):
                return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def corpo_p(self, par):

        if (self.dc_loc(par)):
            self.nextToken()

            if (self.token[token] == "begin"):
                self.nextToken()

                if (self.comandos(par)):
                    self.nextToken()

                    if (self.token[token] == "end"):
                        return True

        return False

    def dc_loc(self, par):

        if (self.dc_v(par)):
            self.nextToken()

            if (self.mais_dcloc()):
                return True

            return False

        elif (' '):
            return True

    def mais_dcloc(self, par):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.dc_loc(par)):
                return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def lista_arg(self, par):

        if (self.token[token] == '('):
            self.nextToken()

            if (self.ultimo_token_buscado[2].startswith('procedure')):
                self.sequencia_parametros = self.ultimo_token_buscado[2].split(',')
                self.sequencia_parametros.pop(0)
                self.codigo_inter.append("PUSHER " + str(len(self.codigo_inter) + len(self.sequencia_parametros) + 2))
                instr = self.ultimo_token_buscado[4]

            if (self.argumentos(par)):
                self.nextToken()
                self.sequencia_parametros.clear()
                self.codigo_inter.append("CHPR " + str(instr))

                if (self.token[token] == ')'):
                    return True

            return False

        elif (' '):
            self.codigo_inter.append("PUSHER " + str(len(self.codigo_inter) + 2))
            self.codigo_inter.append("CHPR " + str(instr))
            self.prevToken()
            return True

    def argumentos(self, par):

        if(self.sequencia_parametros != []):
            if (self.token[tipo] == 'Identificador'):
                self.pilha += ['erro ao buscar o token: ' + str(self.token)]
                self.msg = 'Token ' + str(self.token[token]) + ' ainda não foi declarado!'
                if(self.buscar([self.token[token], self.escopo, 'ident', ''])):
                    self.pilha.pop()
                    if(self.ultimo_token_buscado[2] == self.sequencia_parametros.pop(0)):
                        self.codigo_inter.append("PARAM " + str(self.ultimo_token_buscado[3]))
                        self.nextToken()
                        if (self.mais_ident(par)):
                            return True
            exit('Erro na linha ' + str(self.token[1]) + ' Parametro do procedimento incorreto')

        elif (self.token[tipo] == 'Identificador'):
            exit('\nErro na linha ' + str(self.token[1]) + ' Parametro sobrando.')

        elif(' '):
            self.prevToken()
            return True

    def mais_ident(self, par):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.argumentos(par)):
                return True

            return False
        elif(self.sequencia_parametros != []):
            exit('Erro na linha ' + str(self.token[1]) + ' Parametro do procedimento faltando')
        elif (' '):
            self.prevToken()
            return True

    def pfalsa(self, par, posDesvio="Nulo"):

        if (self.token[token] == "else"):
            self.nextToken()
            posDesvio2 = len(self.codigo_inter)
            self.codigo_inter.append("DSVI ")
            self.codigo_inter[posDesvio] = "DSVF " + str(len(self.codigo_inter))
            if (self.comandos(par)):
                self.codigo_inter[posDesvio2] = "DSVI " + str(len(self.codigo_inter))
                return True
            return False

        elif (' '):
            self.prevToken()
            self.codigo_inter[posDesvio] = "DSVF " + str(len(self.codigo_inter))
            return True

    def comandos(self, par):

        if (self.comando(par)):
            self.nextToken()

            if (self.mais_comandos(par)):
                return True

        return False

    def mais_comandos(self, par):

        if (self.token[token] == ';'):
            self.nextToken()

            if (self.comandos(par)):
                return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def comando(self, par):
        self.sinaliza_tipo = False
        if (self.token[token] == "read"):
            self.nextToken()

            if (self.token[token] == "("):
                self.nextToken()
                par.herdado = "c_read"
                par.retorno = []
                if (self.variaveis(par)):
                    par.herdado = ""
                    for x in range(len(par.retorno)):
                        self.codigo_inter.append("LEIT")
                        y = str(par.retorno[x][3])
                        self.codigo_inter.append("ARMZ " + y)
                    self.nextToken()

                    if (self.token[token] == ")"):
                        return True

        elif (self.token[token] == "write"):
            self.nextToken()

            if (self.token[token] == "("):
                self.nextToken()
                par.herdado = "c_write"
                par.retorno = []
                if (self.variaveis(par)):
                    par.herdado = ""
                    for x in range(len(par.retorno)):
                        y = str(par.retorno[x][3])
                        self.codigo_inter.append("CRVL " + y)
                        self.codigo_inter.append("IMPR")
                    self.nextToken()

                    if (self.token[token] == ")"):
                        return True

        elif (self.token[token] == "while"):
            self.semente += 1
            self.escopo.append([self.semente, 'livre'])
            self.nextToken()
            posInicioWhile = len(self.codigo_inter)
            if (self.condicao(par)):
                self.nextToken()

                if (self.token[token] == "do"):
                    posDesvio = len(self.codigo_inter)
                    self.codigo_inter.append("DSVF ")
                    self.nextToken()

                    if (self.comandos(par)):
                        self.nextToken()

                        if (self.token[token] == '$'):
                            self.escopo.pop()
                            self.codigo_inter.append("DSVI " + str(posInicioWhile))
                            self.codigo_inter[posDesvio] = "DSVF " + str(len(self.codigo_inter))
                            return True

        elif (self.token[token] == "if"):
            self.semente += 1
            self.escopo.append([self.semente, 'livre'])
            self.nextToken()

            if (self.condicao(par)):
                posDesvio = len(self.codigo_inter)
                self.codigo_inter.append("DSVF ")
                self.nextToken()

                if (self.token[token] == "then"):
                    self.nextToken()

                    if (self.comando(par)):
                        self.nextToken()

                        if (self.pfalsa(par, posDesvio)):
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
                        if (self.argumentos(par)):
                            self.pilha.pop()
                            self.nextToken()
                            self.pilha += ['Esperado: )\nEncontrado: ' + str(self.token)]
                            if(self.token[token] == ")"):
                                self.pilha.pop()
                                return True
                else:
                    self.nextToken()
                    if (self.restoident(par)):
                        return True

        return False

    def restoident(self, par):

        if (self.token[token] == ":="):
            self.buscar([self.token[token], self.escopo, 'ident', ''])
            self.nextToken()

            if (self.expressao(par)):
                self.codigo_inter.append("ARMZ " + str(self.ultimo_token_buscado[3]))
                return True

        elif (self.lista_arg(par)):
            return True

        return False

    def condicao(self, par):

        if (self.expressao(par)):
            self.nextToken()

            if (self.relacao(par)):
                self.nextToken()

                if (self.expressao(par)):
                    return True

        return False

    def relacao(self, par):

        if (self.token[token] == '='):
            par.retorno = "CPIG"
            return True

        elif (self.token[token] == "<>"):
            par.retorno = "CDES"
            return True

        elif (self.token[token] == ">="):
            par.retorno = "CMAI"
            return True

        elif (self.token[token] == "<="):
            par.retorno = "CPMI"
            return True

        elif (self.token[token] == '>'):
            par.retorno = "CPMA"
            return True

        elif (self.token[token] == '<'):
            par.retorno = "CPME"
            return True

        return False

    def expressao(self, par):

        if (self.termo(par)):
            self.nextToken()

            if (self.outros_termos(par)):
                return True

        return False

    def op_un(self, par):

        if (self.token[token] == '+'):
            return True

        elif (self.token[token] == '-'):
            return True

        elif (' '):
            self.prevToken()
            return True

    def outros_termos(self, par):

        if (self.op_ad(par)):
            op = self.token[0]
            self.nextToken()

            if (self.termo(par)):
                if(op == "+"):
                    self.codigo_inter.append("SOMA")
                elif(op == "-"):
                    self.codigo_inter.append("SUBT")
                self.nextToken()
                if (self.outros_termos(par)):
                    return True

            return False

        elif (' '):
            self.prevToken()
            return True

    def op_ad(self, par):

        if (self.token[token] == '+'):
            return True

        elif (self.token[token] == '-'):
            return True

        return False

    def termo(self, par):
        if (self.op_un(par)):
            op = self.token[0]
            self.nextToken()

            if (self.fator(par)):
                if(op == "-"):
                    self.codigo_inter.append("INVE")
                self.nextToken()

                if (self.mais_fatores(par)):
                    return True

        return False

    def mais_fatores(self, par):

        if (self.op_mul(par)):
            op = self.token[0]
            self.nextToken()

            if (self.fator(par)):
                if(op == "*"):
                    self.codigo_inter.append("MULT")
                elif(op == "/"):
                    self.codigo_inter.append("DIVI")
                self.nextToken()

                if (self.mais_fatores(par)):
                    return True
            return False

        elif (' '):
            self.prevToken()
            return True

    def op_mul(self, par):

        if (self.token[token] == '*'):
            return True

        elif (self.token[token] == '/'):
            return True

        return False

    def fator(self, par):

        if (self.token[tipo] == "Identificador"):
            self.pilha += ['erro ao buscar o token:' + str(self.token)]
            self.msg = 'Token ' + str(self.token[token]) + ' ainda não foi declarado!'
            if(self.buscar([self.token[token], self.escopo, 'ident', ''])):
                self.codigo_inter.append("CRVL " + str(self.ultimo_token_buscado[3]))
                self.pilha.pop()
                self.pilha += ['erro ao comparar o token:' + str(self.token)]
                if(self.comparar(self.ultimo_token_buscado)):
                    self.pilha.pop()
                    return True

        elif (self.token[tipo] == "Numero inteiro"):
            self.pilha += ['erro ao comparar o token:' + str(self.token)]
            if (self.comparar([self.token[token], self.escopo, 'integer', self.token[token]])):
                self.codigo_inter.append("CRCT " + str(self.token[0]))
                self.pilha.pop()
                return True

        elif (self.token[tipo] == "Numero de ponto flutuante"):
            self.pilha += ['erro ao comparar o token:' + str(self.token)]
            if (self.comparar([self.token[token], self.escopo, 'real', self.token[token]])):
                self.codigo_inter.append("CRCT " + str(self.token[0]))
                self.pilha.pop()
                return True

        elif (self.token[token] == '('):
            self.nextToken()

            if (self.expressao(par)):
                self.nextToken()

                if (self.token[token] == ')'):
                    return True

        return False
