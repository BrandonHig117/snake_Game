import sys
import pygame

# pygame setup
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#Se cargan las imagenes de la carpeta MEDIA
image1 = pygame.image.load("Media\perritoMusica.jpg")
image2 = pygame.image.load("Media\perritoMusica2.jpg")
image3 = pygame.image.load("Media\perritoMusica3.jpg")

#Se carga la musica de la carpeta MEDIA
pygame.mixer.music.load("Media\sonidoBrandon.mp3")
pygame.mixer.music.play()

while running:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  
  screen.fill("grey")

 #Se obtiene el tiempo actual en milisegundos desde que se inició pygame
  tiempo_actual = pygame.time.get_ticks()

 #Condicion si tiempo actual lleva menos de 4 segundos (milisegundos serian 4000) se muestra imagen 1
  if tiempo_actual < 4000:
    screen.blit(image1, (0, 100))
 #Condicion si tiempo actual lleva menos de 8 segundos (milisegundos serian 8000) se muestra imagen 2
  elif tiempo_actual < 8000:
    screen.blit(image2, (300, 100))
 #En caso de que el tiempo actual sea mayor a 8 segundos se muestra imagen 3
  else:
    screen.blit(image3, (600, 100))


  pygame.display.flip()

  clock.tick(60)  

pygame.quit()
sys.exit()