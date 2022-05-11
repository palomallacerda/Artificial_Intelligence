
# Solução para o problema dos missionarios e canibais para a disciplina de IA (UFAL);
# Problema foi solucionado usando busca em largura; 
# miss_left -> qtd de missionarios a esquerda
# miss_rigth -> quantidade de missionarios a direita
# can_left -> quantidade de canibais a esquerda
# can_rigth -> quantidade de canibais a direita

class Estado():
    # função responsável por inicializar os dados necessários
    def __init__(self, miss_left, miss_rigth, can_left, can_rigth, river_side):
        self.miss_left = miss_left
        self.miss_rigth = miss_rigth
        self.can_left = can_left
        self.can_rigth = can_rigth
        self.river_side = river_side
        self.pai = None
        self.filhos = []

    # Retornando uma string com os estados setados
    def __str__(self):
        return 'Missionarios: {}\t|| Missionarios: {}\nCanibais: {}\t|| Canibais: {}'.format(
            self.miss_left, self.miss_rigth, self.can_left, self.can_rigth
        )
        
    #Função responsável por definir todos os estados válidos
    def estado_valido(self):
        ############### ESTADOS QUE NÂO SÂO VÁLIDOS ###############################
        if ((self.miss_left < 0) or (self.miss_rigth < 0) or (self.can_left < 0) or (self.can_rigth < 0)): # Não se pode gerar estados onde o número de pessoas do rio seja menor que zero
            return False

        return ((self.miss_left == 0 or self.miss_left >= self.can_left) and  (self.miss_rigth == 0 or self.miss_rigth >= self.can_rigth)) # O número de missionários não pode ser inferior ao número de canibais. 

    # Verificando se todos os canibais e missionarios atravessaram o rio 
    def estado_final(self):
        left_result = self.miss_left == self.can_left == 0
        rigth_result = self.miss_rigth == self.can_rigth == 3
        return left_result and rigth_result

    def gerar_filhos(self):
        # Encontra o novo lado do rio
        novo_river_side = 'rigth' if self.river_side == 'left' else 'left'
        
        # Gerando a lista de movimentos disponiveis
        movimentos = [
            {'missionarios': 2, 'canibais': 0},
            {'missionarios': 1, 'canibais': 0},
            {'missionarios': 1, 'canibais': 1},
            {'missionarios': 0, 'canibais': 1},
            {'missionarios': 0, 'canibais': 2},
        ]
        for movimento in movimentos:
            if self.river_side == 'left':
                # Se o barco estiver a esquerda do rio -> os missionários e canibais saem da margem esquerda do rio e vão para a direita
                miss_left = self.miss_left - movimento['missionarios']
                miss_rigth = self.miss_rigth + movimento['missionarios']
                can_left = self.can_left - movimento['canibais']
                can_rigth = self.can_rigth + movimento['canibais']
            else:
                # Caso contrário os missionários e canibais saem da margem direita do rio e vão para a esquerda
                miss_rigth = self.miss_rigth - movimento['missionarios']
                miss_left = self.miss_left + movimento['missionarios']
                can_rigth = self.can_rigth - movimento['canibais']
                can_left = self.can_left + movimento['canibais']
            
            # Cria o estado do filho e caso este seja válido, o adiciona à lista de filhos do pai
            filho = Estado(miss_left, miss_rigth, can_left, can_rigth, novo_river_side)
            filho.pai = self
            if filho.estado_valido():
                self.filhos.append(filho)

# Gerando uma árvore de estados 
class Missionarios_Canibais():
    # Insere a raiz na fila de execução, que será utilizada para fazer uma busca em largura
    def __init__(self):
        self.fila_execucao = [Estado(3, 0, 3, 0, 'left')]
        self.solucao = None

    def gerar_solucao(self):
        #Solução encontrada usando o algoritimo de busca em largura, por meio de filas que vão ser executada
        for elemento in self.fila_execucao:
            if elemento.estado_final():
                self.solucao = [elemento]
                while elemento.pai:
                    self.solucao.insert(0, elemento.pai)
                    elemento = elemento.pai
                break;
            # Caso o elemento não seja a solução, gera seus filhos e os adiciona na fila de execução
            elemento.gerar_filhos()
            self.fila_execucao.extend(elemento.filhos)

def main():
    problema = Missionarios_Canibais()
    problema.gerar_solucao()

    for estado in problema.solucao:
        print (estado)
        print (34 * '*')

if __name__ == '__main__':
    main()