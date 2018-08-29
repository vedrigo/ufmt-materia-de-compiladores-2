class Interpretador:

    def __init__(self, codigo_inter):
        self.codigo_inter = codigo_inter
        self.pilha = []
        self.executar()

    def executar(self):
        self.codigo_inter.reverse()
        for i in range(len(self.codigo_inter)):
            instr = self.codigo_inter.pop()
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
                pass
            elif("DSVI" in instr):
                #desvio incondicional para a instrução de endereço p
                pass
            elif("DSVF" in instr):
                #{desvio condicional para a instrução de endereço p; 
                # o desvio será executado caso a condição resultante 
                # seja falsa; o valor dacondição estará no topo
                pass
            elif("LEIT" in instr):
                #lê um dado de entrada para o topo da pilha
                pass
            elif("IMPR" in instr):
                #imprime valor o valor do topo da pilha na saída
                pass
            elif("ALME" in instr):
                #reserva m posições na pilha D; m depende do tipo da variável
                pass
            elif("PARAM" in instr):
                #aloca memória e copia valor da posição n para o topo de D
                pass
            elif("PUSHER" in instr):
                #empilha o índice e da instrução seguinte à chamada do 
                #procedimento, como endereço de retorno, no array C
                pass
            elif("CHPR" in instr):
                #desvia para instrução de índice p no array C, obtido na TS
                pass
            elif("DESM" in instr):
                #desaloca m posições de memória, a partir do topo s de D
                pass
            elif("RTPR" in instr):
                #retorna do procedimento – endereço de retorno estará no topo
                #de D – e desempilha o endereço
                pass
            elif("INPP" in instr):
                #inicia programa – será sempre a 1ª instrução
                pass
            elif("PARA" in instr):
                #termina a execução do programa
                pass
            else:
                exit("Erro, comando inesperado!\n Comando: " + instr)

        print("\n########INTERPRETADOR COM SUCESSO!!!##########")
        print("\nPilha:")
        for i in range(len(self.pilha)):
            print(self.pilha[i])
