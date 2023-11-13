def calcular_area_deforestada(A, B, bosque_mapa):
    def dfs(fila, columna):
        if fila < 0 or fila >= A or columna < 0 or columna >= B or bosque_mapa[fila][columna] == '.':
            return 0
        bosque_mapa[fila][columna] = '.'
        tamaño = 1
        tamaño += dfs(fila + 1, columna)
        tamaño += dfs(fila - 1, columna)
        tamaño += dfs(fila, columna + 1)
        tamaño += dfs(fila, columna - 1)
        return tamaño

    max_area = 0

    for i in range(A):
        for j in range(B):
            if bosque_mapa[i][j] == 'X':
                area = dfs(i, j)
                max_area = max(max_area, area)

    return max_area


def main():
    C = int(input())

    for _ in range(C):
        A, B = map(int, input().split())
        bosque_mapa = [list(input().strip()) for _ in range(A)]

        resultado = calcular_area_deforestada(A, B, bosque_mapa)
        print(resultado)


if __name__ == "__main__":
    main()
