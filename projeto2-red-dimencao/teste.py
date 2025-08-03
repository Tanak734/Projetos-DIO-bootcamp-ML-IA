def rgb_para_cinza(r, g, b):
    # Fórmula comum para converter RGB para tons de cinza
    return int(0.299 * r + 0.587 * g + 0.114 * b)

def inverter_para_binario(valor_cinza, threshold=128):
    # Se valor acima do limiar, branco (255), senão preto (0)
    return 255 if valor_cinza >= threshold else 0

def ppm_para_preto_branco_binario(entrada, saida):
    with open(entrada, 'r') as f:
        linhas = f.readlines()

    dados = []
    for linha in linhas:
        linha = linha.strip()
        if linha == '' or linha.startswith('#'):
            continue
        dados.extend(linha.split())

    tipo = dados.pop(0)
    largura = int(dados.pop(0))
    altura = int(dados.pop(0))
    max_valor = int(dados.pop(0))

    pixels = list(map(int, dados))
    resultado = []

    for i in range(0, len(pixels), 3):
        r = pixels[i]
        g = pixels[i + 1]
        b = pixels[i + 2]

        # 1. Converter para tons de cinza
        cinza = rgb_para_cinza(r, g, b)

        # 2. Converter para preto ou branco
        binario = inverter_para_binario(cinza)

        # 3. Como é imagem binária, todos os canais R=G=B
        resultado.extend([binario, binario, binario])

    # Escreve o novo arquivo PPM
    with open(saida, 'w') as f:
        f.write(f"{tipo}\n")
        f.write(f"{largura} {altura}\n")
        f.write(f"{max_valor}\n")

        for i in range(0, len(resultado), 3):
            r, g, b = resultado[i], resultado[i + 1], resultado[i + 2]
            f.write(f"{r} {g} {b}\n")