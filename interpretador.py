from copy import copy
from debug import debug


class Interpretador:

    def __init__(self, codigo_inter):
        self.codigo_inter = codigo_inter
        self.pilha = []
        self.executar()

    def executar(self):

        i = 0
        debug("\nSequencia de Intruções:")
        while i < len(self.codigo_inter):
            instr = self.codigo_inter[i]
            debug(instr)
            if("CRCT" in instr):
                #carrega constante k no topo da pilha D
                self.pilha.append(float(instr.split(" ")[1])) 
            elif("CRVL" in instr):
                #Carrega valor de endereço n no topo da pilha D
                self.pilha.append(self.pilha[int(instr.split(" ")[1])])
            elif("SOMA" in instr):
                #soma o elemento antecessor com o topo da pilha; desempilha os dois e empilha o resultado
                self.pilha.append(self.pilha.pop() + self.pilha.pop())
            elif("SUBT" in instr):
                #subtrai o antecessor pelo elemento do topo
                self.pilha.append(- self.pilha.pop() + self.pilha.pop())
            elif("MULT" in instr):
                #multiplica elemento antecessor pelo elemento do topo
                self.pilha.append(self.pilha.pop() * self.pilha.pop())
            elif("DIVI" in instr):
                #divide o elemento antecessor pelo elemento do topo
                denominador = self.pilha.pop()
                self.pilha.append(self.pilha.pop() / denominador)
            elif("INVE" in instr):
                #inverte sinal do topo
                self.pilha.append(- self.pilha.pop())
            elif("CONJ" in instr):
                #conjunção de valores lógicos. F=0; V=1
                self.pilha.append(1 if self.pilha.pop() == 1 and self.pilha.pop() == 1 else 0)
            elif("DISJ" in instr):
                #disjunção de valores lógicos
                self.pilha.append(1 if self.pilha.pop() == 1 or self.pilha.pop() == 1 else 0)
            elif("NEGA" in instr):
                #negação lógica
                self.pilha.append(1 - self.pilha.pop())
            elif("CPME" in instr):
                #comparação de menor entre o antecessor e o topo
                topo = self.pilha.pop()
                self.pilha.append(1 if self.pilha.pop() < topo else 0)
            elif("CPMA" in instr):
                #comparação de maior
                topo = self.pilha.pop()
                self.pilha.append(1 if self.pilha.pop() > topo else 0)
            elif("CPIG" in instr):
                #comparação de igualdade
                self.pilha.append(1 if self.pilha.pop() == self.pilha.pop() else 0)
            elif("CDES" in instr):
                #comparação de desigualdade
                self.pilha.append(1 if self.pilha.pop() != self.pilha.pop() else 0)
            elif("CPMI" in instr):
                #{comparação menor-igual
                topo = self.pilha.pop()
                self.pilha.append(1 if self.pilha.pop() <= topo else 0)
            elif("CMAI" in instr):
                #comparação maior-igual
                topo = self.pilha.pop()
                self.pilha.append(1 if self.pilha.pop() >= topo else 0)
            elif("ARMZ" in instr):
                #armazena o topo da pilha no endereço n de D
                self.pilha[int(instr.split(" ")[1])] = self.pilha.pop()
            elif("DSVI" in instr):
                #desvio incondicional para a instrução de endereço p
                i = int(instr.split(" ")[1])
                continue
            elif("DSVF" in instr):
                #{desvio condicional para a instrução de endereço p; 
                # o desvio será executado caso a condição resultante 
                # seja falsa; o valor dacondição estará no topo
                if self.pilha.pop() == 0:
                    i = int(instr.split(" ")[1])
                    continue
            elif("LEIT" in instr):
                #lê um dado de entrada para o topo da pilha
                self.pilha.append(float(input("Entre com um valor: ")))
            elif("IMPR" in instr):
                #imprime valor o valor do topo da pilha na saída
                print("Saída: ", self.pilha.pop())
            elif("ALME" in instr):
                #reserva m posições na pilha D; m depende do tipo da variável
                for j in range(0, int(instr.split(" ")[1])):
                    self.pilha.append("ReservaDeMemmoria")
            elif("PARAM" in instr):
                #aloca memória e copia valor da posição n para o topo de D
                self.pilha.append(copy(self.pilha[int(instr.split(" ")[1])]))
            elif("PUSHER" in instr):
                #empilha o índice e da instrução seguinte à chamada do 
                #procedimento, como endereço de retorno, no array C
                self.pilha.append(instr.split(" ")[1])
            elif("CHPR" in instr):
                #desvia para instrução de índice p no array C, obtido na TS
                i = int(instr.split(" ")[1])
                continue
            elif("DESM" in instr):
                #desaloca m posições de memória, a partir do topo s de D
                for j in range(0, int(instr.split(" ")[1])):
                    self.pilha.pop()
            elif("RTPR" in instr):
                #retorna do procedimento – endereço de retorno estará no topo
                #de D – e desempilha o endereço
                i = int(self.pilha.pop())
                continue
            elif("INPP" in instr):
                #inicia programa – será sempre a 1ª instrução
                pass
            elif("PARA" in instr):
                #termina a execução do programa
                print("\n########INTERPRETADOR COM SUCESSO!!!##########")

                return True
            else:
                exit("Erro, comando inesperado!\n Comando: " + instr)
            i += 1
