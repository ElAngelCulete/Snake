import numpy as np
import random
import pickle
import pygame
import json

class Random:
    def __init__(self, juego):
        self.juego = juego

    def jugar(self): # Juega aleatoriamente
        running = True

        while running:
            print("hola, pase")
            # Elege una acción aleatoria (0 -> recto, 1 -> izquierda, 2 -> derecha)
            accion = random.choice([0, 1, 2])
            estado, recompensa, termino = self.juego.step(accion)

            if termino:
                #running = False  # Terminar el juego si ha terminado
                self.juego.reset()

            # Controlar los eventos de Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.time.delay(100)  # Retardo para controlar la velocidad del juego

    def entrenar(self):
        raise NotImplementedError("Entrenamiento no implementado para el jugador aleatorio")


class IA:
    def __init__(self, juego):
        self.juego = juego
        self.path = 'ola.json'
        self.Q = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1


    def entrenar(self, episodios=1000):
        for episodio in range(episodios):
            estado = self.obtener_estado()
            running = True

            while running:
                accion = self.elegir_accion(estado)
                estado_nuevo, recompensa, termino = self.juego.step(accion)

                if estado_nuevo not in self.Q:
                    self.Q[estado_nuevo] = np.zeros(3)

                # Actualizar la tabla Q con la fórmula de Q-learning
                mejor_accion_nueva = np.argmax(self.Q[estado_nuevo])
                self.Q[estado][accion] = self.Q[estado][accion] + self.alpha * (
                    recompensa + self.gamma * self.Q[estado_nuevo][mejor_accion_nueva] - self.Q[estado][accion]
                )

                estado = estado_nuevo

                if termino:  # Si el juego termina, reiniciar
                    self.juego.reset()
                    running = False

            if episodio % 100 == 0:
                print(f"Episodio {episodio} completado")

    def elegir_accion(self, estado):
        if estado not in self.Q:
            self.Q[estado] = np.zeros(3)  # Inicializar acciones si no existen en Q

        # Elegir entre exploración y explotación
        if random.uniform(0, 1) < self.epsilon:  # Probabilidad de explorar
            return random.choice([0, 1, 2])  # Acción aleatoria
        else:
            return np.argmax(self.Q[estado])  # Mejor acción conocida

    def obtener_estado(self):
        # Definir cómo se obtienen los estados del juego (puede ser una representación simplificada)
        cabeza = self.juego.serpiente[0]
        fruta = self.juego.fruta
        estado = (cabeza[0] // self.juego.width, cabeza[1] // self.juego.height)  # Ejemplo de estado basado en la posición
        return estado

    # Guardar y cargar la tabla Q
    def save(self):
        if self.path is not None:
            # Convertir el diccionario de numpy arrays a listas de Python
            Q_converted = {str(k): v.tolist() for k, v in self.Q.items()}
            with open(self.path, 'w') as f:
                json.dump(Q_converted, f)

    def load(self):
        if self.path is not None:
            try:
                with open(self.path, 'r') as f:
                    Q_loaded = json.load(f)
                    # Convertir listas de nuevo a numpy arrays
                    self.Q = {eval(k): np.array(v) for k, v in Q_loaded.items()}
            except FileNotFoundError:
                print(f"Archivo {self.path} no encontrado. Se comenzará desde cero.")
