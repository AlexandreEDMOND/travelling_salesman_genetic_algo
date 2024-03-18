import random
from math import sqrt
from copy import deepcopy

class Agent:
    def __init__(self, order_point):
        self.order_point = deepcopy(order_point)
        self.score = 999999999
    
    def random_choice(self):
        random.shuffle(self.order_point)
        self.calcul_score()

    def distance_euclidienne(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def calcul_score(self):
        self.score = 10
        for i in range(len(self.order_point) - 1):
            distance = self.distance_euclidienne(self.order_point[i], self.order_point[i+1])
            self.score += distance
    
    def mutation(self, mutation_rate):
        for _ in range(3):
            if random.random() < mutation_rate:
                rand_index_1 = random.randint(0, len(self.order_point) - 1)
                rand_index_2 = random.randint(0, len(self.order_point) - 1)

                # Échange des éléments
                self.order_point[rand_index_1], self.order_point[rand_index_2] = self.order_point[rand_index_2], self.order_point[rand_index_1]
        
        self.calcul_score()
