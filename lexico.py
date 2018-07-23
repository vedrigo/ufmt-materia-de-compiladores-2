import re
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


class Lexico(object):

    coluna = 0
    linha = 1
    lista_de_tokens = list()
    p_reservadas = list()

    def __init__(self, arquivo):
        self.p_reservadas = self.archiveToList("p_reservadas.txt")
        self.arquivo_fonte = open(arquivo, 'r')
        self.caracter = self.arquivo_fonte.read(1)

        if self.caracter == "":
            print("Arquivo fonte vazio.")
        else:
            while True:
                #print("Loop principal...")
                if self.caracter == "":
                    #print("fim de arquivo")
                    break
                # Letra
                elif re.match("[a-z]|[A-Z]", self.caracter) is not None:
                    self.q1()
                # Digito
                elif re.match("\d", self.caracter) is not None:
                    self.q2()
                # Comentário barra ou divisão
                elif re.match("\/", self.caracter) is not None:
                    self.q3()
                # Comentário chaves
                elif self.caracter == '{':
                    self.q4()
                # Fim do programa
                elif re.match("\.", self.caracter):
                    self.q5()
                # Espaços e tabulações
                elif self.caracter in [' ', '\t']:
                    self.q7()
                # Quebra de linhas
                elif self.caracter == '\n':
                    self.q8()
                # Simbolos
                elif re.match("\(|\)|\*|\+|\-|\:|\<|\>|\,|\w|\=|\;", self.caracter) is not None:
                    self.q9()
                # Fim de Bloco
                elif self.caracter == '$':
                    self.q10()
                # erro
                else:
                    self.q6()

        print("\n####LEXICO COM SUCESSO!!!#####\n")
        print('Lista de Tokens:')
        for x in range(len(self.lista_de_tokens)):
            print(x, ":", self.lista_de_tokens[x])

    # Transforma as linhas de um arquivo em uma lista
    def archiveToList(self, path):
        #print("função archiveToList")
        fonte = open(path, 'r')
        lista = fonte.readlines()
        for i in range(len(lista)):
            lista[i] = lista[i].replace('\n', '')
        return lista

    # Erro Função Principal
    def error(self, text):
        print(bcolors.FAIL, "\n*****ERRO NA LINHA", self.linha, "COLUNA", self.coluna, "*****")
        print(text, bcolors.ENDC)
        sys.exit()

    # Atenção
    def warning(self, text):
        '''Imprime os alertas'''
        print(bcolors.WARNING, text, bcolors.ENDC)

    # Letra
    def q1(self):
        '''Letra'''
        #print("função q1")
        token = self.caracter
        while True:
            self.caracter = self.arquivo_fonte.read(1)
            self.coluna += 1
            if re.match("[a-z]|[A-Z]|[0-9]", self.caracter) is not None:
                token += self.caracter
            elif "caracter in alfabeto":
                if token in self.p_reservadas:
                    self.lista_de_tokens.append([token, self.linha, self.coluna, "Palavra Reservada"])
                else:
                    self.lista_de_tokens.append([token, self.linha, self.coluna, "Identificador"])
                break
            else:
                self.error()

    # Digito
    def q2(self):
        '''Digito'''
        #print("função q2")
        token = self.caracter
        flag = False
        flag2 = False
        while True:
            self.caracter = self.arquivo_fonte.read(1)
            self.coluna += 1
            if re.match("\d", self.caracter) is not None:
                token += self.caracter
                if flag is True:
                    flag2 = True
            elif re.match("\.", self.caracter) is not None and flag is False:
                flag = True
                token += self.caracter
            elif flag is True and flag2 is True:
                self.lista_de_tokens.append([token, self.linha, self.coluna, "Numero de ponto flutuante"])
                break
            elif flag is False:
                self.lista_de_tokens.append([token, self.linha, self.coluna, "Numero inteiro"])
                break
            elif flag is True and flag2 is False:
                self.error("Esperado um digito")
            else:
                self.error()

    # Comentário barra ou divisão
    def q3(self):
        '''Descrição: Comentário barra ou divisão'''
        #print("função q3")
        token = ''
        token += self.caracter
        self.caracter = self.arquivo_fonte.read(1)
        self.coluna += 1
        if re.match("\*", self.caracter) is not None:
            while True:
                token += self.caracter
                self.caracter = self.arquivo_fonte.read(1)
                self.coluna += 1
                if self.caracter == '\n':
                    self.q8()
                elif self.caracter == '*':
                    token += self.caracter
                    self.caracter = self.arquivo_fonte.read(1)
                    self.coluna += 1
                    if self.caracter == '/':
                        token += self.caracter
                        self.caracter = self.arquivo_fonte.read(1)
                        self.coluna += 1
                        break
                elif self.caracter == '':
                    self.error('Esperado o simbolo */ de fechamento de comentário')
            self.lista_de_tokens.append([token, self.linha, self.coluna, "Comentário"])
        elif re.match("[a-z]|[A-Z]|[0-9]", self.caracter) is not None:
            self.lista_de_tokens.append([token, self.linha, self.coluna, "Simbolo de divisão"])
        else:
            self.error('Esperado ou o simbolo de * de comentário ou um numeral ou um identificador')

    # Comentário chaves
    def q4(self):
        '''Comentário chaves'''
        #print("função q4")
        token = ''
        while True:
            token += self.caracter
            self.caracter = self.arquivo_fonte.read(1)
            self.coluna += 1
            if self.caracter == '}':
                token += self.caracter
                self.caracter = self.arquivo_fonte.read(1)
                self.coluna += 1
                break
            elif self.caracter == '\n':
                self.q8()
            elif self.caracter == '':
                self.error('Esperado o simbolo fechamento de comentário }')
        self.lista_de_tokens.append([token, self.linha, self.coluna, "Comentário"])

    # Fim do Programa
    def q5(self):
        '''Fim do Programa'''
        #print("função q5")
        self.caracter = self.arquivo_fonte.read(1)
        self.coluna += 1
        if self.caracter != '':
            self.warning('Foi encontrado caracteres depois do fim do programa')

        self.lista_de_tokens.append(['.', self.linha, self.coluna, "Palavra Reservada"])

    # Erro simbolo inexistente
    def q6(self):
        self.error('Simbolo não existe na linguagem')

    # Espaços e tabulações
    def q7(self):
        #print("função q7")
        while self.caracter in [' ', '\t']:
            self.caracter = self.arquivo_fonte.read(1)
            self.coluna += 1

    # Quebra de linhas
    def q8(self):
        #print("função q8")
        self.coluna = 1
        while self.caracter == '\n':
            self.caracter = self.arquivo_fonte.read(1)
            self.linha += 1

    # Simbolos
    def q9(self):
        token = ''
        #print("função q9")
        token += self.caracter
        self.caracter = self.arquivo_fonte.read(1)
        self.coluna += 1
        if self.caracter == '=' or self.caracter == '>':
            token += self.caracter
            self.caracter = self.arquivo_fonte.read(1)
            self.coluna += 1
            self.lista_de_tokens.append([token, self.linha, self.coluna, "Simbolo duplo"])
        else:
            self.lista_de_tokens.append([token, self.linha, self.coluna, "Simbolo simples"])

    # Fim do Bloco
    def q10(self):
        '''Fim do Bloco'''
        #print("função q10")
        self.lista_de_tokens.append([self.caracter, self.linha, self.coluna, "Fim de Bloco"])
        self.caracter = self.arquivo_fonte.read(1)
        self.coluna += 1
