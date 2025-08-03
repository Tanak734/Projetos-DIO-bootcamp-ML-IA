import numpy as np
from PIL import Image
from pathlib import Path

# definindo uma constante para o caminho da imagem

CAMINHO_IMAGEM = ...


#abrindo a imagem
imagem = Image.open(CAMINHO_IMAGEM)
#--------------------------------------------------------------
## Exibindo informações da imagem
print(imagem.format) # jpeg
print(imagem.mode) # tipo de coloração (rgb, L)
print(imagem.getbands())
print(imagem.size)


#mostrando a imagem normal

# imagem.show()

#--------------------------------------------------------------
# Convetendo a imagem em tons de cinza
imagem_tc = imagem.convert('L')

# mostrando a imagem cinza


# imagem_tc.show()

#--------------------------------------------------------------
# convertendo a imagem para tons de preto e branco atravez de binarização
limiar = 130.779585 # valor do ponto medio entre o preto (0) e o branco (255)

'''
função que faz a conversão de valores 
maiores que o limiar (> 128) para branco e menores (< 128) para preto

'''
def calculo_limiar(pixel):
    return 255 if pixel >= limiar else 0

# define a função para cada pixel
imagem_binaria = imagem_tc.point(calculo_limiar)

imagem_binaria.show()
#--------------------------------------------------------------

#testes
if __name__ == '__main__':
    print(CAMINHO_IMAGEM)