import pygame
import random

class Snake:
    def __init__(self, tamano):

        self.width, self.height = 20, 20  
        self.window_width, self.window_height = 300, 300  
        self.tamano = tamano

        self.direccion = pygame.K_RIGHT
        self.velocidad = self.width

        pygame.init()
        self.ventana = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake')

        self.reset()

    def reset(self):

        self.serpiente = [(random.randint(0, (self.window_width // self.width) - 1) * self.width,
                           random.randint(0, (self.window_height // self.height) - 1) * self.height)]
        self.direccion = pygame.K_RIGHT

        self.fruta = (random.randint(0, (self.window_width // self.width) - 1) * self.width,
                      random.randint(0, (self.window_height // self.height) - 1) * self.height)

    def step(self, accion):
        assert accion in {0, 1, 2}, "Accion invalida"  # 0 = sigue, 1 = izquierda, 2 = derecha

        x, y = self.serpiente[0]

        if accion == 1:  # Izquierda
            self.direccion = pygame.K_LEFT if self.direccion != pygame.K_RIGHT else self.direccion
        elif accion == 2:  # Derecha
            self.direccion = pygame.K_RIGHT if self.direccion != pygame.K_LEFT else self.direccion
        elif accion == 0:  # Arriba
            self.direccion = pygame.K_UP if self.direccion != pygame.K_DOWN else self.direccion

        if self.direccion == pygame.K_LEFT:
            x -= self.velocidad
        elif self.direccion == pygame.K_RIGHT:
            x += self.velocidad
        elif self.direccion == pygame.K_UP:
            y -= self.velocidad
        elif self.direccion == pygame.K_DOWN:
            y += self.velocidad

        nueva_posicion = (x, y)
        self.serpiente = [nueva_posicion] + self.serpiente[:-1]

        estado_nuevo = [0] * 11 
        termino = False
        recompenza = 0

        if self.serpiente[0] == self.fruta:
            # Si comemos la fruta
            self.serpiente.append(self.serpiente[-1])
            recompenza = 1
            self.fruta = (random.randint(0, (self.window_width // self.width) - 1) * self.width,
                          random.randint(0, (self.window_height // self.height) - 1) * self.height)
        elif nueva_posicion[0] < 0 or nueva_posicion[0] >= self.window_width or nueva_posicion[1] < 0 or nueva_posicion[1] >= self.window_height:
            # Si toca los bordes, pierde
            recompenza = -1
            termino = True

        self.render()
        return estado_nuevo, recompenza, termino

    def render(self):

        # fondo
        for i in range(0, self.window_width, self.width):
            for j in range(0, self.window_height, self.height):
                color = (173, 216, 230) if (i // self.width + j // self.height) % 2 == 0 else (135, 206, 235)
                pygame.draw.rect(self.ventana, color, (i, j, self.width, self.height))

        # serpiente
        for bloque in self.serpiente:
            pygame.draw.rect(self.ventana, (0, 255, 0), (*bloque, self.width, self.height))

        # manzanita
        fruta_centrada = (self.fruta[0] + self.width // 4, self.fruta[1] + self.height // 4)
        pygame.draw.rect(self.ventana, (255, 0, 0), (*fruta_centrada, self.width // 2, self.height // 2))

        pygame.display.update()