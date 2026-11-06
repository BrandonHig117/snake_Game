import pygame
import random
import sys

pygame.init() # Lo usamos para poder iniciar el juego.

# Usamos un tamaño de bloques de 20x20 píxeles para movernos por "casillas"
ANCHO = 600
ALTO = 600
BLOQUE = 20

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake Game")

# Colores
BLACK = (0, 0, 0)
GREEN = (46, 204, 113)  
RED = (231, 76, 60)      
WHITE = (255, 255, 255) 
BLUE = (55, 118, 171)
GRAY = (127, 140, 141)  # Color para los obstáculos

fuente = pygame.font.SysFont(None, 40)
fuente_chica = pygame.font.SysFont(None, 30)
reloj = pygame.time.Clock()

def generar_posicion_valida(serpiente, obstaculos):
    """Genera una posición aleatoria que no quede encima de la serpiente ni de los obstáculos"""
    while True:
        pos = [
            random.randrange(0, ANCHO // BLOQUE) * BLOQUE,
            random.randrange(0, ALTO // BLOQUE) * BLOQUE
        ]
        if pos not in serpiente and pos not in obstaculos:
            return pos

def reiniciar_juego():
    global serpiente, direccion, manzana, obstaculos, puntuacion, juego_terminado
    # La serpiente empieza con 3 bloques de tamaño guardados como coordenadas (x, y)
    serpiente = [[100, 100], [80, 100], [60, 100]]
    direccion = "RIGHT"  # Empieza moviéndose hacia la derecha
    puntuacion = 0
    
    # Generamos algunos obstáculos estáticos que estorben en el mapa agregamos 5 objetos
    obstaculos = []
    for _ in range(5):
        obs = [
            random.randrange(2, (ANCHO // BLOQUE) - 2) * BLOQUE,
            random.randrange(2, (ALTO // BLOQUE) - 2) * BLOQUE
        ]
        obstaculos.append(obs)

    # Generamos la primera manzana evitando que caiga en la serpiente u obstáculos
    manzana = generar_posicion_valida(serpiente, obstaculos)
    juego_terminado = False

# Llamamos a la función para iniciar por primera vez
reiniciar_juego()

# Bucle principal del juego
while True:
    # Se maneja el evento aqui que es cuando el usuario elija S o N para continuar o salir
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            # Si el juego terminó, presionamos S para reiniciar o N/ESC para salir
            if juego_terminado:
                if evento.key == pygame.K_s:
                    reiniciar_juego()
                elif evento.key == pygame.K_n or evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            # Se evita que gires y des por error hacia ti mismo en las 4 direcciones
            if evento.key == pygame.K_w and direccion != "DOWN":
                direccion = "UP"
            elif evento.key == pygame.K_s and direccion != "UP":
                direccion = "DOWN"
            elif evento.key == pygame.K_a and direccion != "RIGHT":
                direccion = "LEFT"
            elif evento.key == pygame.K_d and direccion != "LEFT":
                direccion = "RIGHT"

    # Si el juego NO ha terminado, actualizamos el movimiento
    if not juego_terminado:
        # Calculamos la posición de la nueva cabeza basada en la dirección actual
        cabeza = list(serpiente[0])
        if direccion == "UP":
            cabeza[1] -= BLOQUE
        elif direccion == "DOWN":
            cabeza[1] += BLOQUE
        elif direccion == "LEFT":
            cabeza[0] -= BLOQUE
        elif direccion == "RIGHT":
            cabeza[0] += BLOQUE

        # Si la serpiente toca (come) la manzana
        if cabeza == manzana:
            puntuacion += 1  # Sumamos 1 al marcador de manzanas
            # Generamos una nueva manzana en coordenadas aleatorias válidas llamando la funcion para que no reaparezca donde esta la serpiente o los bloques
            manzana = generar_posicion_valida(serpiente, obstaculos)
            # Como agarró la manzana, no se borra la cola (la serpiente crece)
        else:
            # Si no comió, eliminamos el último bloque para mantener el tamaño
            serpiente.pop()

        # Insertamos el nuevo valor de la cabeza haciendo que avance
        serpiente.insert(0, cabeza)

        # 1. Choque con las paredes de la ventana
        if cabeza[0] < 0 or cabeza[0] >= ANCHO or cabeza[1] < 0 or cabeza[1] >= ALTO:
            juego_terminado = True

        # 2. Choque con su propio cuerpo
        for bloque in serpiente[1:]:
            if cabeza == bloque:
                juego_terminado = True

        # 3. Choque con los obstáculos
        for obs in obstaculos:
            if cabeza == obs:
                juego_terminado = True

    # Renderizado en pantalla
    pantalla.fill(GREEN)

    # Dibujar los obstáculos
    for obs in obstaculos:
        pygame.draw.rect(pantalla, GRAY, (obs[0], obs[1], BLOQUE, BLOQUE))

    # Dibujar la manzana
    pygame.draw.rect(pantalla, RED, (manzana[0], manzana[1], BLOQUE, BLOQUE))

    # Dibujar cada parte del cuerpo de la serpiente
    for bloque in serpiente:
        pygame.draw.rect(pantalla, BLUE, (bloque[0], bloque[1], BLOQUE, BLOQUE))

    # Mostrar la puntuación actual en la esquina superior izquierda durante la partida
    texto_puntuacion = fuente_chica.render(f"Manzanas: {puntuacion}", True, WHITE)
    pantalla.blit(texto_puntuacion, (15, 15))

    # Si perdió, mostrar mensaje de Game Over y cuántas manzanas llevabas
    if juego_terminado:
        #Donde se muestra los textos en la pantalla del usuario
        texto_perdid = fuente.render("¡Haz Perdido!", True, BLACK)
        texto_resultado = fuente_chica.render(f"Manzanas totales recolectadas: {puntuacion}", True, BLACK)
        texto_opciones = fuente_chica.render("(S = Jugar de nuevo / N = Salir)", True, BLACK)
        
        pantalla.blit(texto_perdid, (ANCHO // 2 - 70, ALTO // 2 - 50))
        pantalla.blit(texto_resultado, (ANCHO // 2 - 150, ALTO // 2 - 10))
        pantalla.blit(texto_opciones, (ANCHO // 2 - 130, ALTO // 2 + 30))

    pygame.display.flip()  # Mostramos en pantalla lo que se editó
    
    # Velocidad del juego ajustada a 10 FPS para que se mueva de forma fluida y jugable lo tenia en 15 pero se siente rapido y origalmente va mas lento.
    reloj.tick(10)