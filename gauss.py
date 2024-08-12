


matriz = [[1, 4, 5, 6], [2, 5, 7, 9], [1, 3, 8, 6]]


for k in range(len(matriz)):
    pivor= float(matriz[0][0])
    if k > 0:
        for i in range(len(matriz[k])):
            multiplicador = matriz[k][0] / pivor
            elemento = matriz[k][i] - (pivor * (multiplicador))
            matriz[k][i] = elemento

print(matriz)

for k in range(len(matriz)):
    pivor = float(matriz[1][1])
    if k > 1:
        for i in range(len(matriz[k])):
            if i > 0:
                multiplicador = matriz[k][1] / pivor
                elemento = matriz[k][i] - pivor * (multiplicador)
                matriz[k][i] = elemento
print(matriz)
