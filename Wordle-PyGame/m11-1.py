def calcular_numero_paulina(I, parejas):
    grafo = {i: set() for i in range(I)}
    for pareja in parejas:
        grafo[pareja[0]].add(pareja[1])
        grafo[pareja[1]].add(pareja[0])

    numero_paulina = {i: float('INF') for i in range(1, I)}
    numero_paulina[0] = 0

    cola = [0]
    visitados = set()

    while cola:
        persona = cola.pop(0)
        for vecino in grafo[persona]:
            if numero_paulina[vecino] == float('INF'):
                numero_paulina[vecino] = numero_paulina[persona] + 1
                cola.append(vecino)

    return numero_paulina


def main():
    casos = int(input())
    for caso in range(1, casos + 1):
        I, B = map(int, input().split(","))
        parejas = [tuple(map(int, input().split())) for _ in range(B)]

        numero_paulina = calcular_numero_paulina(I, parejas)

        print(f'fiesta {caso}:')
        for persona in range(1, I):
            print(f'{persona} {"INF" if numero_paulina[persona] == float("inf") else numero_paulina[persona]}')

        if caso < casos:
            print()


if __name__ == "__main__":
    main()
