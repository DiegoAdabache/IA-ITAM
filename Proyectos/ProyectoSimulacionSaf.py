import math
import random
import matplotlib.pyplot as plt

"""
Para poder visualizar el modelo de manera adecuada tiene que correr el código permitiendo
que los gráficos se cargen dentro del área de plot, no con la opción de graficar en 
una pestaña extra.
"""

# Clase para representar un camino en el parque
class Camino:
    def __init__(self, puntos_ruta, entrada, salida):
        self.puntos_ruta = puntos_ruta
        self.entrada = entrada
        self.salida = salida

# Clase para representar un animal en la simulación
class Animal:
    colores = {
        "león": "red", "jirafa": "brown", "elefante": "gray", "hipopótamo": "purple",
        "gacela": "blue", "cebra": "black", "leopardo": "gold"
    }
    jerarquias = {
        "león": 1, "hipopótamo": 2, "leopardo": 3, "elefante": 4,
        "jirafa": 5, "cebra": 6, "gacela": 7
    }
    esperanza_vida_intervalos = {
        "león": (30, 34), "jirafa": (40, 44), "elefante": (87, 95),
        "hipopótamo": (66, 71), "gacela": (25, 32), "cebra": (31, 36),
        "leopardo": (32, 37)
    }

    def __init__(self, id_animal, tipo, genero, posicion, ancho, alto):
        self.id_animal = id_animal
        self.tipo = tipo
        self.genero = genero
        self.posicion = posicion
        self.comportamiento = "nocturno" if tipo in ["león", "leopardo"] else "diurno"
        self.alimentacion = "carnívoro" if tipo in ["león", "leopardo"] else "herbívoro"
        self.jerarquia = self.jerarquias[tipo]
        self.hambre = 0
        self.vida = True
        self.edad = 0
        self.ya_reprodujo = False
        self.ancho = ancho
        self.alto = alto
        self.esperanza_vida = random.randint(*self.esperanza_vida_intervalos[tipo])  # Generar esperanza de vida aleatoria

    def mover(self):
        if self.vida:
            factor_movimiento = 0.5 if self.edad >= self.esperanza_vida else 1
            dx = random.uniform(-8, 8) * factor_movimiento
            dy = random.uniform(-8, 8) * factor_movimiento
            nueva_x = self.posicion[0] + dx
            nueva_y = self.posicion[1] + dy

            # Ajustar posición para que no salga del rango
            nueva_x = max(0, min(self.ancho, nueva_x))
            nueva_y = max(0, min(self.alto, nueva_y))

            self.posicion = (nueva_x, nueva_y)

    def incrementar_edad_y_hambre(self):
        if self.vida:
            self.edad += 1
            if self.alimentacion == "carnívoro":
                self.hambre += 5

            if self.edad > self.esperanza_vida:
                self.vida = False
                print(f"El animal tipo {self.tipo} con id {self.id_animal} ha muerto de vejez.")
            elif self.hambre >= 100:
                self.vida = False
                if self.alimentacion == "carnívoro":
                    print(f"El animal tipo {self.tipo} con id {self.id_animal} ha muerto de hambre.")

# Clase para representar un vehículo turístico
class Vehiculo:
    def __init__(self, id_vehiculo, posicion, sigue_camino=False, camino=None):
        self.id_vehiculo = id_vehiculo
        self.posicion = posicion
        self.sigue_camino = sigue_camino
        self.camino = camino
        self.punto_actual = 0

    def mover(self):
        if self.sigue_camino and self.camino:
            if self.punto_actual < len(self.camino.puntos_ruta):
                siguiente_punto = self.camino.puntos_ruta[self.punto_actual]
                self.posicion = siguiente_punto
                self.punto_actual += 1
            else:
                self.punto_actual = 0
        else:
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            self.posicion = (self.posicion[0] + dx, self.posicion[1] + dy)

# Clase para representar el parque
class Parque:
    def __init__(self, ancho, alto, num_animales, num_vehiculos):
        self.ancho = ancho
        self.alto = alto
        self.animales = []
        self.vehiculos = []
        self.caminos = []
        self.crear_animales(num_animales)
        self.crear_caminos()
        self.crear_vehiculos(num_vehiculos)

    def crear_animales(self, num_animales):
        especies = ["león", "jirafa", "elefante", "hipopótamo", "gacela", "cebra", "leopardo"]
        for i in range(num_animales):
            tipo = random.choice(especies)
            genero = random.choice(["macho", "hembra"])
            posicion = (random.uniform(0, self.ancho), random.uniform(0, self.alto))
            animal = Animal(id_animal=i, tipo=tipo, genero=genero, posicion=posicion, ancho=self.ancho, alto=self.alto)
            self.animales.append(animal)

    def crear_caminos(self):
        camino1 = Camino(puntos_ruta=[(0, 10), (20, 10),(27,15), (35, 20), (40, 30), (45,40), (50, 45), (55,48), (60, 50), (70,55), (75, 60), (77,70), (80, 90), (90,95), (100, 80)], entrada=(0, 10), salida=(100, 80))
        camino2 = Camino(puntos_ruta=[(0, 80), (10, 80), (15,75), (20, 70), (25,70), (30, 70), (40,65), (45, 60), (60, 50), (65,48), (70, 45), (80,40), (85, 30), (90,25), (100, 20)], entrada=(0, 80), salida=(100, 20))
        self.caminos.extend([camino1, camino2])

    def crear_vehiculos(self, num_vehiculos):
        for i in range(num_vehiculos):
            posicion = (random.uniform(0, self.ancho), random.uniform(0, self.alto))
            sigue_camino = random.choice([True, False])
            camino = random.choice(self.caminos) if sigue_camino else None
            vehiculo = Vehiculo(
                id_vehiculo=i,
                posicion=posicion,
                sigue_camino=sigue_camino,
                camino=camino
            )
            self.vehiculos.append(vehiculo)

    def reproducir(self, animal):
        for otro in self.animales:
            if (
                otro != animal and otro.tipo == animal.tipo and otro.genero != animal.genero and
                otro.vida and not otro.ya_reprodujo and not animal.ya_reprodujo
                and animal.edad > 9 and otro.edad > 9
            ):
                if random.random() < 0.2:
                    nuevo_id = len(self.animales)
                    nueva_posicion = (
                        (animal.posicion[0] + otro.posicion[0]) / 2,
                        (animal.posicion[1] + otro.posicion[1]) / 2,
                    )
                    nuevo_animal = Animal(
                        id_animal=nuevo_id,
                        tipo=animal.tipo,
                        genero=random.choice(["macho", "hembra"]),
                        posicion=nueva_posicion,
                        ancho=self.ancho,
                        alto=self.alto,
                    )
                    self.animales.append(nuevo_animal)
                    animal.ya_reprodujo = True
                    otro.ya_reprodujo = True
                    print(f"La {animal.tipo} con id {animal.id_animal} y la {animal.tipo} con id {otro.id_animal} dieron a luz al animal con id {nuevo_id}.")

    def devorar(self, depredador, presa):
        if depredador.alimentacion == "carnívoro" and depredador.vida and presa.vida and depredador.hambre >= 50:
            distancia = math.sqrt((depredador.posicion[0] - presa.posicion[0])**2 +
                                   (depredador.posicion[1] - presa.posicion[1])**2)
            if distancia < 5 and depredador.jerarquia < presa.jerarquia:
                presa.vida = False
                depredador.hambre = 0
                print(f"El animal tipo {presa.tipo} con id {presa.id_animal} ha sido devorado por el animal tipo {depredador.tipo} con id {depredador.id_animal}.")

    def ejecutar_paso(self):
        for animal in self.animales:
            if animal.vida:
                animal.mover()
                animal.incrementar_edad_y_hambre()
                self.reproducir(animal)

        for depredador in self.animales:
            if depredador.alimentacion == "carnívoro" and depredador.vida:
                for presa in self.animales:
                    if presa != depredador and presa.vida:
                        self.devorar(depredador, presa)

        for vehiculo in self.vehiculos:
            vehiculo.mover()

    def visualizar(self):
        plt.figure(figsize=(10, 8))
        plt.xlim(0, self.ancho)
        plt.ylim(0, self.alto)
        for camino in self.caminos:
            ruta_x, ruta_y = zip(*camino.puntos_ruta)
            plt.plot(ruta_x, ruta_y, linestyle="--", color="black")
        leyenda_agregada = set()
        for animal in self.animales:
            if animal.vida:
                plt.scatter(animal.posicion[0], animal.posicion[1], color=Animal.colores[animal.tipo])
                if animal.tipo not in leyenda_agregada:
                    plt.scatter([], [], color=Animal.colores[animal.tipo], label=animal.tipo)
                    leyenda_agregada.add(animal.tipo)
        for vehiculo in self.vehiculos:
            plt.scatter(vehiculo.posicion[0], vehiculo.posicion[1], color="green", label="Vehículo" if vehiculo == self.vehiculos[0] else "")
        plt.legend()
        plt.title("Simulación del Safari")
        plt.xlabel("Posición X")
        plt.ylabel("Posición Y")
        plt.show()

# Simulación principal
parque = Parque(ancho=100, alto=100, num_animales=38, num_vehiculos=5)
for paso in range(1):
    print(f"Paso {paso + 1}")
    parque.ejecutar_paso()
    parque.visualizar()
