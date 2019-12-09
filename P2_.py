import math
import random
from collections import Counter

#Classe Pessoa
class Pessoa:
    def __init__(self, idade, sexo, salario, intencao_de_voto):
        self.idade = idade
        self.sexo = sexo
        self.salario = salario
        self.intencao_de_voto = intencao_de_voto
    def __str__(self):
        return f'idade: {self.idade}, sexo: {self.sexo}, salario: {self.salario}, intencao_de_voto: {self.intencao_de_voto}'
    def __eq__(self, other):
        return self.intencao_de_voto == other.intencao_de_voto
    def __hash__(self):
        return 1

#Base de Pessoas sem voto
def gera_base_sem_voto (n):
    l = []
    for _ in range (n):
        idade = random.randint(16, 70)
        sexo = random.choice(['M', 'F'])
        salario = 1200 + random.random() * 5000 + random.random() * 2500
        intencao_de_voto = None
        p = Pessoa (idade, sexo, salario, intencao_de_voto)
        l.append(p)
    return l

#Inserir intenção de voto em cada Pessoa
def gera_base_com_voto(lista_sem_voto):
    for pessoa in lista_sem_voto:
        intencao_pela_idade(pessoa)
    return lista_sem_voto # agora com voto

#Base final com intenção de voto
def gera_base(n):
    base_pessoas = gera_base_com_voto(gera_base_sem_voto(n))
    return base_pessoas

#-------------------------------Intenção de Voto-------------------------------------
#Verificar intenção de voto por idade independente de outros atributos
def intencao_pela_idade(p):
    if p.idade <= 22:
        intencao = random.random()
        if intencao <= 0.92:
            #Voto para o Haddad
            p.intencao_de_voto = 'H'
        else:
            #sendo mais velho ou não fazer parte dos 92%
            #Voto para o Bolsonaro
            p.intencao_de_voto = 'B'
    else:
        intencao_pelo_salario(p)
#Verificar intenção de voto por salario após verificar idade
def intencao_pelo_salario(p):
    if p.salario >= 5000:
        intencao = random.random()
        if intencao <= 0.55:
            #Voto para Bolsonaro
            p.intencao_de_voto = 'B'
        else:
            #Tendo um salario inferior ou não fazer parte dos 55%
            p.intencao_de_voto = 'H'
    else:
        intencao_pelo_sexo(p)
#Verificar intenção de voto pelo sexo da pessoa após cerificar salário e idade
def intencao_pelo_sexo(p):
    if p.sexo == 'F':
        intencao = random.random()
        if intencao <= 0.80:
            #Voto Haddad
            p.intencao_de_voto = 'H'
        else:
            #Não fazendo parte dos 80%
            p.intencao_de_voto = 'B'
    else:
        #Sendo Homem
        intencao = random.random()
        if intencao <= 0.85:
            p.intencao_de_voto = 'B'
        else:
            #não fazendo parte dos 85%
            p.intencao_de_voto = 'H'

#Teste - Base de Pessoas
def teste_base_gerada(n):
    #Base de Pessoas
    lista = gera_base(n)
    for p in lista:
        print(p)
    print(f'----'*15)

#-------------------------- KMEANS -----------------------------
def scalar_multiply(escalar, vetor):
    return [escalar * i for i in vetor]

def vector_sum(vetores):
    resultado = vetores[0]
    for vetor in vetores[1:]:
        resultado = [resultado[i] + vetor[i] for i in range(len(vetor))]
    return resultado

def vector_mean(vetores):
    return scalar_multiply(1/len(vetores), vector_sum(vetores))

def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def vector_subtract(v, w):
    return [v_i - w_i for v_i, w_i in zip(v, w)]

def sum_of_squares(v):
    return dot(v, v)

def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))

def distance (v, w):
    return math.sqrt(squared_distance(v, w))

class KMeans:
    def __init__(self, k, means=None):
        self.k = k
        self.means = means
    def classify (self, ponto):
        return min (range (self.k), key = lambda i: distance(ponto, self.means[i]))
    def train (self, pontos):
        self.means = random.sample(pontos, self.k) if self.means == None else self.means
        assignments = None
        while True:
            new_assignments = list(map (self.classify, pontos))
            if new_assignments == assignments:
                return
            assignments = new_assignments
            for i in range (self.k):
                i_points = [p for p, a in zip (pontos, assignments) if a == i]
                if i_points:
                    self.means[i] = vector_mean (i_points)
#class Kmeans
#-------------------------------------------------------------------

#Tornar centroides em classe 'Pessoa'
def meansClasse(means):
    lista_means = []
    for mean in means:
        p = Pessoa(mean[0], mean[1], mean[2], mean[3])
        lista_means.append(p)
    return lista_means

#------------------Converter dados de Pessoa para números------------
#Cria uma cópia da base original mas cada Pessoa se torna um vetor
def base_pessoas_convertida_inteiros(base):
    lista = []
    for p in base:
        #Altera dados na base original
        #'F' = 70; 'M' = 77 
        p.sexo = ord(p.sexo)
        #'B' = 66; 'H' = 72
        p.intencao_de_voto = ord(p.intencao_de_voto)
        lista.append([p.idade, p.sexo, p.salario, p.intencao_de_voto])
    return lista

#Teste gerar pontos médios com relação à base
def teste_KMeans(n):
    lista = gera_base(n)
    lista_convertida = base_pessoas_convertida_inteiros(lista)
    print('-------Lista de Pessoas-------')
    for p in lista_convertida:
        print(p)
    print(f'----'*10)
    #KMeans retornando pontos médios
    kmeans = KMeans(3)
    kmeans.train(lista_convertida)
    print(kmeans.means)

#------------------------- Criar Grupos e dividir Pessoas --------------------------
#Distancia entre uma pessoa e cada um dos centroides
def lista_distancias(pessoa, means):
    distancias = []
    for ponto_medio in means:
        distancias.append(distance(pessoa, ponto_medio))
    return distancias

def agruparPessoas (base, means): #base_convertida, kmeans.means
    g1 = []
    g2 = []
    g3 = []
    for p in base:
        distancias = lista_distancias(p, means)
        #mais proximo do primeiro ponto médio
        if distancias[0] <= distancias[1] and distancias[0] <= distancias[2] and len(g1) < len(base)/3:
            g1.append(p)
        #mais proximo do segundo ponto médio
        elif distancias[1] <= distancias[0] and distancias[1] <= distancias[2] and len(g2) < len(base)/3:
            g2.append(p)
        #mais proximo do terceiro ponto médio
        elif distancias[2] <= distancias[0] and distancias[2] <= distancias[1] and len(g3) < len(base)/3:
            g3.append(p)
    return (g1, g2, g3)

# --------------------- Reconstruindo a Base Original de cada Grupos ---------------------
#Usar a base original para
def base_pessoas_convertida_caracter(base_alterada, base_original):
    new_base = []
    for i in base_alterada:
        for p in base_original:
            if (i[0] == p.idade and i[2] == p.salario):
                #Altera dados na base original
                #'F' = 70; 'M' = 77 
                p.sexo = chr(p.sexo)
                #'B' = 66; 'H' = 72
                p.intencao_de_voto = chr(p.intencao_de_voto)
                new_base.append(p)
    return new_base

#Teste Pessoas separadas em cada grupo
def teste_criar_grupos(n):
    lista = gera_base(n)
    lista_convertida = base_pessoas_convertida_inteiros(lista)
    #KMeans retornando pontos médios
    kmeans = KMeans(3)
    kmeans.train(lista_convertida)
    l1,l2,l3 = agruparPessoas (lista_convertida, kmeans.means)
    l1 = base_pessoas_convertida_caracter(l1, lista)
    print ('Grupo 1')
    for i in l1:
        print (i)
    l2 = base_pessoas_convertida_caracter(l2, lista)
    print ('Grupo 2')
    for i in l2:
        print (i)
    l3 = base_pessoas_convertida_caracter(l3, lista)
    print ('Grupo 3')
    for i in l3:
        print (i)

#---------------------- KNN --------------------------------
#Distancia lida com classe pessoa
def distancia(p1, p2):
    i = math.pow((p1.idade - p2.idade), 2)
    s = math.pow((1 if p1.sexo == 'M' else 0) - (1 if p2.sexo == 'M' else 0), 2)
    sal = math.pow((p1.salario - p2.salario), 2)
    return math.sqrt(i + s + sal)

def rotulo_de_maior_frequencia_sem_empate(pessoas):
    frequencias = Counter(pessoas)
    rotulo, frequencia = frequencias.most_common(1)[0]
    qtde_mais_frequentes = len([
        count
        for count in frequencias.values()
        if count == frequencia
    ])
    if qtde_mais_frequentes == 1:
        return rotulo
    return rotulo_de_maior_frequencia_sem_empate(pessoas[:-1])

def knn(k, observacoes_rotuladas, nova_observacao):
    ordenados_por_distancia = sorted(
        observacoes_rotuladas, key=lambda obs: distancia(obs, nova_observacao))
    k_mais_proximo = ordenados_por_distancia[:k]
    resultado = rotulo_de_maior_frequencia_sem_empate(k_mais_proximo)
    return resultado.intencao_de_voto

def teste_knn(n):
    base = gera_base(n)
    lista_convertida = base_pessoas_convertida_inteiros(base)
    kmeans = KMeans(3)
    kmeans.train(lista_convertida)
    #agrupar 'Pessoa' e tornar means em Classes
    l1,l2,l3 = agruparPessoas (lista_convertida, kmeans.means)
    lista_means = meansClasse(kmeans.means)
    #Uso de cada centroide para intenção de voto do grupo
    l1 = base_pessoas_convertida_caracter(l1, base)
    print(f"Grupo 1: {knn(5, l1, lista_means[0])}.")
    l2 = base_pessoas_convertida_caracter(l2, base)
    print(f"Grupo 2: {knn(5, l2, lista_means[1])}.")
    l3 = base_pessoas_convertida_caracter(l3, base)
    print(f"Grupo 3: {knn(5, l3, lista_means[2])}.")


def main():
    n = 30
    #gerar base somente
    # teste_base_gerada(n)

    #gerar pontos médios a partir de uma base
    # teste_KMeans(n)

    #organizar lista de pessoas
    # teste_criar_grupos(n)

    #Prever intenção de voto do grupo com KNN
    teste_knn(n)

    #Cross Validation Leave One Out
main()