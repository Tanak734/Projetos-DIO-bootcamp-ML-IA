def soma(a, b):
    """
    Retorna a soma de dois números
    """
    return a + b

def subtracao(a, b):
    """
    Retorna a subtração de dois números
    """
    return a - b

def divisao(a, b):
    """
    Retorna a divisão de dois números
    Levanta ValueError se b for zero
    """
    if b == 0:
        raise ValueError("Divisão por zero não é permitida")
    return a / b

def eh_par(numero):
    """
    Verifica se um número é par
    """
    return numero % 2 == 0