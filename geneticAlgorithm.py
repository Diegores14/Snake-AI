''' Network Config
  Layer Input -> 24 
  Layer 1 -> 16 neurons
  Layer 2 -> 16 neurons
  Layer Ouput -> 4
  Population = 2000 individuals
  amount of weights per individual = 24*16 + 16*16 + 16*4 + 16 + 16 + 4 = 740
  2000*740 = 1480000
'''
import tensorflow as tf
import random
import numpy as np

pressure = 3  
mutation_chance = 0.2 

def individual():
  layers = tf.keras.models.Sequential([
      tf.keras.layers.InputLayer(input_shape=(24,)),
      tf.keras.layers.Dense(16, activation='relu'),
      tf.keras.layers.Dense(16, activation='relu'),
      tf.keras.layers.Dense(4, activation='softmax')
    ]).layers
  return [ layer.get_weights() for layer in layers ]

def createPopulation(quantity):
  return [individual() for i in range(quantity)]

# def calcularFitness(individual):
#     """
#         Calcula el fitness de un individuo concreto.
#     """
#     fitness = 0
#     for i in range(len(individual)):
#         if individual[i] == modelo[i]:
#             fitness += 1
  
#     return fitness

def selection_and_reproduction(population):
  """
      Puntua todos los elementos de la poblacion (population) y se queda con los mejores
      guardandolos dentro de 'selected'.
      Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
      llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
      modificar).

      Por ultimo muta a los individuos.

  """
  # puntuados = [ (calcularFitness(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
  # puntuados = [i[1] for i in sorted(puntuados)] #Ordena los pares ordenados y se queda solo con el array de valores
  # population = puntuados
  puntuados = population


  selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'



  #Se mezcla el material genetico para crear nuevos individuos
  for i in range(len(population)-pressure):
    padre = random.sample(selected, 2) #Se eligen dos padres
    for j in range(3):
      punto = random.randint(1,len(population[i][j][0])-1) #Se elige un punto para hacer el intercambio
        
      population[i][j][0][:punto] = padre[0][j][0][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
      population[i][j][0][punto:] = padre[1][j][0][punto:]

      punto = random.randint(1,len(population[i][j][1])-1) #Se elige un punto para hacer el intercambio

      population[i][j][1][:punto] = padre[0][j][1][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
      population[i][j][1][punto:] = padre[1][j][1][punto:]
  
  return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven


def mutation(population):
    """
        Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria
        alcanzarse la solucion.
    """
    for i in range(len(population)-pressure):
      if random.random() <= mutation_chance: #Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
        for j in range(3): 
          punto = random.randint(0,len(population[i][j][0])-1) #Se elgie un punto al azar
          population[i][j][0][punto] = np.random.uniform(-1, 1, size=population[i][j][0][punto].shape) #y un nuevo valor para este punto

          punto = random.randint(0,len(population[i][j][1])-1) #Se elgie un punto al azar
          population[i][j][1][punto] = random.uniform(-1, 1) #y un nuevo valor para este punto
  
    return population


# population = crearPoblacion()

# for i in range(100):
#     population = selection_and_reproduction(population)
#     population = mutation(population)

selection_and_reproduction(createPopulation(10))
