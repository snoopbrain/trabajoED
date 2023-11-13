from collections import deque

def calcular_chismorreo(personas, fuente):
    grafo = {i: set(amigos) for i, amigos in enumerate(personas)}

    # Usaremos un conjunto para rastrear las personas que escuchan el chisme en cada día
    personas_que_escuchan = set([fuente])
    
    dia = 0
    radio_maximo_chismorreo = 0

    while personas_que_escuchan:
        dia += 1
        nuevos_escuchas = set()

        for persona in personas_que_escuchan:
            # Expandir a los amigos no visitados
            for amigo in grafo[persona]:
                if amigo not in personas_que_escuchan and amigo not in nuevos_escuchas:
                    nuevos_escuchas.add(amigo)

        # Verificar si el conjunto de nuevos escuchas es mayor que el radio máximo actual
        if len(nuevos_escuchas) > radio_maximo_chismorreo:
            radio_maximo_chismorreo = len(nuevos_escuchas)

        # Actualizar el conjunto de personas que escuchan
        personas_que_escuchan = nuevos_escuchas

    return dia, radio_maximo_chismorreo

def main():
    P = int(input())
    personas = [list(map(int, input().split())) for _ in range(P)]
    
    # T = int(input())
    fuentes = list(map(int, input().split()))

    for fuente in fuentes:
        dia, radio = calcular_chismorreo(personas, fuente)
        print(f'{dia} {radio}' if radio > 0 else '0')

if __name__ == "__main__":
    main()
