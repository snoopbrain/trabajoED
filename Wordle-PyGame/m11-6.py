def min_movimientos(celda_inicio, celda_destino):
    # Convertir las letras a números de columna (A=0, B=1, ..., H=7)
    col_inicial = ord(celda_inicio[0]) - ord('A')
    # Convertir el número de fila a índice de fila (1 se resta para que el índice sea 0-based)
    fila_inicial = int(celda_inicio[1]) - 1
    col_final = ord(celda_destino[0]) - ord('A')
    fila_final = int(celda_destino[1]) - 1

    # Inicializar el tablero con ceros
    tablero = [[0] * 8 for _ in range(8)]

    # Definir los posibles movimientos del caballo
    movimientos = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    # Marcar la celda inicial con 1
    tablero[fila_inicial][col_inicial] = 1

    # Inicializar la cola con la celda inicial
    cola = [(fila_inicial, col_inicial)]

    # Realizar un recorrido en anchura (BFS)
    while cola:
        fila, col = cola.pop(0)

        # Verificar si hemos alcanzado la celda de destino
        if fila == fila_final and col == col_final:
            # Restar 1 para obtener la cantidad mínima de movimientos
            return tablero[fila][col] - 1

        # Explorar los movimientos posibles
        for movimiento in movimientos:
            nueva_fila = fila + movimiento[0]
            nueva_col = col + movimiento[1]

            # Verificar si la nueva posición está dentro del tablero y no ha sido visitada
            if 0 <= nueva_fila < 8 and 0 <= nueva_col < 8 and tablero[nueva_fila][nueva_col] == 0:
                # Marcar la nueva posición y agregarla a la cola
                tablero[nueva_fila][nueva_col] = tablero[fila][col] + 1
                cola.append((nueva_fila, nueva_col))

    # Si no se alcanza la celda de destino, retornar -1
    return -1

# Leer la cantidad de casos de prueba
C = int(input())

resultados = []

# Leer y procesar cada caso de prueba
for _ in range(C):
    inicio, destino = input().split()
    movimientos = min_movimientos(inicio, destino)
    resultados.append(movimientos)

# Imprimir los resultados
for resultado in resultados:
    print(resultado)
