'''
FEITO SEM NENHUMA BIBLIOTECA, mas nao funcionou, fiz junto com IA e fiz outro que funciona
'''

ARQUIVO_IMG = ...

with open(ARQUIVO_IMG, 'rb') as arquivo:
    # Lê tipo
    tipo = arquivo.readline().decode('ascii').strip()
    
    # Lê dimensões (pulando comentários)
    linha = arquivo.readline()
    while linha.startswith(b'#'):
        linha = arquivo.readline()
    dimensoes = linha.decode('ascii').split()
    largura, altura = int(dimensoes[0]), int(dimensoes[1])
    
    # Lê valor máximo de cor
    linha = arquivo.readline()
    while linha.startswith(b'#'):
        linha = arquivo.readline()
    max_cor = int(linha.decode('ascii').strip())
    
    # Lê todos os valores de cor restantes
    dados_restantes = arquivo.read()
    
    # Tenta decodificar usando Latin-1
    try:
        dados_str = dados_restantes.decode('latin-1')
    except:
        dados_str = dados_restantes.decode('ascii', errors='ignore')
    
    # Processa os valores
    valores = []
    for valor in dados_str.split():
        try:
            valores.append(int(valor))
        except:
            continue

print(f'tipo: {tipo} | dimensões: {largura} X {altura} | cor maxima {max_cor}')
print(f'Total de valores lidos: {len(valores)}')
print(f'Valores esperados (largura * altura * 3): {largura * altura * 3}')

#----------------------------------------------------------

print('-----------------------------------------------------------')

# Calcula o número total de pixels
total_pixels = len(valores) // 3
print(f'Total de pixels: {total_pixels}')

# Converte cada pixel para tons de cinza (fórmula mais brilhante)
pixels_cinza = []
for i in range(total_pixels):
    r = valores[i*3]
    g = valores[i*3 + 1]
    b = valores[i*3 + 2]
    
    # Fórmula mais clara para garantir visibilidade
    cinza = (r * 0.3 + g * 0.6 + b * 0.1) * 1.2  # Aumenta o brilho
    cinza = min(max_cor, max(0, int(cinza)))
    pixels_cinza.append(cinza)

print(f'Conversão completa! Primeiros 10 valores de cinza: {pixels_cinza[:10]}')
print(f'Valor médio de cinza: {sum(pixels_cinza)/len(pixels_cinza):.2f}')

#------------------------------------------------------------------------
# SALVAR IMAGEM EM TONS DE CINZA (PGM - P2)
nome_saida_cinza = "imagem_cinza.pgm"

with open(nome_saida_cinza, 'w') as f:
    # Escreve o cabeçalho
    f.write("P2\n")
    f.write(f"{largura} {altura}\n")
    f.write(f"{max_cor}\n")
    
    # Escreve os dados de pixel
    for i in range(altura):
        for j in range(largura):
            idx = i * largura + j
            if idx < len(pixels_cinza):
                f.write(f"{pixels_cinza[idx]} ")
        f.write("\n")

print(f"Imagem em tons de cinza salva como {nome_saida_cinza}")

#------------------------------------------------------------------------
# SALVAR VERSÃO ALTERNATIVA EM PPM PARA VISUALIZAÇÃO (RGB igual para cinza)
nome_saida_cinza_ppm = "imagem_cinza.ppm"
with open(nome_saida_cinza_ppm, 'w') as f:
    f.write("P3\n")
    f.write(f"{largura} {altura}\n")
    f.write(f"{max_cor}\n")
    
    for cinza in pixels_cinza:
        f.write(f"{cinza} {cinza} {cinza} ")

print(f"Versão alternativa salva como {nome_saida_cinza_ppm} (PPM)")

#------------------------------------------------------------------------
# Binarização com limiar ajustado
limiar = sum(pixels_cinza) / len(pixels_cinza)  # Usa a média como limiar
print(f'Limiar automático: {limiar:.2f}')

pixels_bin = []
for cinza in pixels_cinza:
    if cinza <= limiar:
        pixels_bin.append(0)      # Preto
    else:
        pixels_bin.append(1)      # Branco (valor 1 para PBM)

# SALVAR IMAGEM BINARIZADA (PBM - P1)
nome_saida_bin = "imagem_binaria.pbm"

with open(nome_saida_bin, 'w') as f:
    # Escreve o cabeçalho
    f.write("P1\n")
    f.write(f"{largura} {altura}\n")
    
    # Escreve os dados de pixel
    for i in range(altura):
        for j in range(largura):
            idx = i * largura + j
            if idx < len(pixels_bin):
                f.write(f"{pixels_bin[idx]} ")
        f.write("\n")

print(f"Imagem binária salva como {nome_saida_bin}")

#------------------------------------------------------------------------
# SALVAR VERSÃO VISUALIZÁVEL DA BINARIZAÇÃO (PGM)
nome_saida_bin_pgm = "imagem_binaria_vis.pgm"
with open(nome_saida_bin_pgm, 'w') as f:
    f.write("P2\n")
    f.write(f"{largura} {altura}\n")
    f.write("255\n")
    
    for valor in pixels_bin:
        cor = 0 if valor == 0 else 255
        f.write(f"{cor} ")

print(f"Versão visualizável da binária salva como {nome_saida_bin_pgm}")