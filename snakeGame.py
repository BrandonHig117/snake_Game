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

fuente = pygame.font.SysFont(None, 40)
fuente_chica = pygame.font.SysFont(None, 30)
reloj = pygame.time.Clock()

def generar_manzana(serpiente):
    """Genera una posición aleatoria para la manzana que no quede encima de la serpiente"""
    while True:
        pos = [
            random.randrange(0, ANCHO // BLOQUE) * BLOQUE,
            random.randrange(0, ALTO // BLOQUE) * BLOQUE
        ]
        if pos not in serpiente:
            return pos

def reiniciar_juego():
    global serpiente, direccion, manzana, juego_terminado
    # La serpiente empieza con 3 bloques de tamaño guardados como coordenadas (x, y)
    serpiente = [[100, 100], [80, 100], [60, 100]]
    direccion = "RIGHT"  # Empieza moviéndose hacia la derecha
    
    # Generamos la primera manzana evitando que caiga en la serpiente
    manzana = generar_manzana(serpiente)
    juego_terminado = False

# Llamamos a la función para iniciar por primera vez
reiniciar_juego()

# Bucle principal del juego
while True:
    # Se maneja el evento para salir o reiniciar
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
            # Generamos una nueva manzana en coordenadas aleatorias válidas
            manzana = generar_manzana(serpiente)
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

    # Renderizado en pantalla
    pantalla.fill(GREEN)

    # Dibujar la manzana
    pygame.draw.rect(pantalla, RED, (manzana[0], manzana[1], BLOQUE, BLOQUE))

    # Dibujar cada parte del cuerpo de la serpiente
    for bloque in serpiente:
        pygame.draw.rect(pantalla, BLUE, (bloque[0], bloque[1], BLOQUE, BLOQUE))

    # Si perdió, mostrar mensaje de Game Over simple
    if juego_terminado:
        texto_perdid = fuente.render("¡Has Perdido!", True, BLACK)
        texto_opciones = fuente_chica.render("(S = Jugar de nuevo / N = Salir)", True, BLACK)
        
        pantalla.blit(texto_perdid, (ANCHO // 2 - 90, ALTO // 2 - 30))
        pantalla.blit(texto_opciones, (ANCHO // 2 - 130, ALTO // 2 + 10))

    pygame.display.flip()  # Mostramos en pantalla lo que se editó
    
    # Velocidad del juego ajustada a 10 FPS
    reloj.tick(10)