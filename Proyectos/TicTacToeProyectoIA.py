# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 20:59:53 2025

@author: diego
"""

import copy
import time


'''

Manual de Usuario:
    
Para comenzar a jugar al Ultimate Tic Tac Toe, ejecuta el programa en Spyder. 
El juego te dará la bienvenida y presentará un resumen de las reglas. 
Primero, deberás elegir quién tendrá el primer turno: 
ingresa '1' para jugar tú primero o '2' para que la IA comience. 
El tablero se mostrará como una cuadrícula 9x9, donde cada celda
vacía se representa con un punto ('.'), tus movimientos con 'O',
y los de la IA con 'X'. El tablero está dividido en 9 sub-tableros de 3x3. 
Para realizar un movimiento, ingresa dos letras cuando se te solicite: 
la primera letra mayúscula (A-I) indica el sub-tablero, y la segunda 
letra minúscula (a-i) señala la posición dentro de ese sub-tablero. 
Por ejemplo, 'Aa' representa la esquina superior izquierda del sub-tablero 
superior izquierdo. Tu movimiento determinará en qué sub-tablero debe jugar 
tu oponente en el siguiente turno. Por ejemplo, si juegas en la posición 'c' 
de cualquier sub-tablero, tu oponente deberá jugar en el sub-tablero 'C' en 
su próximo turno.

El juego sigue reglas especiales: si te envían a un sub-tablero 
que ya está ganado o completamente lleno, podrás jugar en cualquier 
sub-tablero disponible. Para ganar un sub-tablero, debes conseguir
tres de tus símbolos en línea (horizontal, vertical o diagonal), 
al igual que en el Tic Tac Toe tradicional. 
El objetivo final es ganar tres sub-tableros en línea para ganar 
el juego completo. Después de cada movimiento, el programa verificará 
automáticamente si hay un ganador o si se ha producido un empate en 
algún sub-tablero o en el juego completo. La IA utilizará un algoritmo 
minimax con poda alfa-beta para tomar decisiones estratégicas. 
Siempre se mostrarán indicaciones en pantalla, que te informarán
sobre el estado del juego, de quién es el turno y si algún movimiento
es inválido.

Durante el juego, observar que se imprimen los movimientos tanto 
del usuario cómo de la IA. Si cometes un error al ingresar tu movimiento, 
el juego te pedirá que lo intentes de nuevo. El juego continuará alternando 
turnos entre el usuario y la IA hasta que haya un ganador o se produzca un 
empate en el tablero completo. En ese momento, se anunciará el resultado final.
Si deseas jugar otra partida, simplemente vuelve a ejecutar el programa.

Nota: La biblioteca copy se utiliza en este código para crear copias profundas del
tablero de juego, especialmente en la función mov_ia. Esto permite a la IA simular movimientos
en una copia del tablero sin afectar el estado real del juego, lo cual es crucial
para el algoritmo minimax. Por otro lado, la biblioteca time se emplea para medir el tiempo 
de ejecución del algoritmo de la IA. En la función mov_ia, se establece un límite de tiempo 
(10 segundos por defecto) para que la IA tome una decisión, evitando así que el juego se ralentice 
excesivamente en situaciones complejas.

'''

# Verifica si el tablero está completamente lleno (empate)
def empate(tablero):
    return all(celda != '' for ren in tablero for celda in ren)

# Verifica si hay un ganador en un tablero 3x3
def checa_ganador(jugador, tablero):
    # Verifica filas y columnas
    for i in range(3):
        if all(tablero[i][j] == jugador for j in range(3)) or all(tablero[j][i] == jugador for j in range(3)):
            return True
    # Verifica diagonales
    if all(tablero[i][i] == jugador for i in range(3)) or all(tablero[i][2-i] == jugador for i in range(3)):
        return True
    return False

# Obtiene un sub-tablero 3x3 del tablero principal 9x9
def obten_sub_tablero(tablero, ren, col):
    start_ren, start_col = 3 * (ren // 3), 3 * (col // 3)
    return [tablero[i][start_col:start_col+3] for i in range(start_ren, start_ren+3)]

# Nueva función para evaluar "proyectos"
def evaluar_proyecto(sub_tablero, jugador):
    # Checa si el jugador está a un movimiento de ganar
    for i in range(3):
        # Filas y columnas con 2 piezas del jugador y una vacía
        if sub_tablero[i].count(jugador) == 2 and sub_tablero[i].count('') == 1:
            return True
        if [sub_tablero[j][i] for j in range(3)].count(jugador) == 2 and [sub_tablero[j][i] for j in range(3)].count('') == 1:
            return True
    # Diagonales con 2 piezas del jugador y una vacía
    if [sub_tablero[i][i] for i in range(3)].count(jugador) == 2 and [sub_tablero[i][i] for i in range(3)].count('') == 1:
        return True
    if [sub_tablero[i][2-i] for i in range(3)].count(jugador) == 2 and [sub_tablero[i][2-i] for i in range(3)].count('') == 1:
        return True
    return False

# Nueva función para evaluar posiciones clave
def evaluar_posiciones_clave(sub_tablero, jugador):
    puntos = 0
    # Centro
    if sub_tablero[1][1] == jugador:
        puntos += 2
    # Esquinas
    for (x, y) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if sub_tablero[x][y] == jugador:
            puntos += 1
    return puntos



# Función de evaluación del tablero actualizada
def evaluar_tablero(tablero):
    score = 0
    for i in range(3):
        for j in range(3):
            sub_tablero = obten_sub_tablero(tablero, i*3, j*3)
            if checa_ganador('X', sub_tablero):
                score += 10  # Puntuación más alta por ganar el sub-tablero
            elif checa_ganador('O', sub_tablero):
                score -= 10
            elif evaluar_proyecto(sub_tablero, 'X'):
                score += 3  # Valor adicional por tener un "proyecto"
            elif evaluar_proyecto(sub_tablero, 'O'):
                score -= 3
            score += evaluar_posiciones_clave(sub_tablero, 'X')
            score -= evaluar_posiciones_clave(sub_tablero, 'O')
    return score

# Implementa el algoritmo minimax con poda alfa-beta
def minimax(tablero, depth, max_jugador, alpha, beta, ultimo_mov):
    if depth == 0 or empate(tablero):
        return evaluar_tablero(tablero)

    mov_validos = obtener_mov_validos(tablero, ultimo_mov)
    
    if max_jugador:
        max_eval = float('-inf')
        for move in mov_validos:
            copia_tablero = copy.deepcopy(tablero)
            update_tablero('X', move, copia_tablero)
            eval = minimax(copia_tablero, depth-1, False, alpha, beta, ('X', move[0], move[1]))
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in mov_validos:
            copia_tablero = copy.deepcopy(tablero)
            update_tablero('O', move, copia_tablero)
            eval = minimax(copia_tablero, depth-1, True, alpha, beta, ('O', move[0], move[1]))
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Actualiza el tablero con un movimiento
def update_tablero(jugador, move, tablero):
    ren, col = move
    if 0 <= ren < 9 and 0 <= col < 9 and tablero[ren][col] == '':
        tablero[ren][col] = jugador
        return True
    return False

# Verifica si un sub-tablero ha sido ganado
def sub_tablero_ganado(tablero, ren, col):
    sub_tablero = obten_sub_tablero(tablero, ren, col)
    return checa_ganador('X', sub_tablero) or checa_ganador('O', sub_tablero)

# Verifica si un sub-tablero está lleno
def sub_tablero_lleno(tablero, ren, col):
    sub_tablero = obten_sub_tablero(tablero, ren, col)
    return all(celda != '' for ren in sub_tablero for celda in ren)

# Obtiene los movimientos válidos según las reglas del juego
def obtener_mov_validos(tablero, ultimo_mov):
    if ultimo_mov is None:
        return [(i, j) for i in range(9) for j in range(9) if tablero[i][j] == '']
    
    next_sub_tablero_ren = ultimo_mov[1] % 3
    next_sub_tablero_col = ultimo_mov[2] % 3
    start_ren = 3 * next_sub_tablero_ren
    start_col = 3 * next_sub_tablero_col
    
    if sub_tablero_ganado(tablero, start_ren, start_col) or sub_tablero_lleno(tablero, start_ren, start_col):
        # Si el sub-tablero está ganado o lleno, permite jugar en cualquier sub-tablero no ganado y no lleno
        mov_validos = []
        for i in range(3):
            for j in range(3):
                sub_start_ren, sub_start_col = 3 * i, 3 * j
                if not sub_tablero_ganado(tablero, sub_start_ren, sub_start_col) and not sub_tablero_lleno(tablero, sub_start_ren, sub_start_col):
                    mov_validos.extend([(ren, col) for ren in range(sub_start_ren, sub_start_ren+3) 
                                        for col in range(sub_start_col, sub_start_col+3) if tablero[ren][col] == ''])
        return mov_validos
    else:
        return [(i, j) for i in range(start_ren, start_ren+3) for j in range(start_col, start_col+3) if tablero[i][j] == '']

# Convierte coordenadas numéricas a formato de letras
def convertir_a_letra(ren, col):
    letra_mayuscula = chr(65 + (ren // 3) * 3 + (col // 3))
    letra_minuscula = chr(97 + (ren % 3) * 3 + (col % 3))
    return f"{letra_mayuscula}{letra_minuscula}"

# Convierte formato de letras a coordenadas numéricas
def convert_from_letter_format(move):
    letra_mayuscula, letra_minuscula = move[0], move[1]
    big_ren = (ord(letra_mayuscula) - 65) // 3
    big_col = (ord(letra_mayuscula) - 65) % 3
    small_ren = (ord(letra_minuscula) - 97) // 3
    small_col = (ord(letra_minuscula) - 97) % 3
    return (big_ren * 3 + small_ren, big_col * 3 + small_col)

# Determina el mejor movimiento para la IA
def mov_ia(tablero, ultimo_mov, tiempo_limite=10):
    tiempo_inicial = time.time()
    best_move = None
    best_score = float('-inf')
    mov_validos = obtener_mov_validos(tablero, ultimo_mov)
    
    if not mov_validos:
        return None  # No hay movimientos válidos, el juego ha terminado

    for move in mov_validos:
        copia_tablero = copy.deepcopy(tablero)
        update_tablero('X', move, copia_tablero)
        score = minimax(copia_tablero, 3, False, float('-inf'), float('inf'), ('X', move[0], move[1]))
        if score > best_score:
            best_score = score
            best_move = move
        
        if time.time() - tiempo_inicial > tiempo_limite:
            print("La IA está tomando demasiado tiempo, usando el mejor movimiento encontrado hasta ahora.")
            break
    
    return best_move


# Procesa el movimiento del jugador humano
def mov_jugador(tablero, ultimo_mov):
    mov_validos = obtener_mov_validos(tablero, ultimo_mov)
    while True:
        try:
            print("Ingresa tu movimiento en formato 'Aa' donde 'A' es el sub-tablero y 'a' es la posición en ese sub-tablero.")
            move_input = input("Tu movimiento: ").strip()
            if len(move_input) != 2 or not move_input[0].isupper() or not move_input[1].islower():
                raise ValueError
            move = convert_from_letter_format(move_input)
            if move in mov_validos:
                return move
            else:
                print("Movimiento inválido. Intenta nuevamente.")
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar dos letras en el formato correcto (por ejemplo, 'Aa').")

# Imprime el tablero de juego
def print_tablero(tablero):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(tablero[i][j] if tablero[i][j] != '' else '.', end=" ")
        print()

# Verifica si hay un ganador en el juego completo
def checar_ganador_juego(tablero):
    tablero_principal = [['' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            sub_tablero = obten_sub_tablero(tablero, i*3, j*3)
            if checa_ganador('X', sub_tablero):
                tablero_principal[i][j] = 'X'
            elif checa_ganador('O', sub_tablero):
                tablero_principal[i][j] = 'O'
    
    if checa_ganador('X', tablero_principal):
        return 'X'
    elif checa_ganador('O', tablero_principal):
        return 'O'
    elif empate(tablero_principal):
        return 'Tie'
    return None

# Nueva función para elegir quién inicia el juego
def escoger_primer_jugador():
    while True:
        choice = input("¿Quién tendrá el primer turno? (1: Tú, 2: IA): ").strip()
        if choice == '1':
            return 'O'
        elif choice == '2':
            return 'X'
        else:
            print("Entrada inválida. Por favor, ingresa 1 o 2.")

# Función principal que ejecuta el juego (modificada)
def ejecutar_juego():
    print("Bienvenido al juego de Ultimate Tic Tac Toe.")
    print("Reglas del juego:")
    print("- El tablero es de 9x9, dividido en 9 sub-tableros 3x3.")
    print("- Gana un sub-tablero alineando 3 de tus símbolos.")
    print("- El lugar donde juegas en un sub-tablero determina en qué sub-tablero jugará tu oponente.")
    print("- Si te envían a un sub-tablero ganado o lleno, puedes jugar en cualquier sub-tablero no ganado y no lleno.")
    print("- Gana el juego al ganar 3 sub-tableros en línea.")
    print("- Los movimientos se ingresan como 'Aa', donde 'A' es el sub-tablero (A-I) y 'a' es la posición en ese sub-tablero (a-i).")
    
    tablero = [['' for _ in range(9)] for _ in range(9)]
    jugador_actual = escoger_primer_jugador()
    print(f"Comienza el jugador {jugador_actual}.")
    ultimo_mov = None

    while True:
        print_tablero(tablero)
        
        if jugador_actual == 'X':
            print("Turno de la IA (X)...")
            move = mov_ia(tablero, ultimo_mov)
            if move is None:
                print("No hay movimientos válidos disponibles. El juego ha terminado.")
                break
            move_str = convertir_a_letra(move[0], move[1])
            print(f"La IA jugó: {move_str}")
        else:
            move = mov_jugador(tablero, ultimo_mov)

        update_tablero(jugador_actual, move, tablero)
        ultimo_mov = (jugador_actual, move[0], move[1])

        ganador = checar_ganador_juego(tablero)
        if ganador:
            print_tablero(tablero)
            if ganador == 'Tie':
                print("¡Es un empate!")
            else:
                print(f'¡{ganador} ha ganado el juego!')
            break

        jugador_actual = 'O' if jugador_actual == 'X' else 'X'

if __name__ == "__main__":
    ejecutar_juego()
