import numpy as np
def eliminacao_gauss_jordan(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    for k in range(n):
        # Encontrar a linha de pivô com o valor absoluto máximo na coluna k
        linha_max = max(range(k, n), key=lambda i: abs(a[i][k]))
        # Verificar se a matriz é singular (nenhum pivô não nulo encontrado)
        if a[linha_max][k] == 0:
            raise ValueError("Matriz é singular.")
        # Trocar a linha atual com a linha de pivô
        a[[k, linha_max]] = a[[linha_max, k]]
        b[[k, linha_max]] = b[[linha_max, k]]
        # Normalizar a linha do pivô
        fator = a[k][k]
        a[k] = a[k] / fator
        b[k] = b[k] / fator
        # Eliminar todas as outras entradas na coluna k
        for i in range(n):
            if i != k:
                fator = a[i][k]
                a[i] -= fator * a[k]
                b[i] -= fator * b[k]
    return b
