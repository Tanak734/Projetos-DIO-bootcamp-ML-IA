import numpy as np
import secrets
random = secrets.SystemRandom()
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#--------criando a matriz-------------
num_classificadores = 100  # Quantidade de classificadores a simular
pontos = []  # Armazenará (tfp, tvp) para cada classificador


for _ in range(num_classificadores):
    # Gera uma matriz de confusão 2x2 com valores aleatórios
    matriz = np.zeros((2, 2))
    
    # Preenche a matriz com valores realistas
    for i in range(2):
        for j in range(2):
            if i == j:  # Elementos da diagonal (VP e VN)
                # matriz[i, j] = random.uniform(0.7, 1.0)
                matriz[i, j] = random.random()
            else:       # Elementos fora da diagonal (FP e FN)
                # matriz[i, j] = random.uniform(0, 0.5)
                matriz[i, j] = random.random()

    #Calculos
    VP = matriz[0, 0]
    FP = matriz[0, 1]
    FN = matriz[1, 0]
    VN = matriz[1, 1]

    sens = VP/(VP+FN)
    esp = VN/(FP+VN)
    acc = (VP + VN)/(VP + FN + FP + VN)
    p = VP/VP+FP
    f_score = 2 * (p * sens)/(p + sens)
    
    tvp = sens # tvp
    tfp = (1 - esp) # tfp

    pontos.append((tfp, sens))

tfp_vals, tvp_vals = zip(*pontos)

#-----------analisador-grafico----------

plt.figure(figsize=(10, 8))

# 1. Pontos dos classificadores
plt.scatter(tfp_vals, tvp_vals, alpha=0.6, label='Classificadores')

# 2. Classificador perfeito (ponto ideal)
plt.scatter(0, 1, s=150, color='green', marker='*', label='Classificador Perfeito')

# 3. Linha do classificador aleatório (diagonal)
plt.plot([0, 1], [0, 1], 'r--', label='Classificador Aleatório')

# 4. Destaque para pontos específicos mencionados na imagem
plt.scatter(0.0, 0.8, s=100, color='purple', marker='s', label='Ponto Destacado (0.0, 0.8)')

# Configurações do gráfico
plt.title('Espaço ROC - Análise de Classificadores', fontsize=15)
plt.xlabel('Taxa de Falsos Positivos (TFP)', fontsize=12)
plt.ylabel('Taxa de Verdadeiros Positivos (TVP)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='lower right')
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])

# Áreas de desempenho
plt.gca().add_patch(patches.Rectangle((0, 0.8), 0.2, 0.2, alpha=0.1, color='green', label='Bom desempenho'))
plt.text(0.1, 0.9, 'Bons Classificadores', ha='center')

plt.tight_layout()
plt.show()