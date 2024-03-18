import pygame
from agent import *
import random

class Jeu:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.h_division = 0.2
        self.screen = pygame.display.set_mode((w, h))
        self.list_points = []
        self.radius_point = 10
        self.list_agent = []
        self.best_agent = None
        self.list_affichage = ["Random", "Find"]
        self.rect_list_affichage = self.get_rect_from_list_affichage()
        self.font = None
    
    def get_rect_from_list_affichage(self):
        liste = []
        long_list = len(self.list_affichage)
        marge = 20
        space = int( self.w / long_list ) - 2*marge
        pas = int( self.w / long_list )
        for i in range(long_list):
            rectangle = pygame.Rect(i*pas + marge, self.h * (1 - self.h_division) + marge,  space, self.h * self.h_division - 2*marge)
            liste.append(rectangle)
        return liste

    def affichage_screen(self):
        pygame.draw.rect(self.screen, (15, 15, 15), pygame.Rect(0, self.h * (1 - self.h_division), self.w, self.h * self.h_division))
        
        # Affichage des list_points
        for point in self.list_points:
            pygame.draw.circle(self.screen, (200, 0, 0), (point[0], point[1]), self.radius_point)
        
        # Affichage du meilleur trajet
        if self.best_agent != None:
            for i in range(len(self.best_agent.order_point)-1):
                pygame.draw.line(self.screen, (0, 255, 0), self.best_agent.order_point[i], self.best_agent.order_point[i+1])


        # Affichage des boutons du bas
        long_list = len(self.list_affichage)
        for i in range(long_list):
            pygame.draw.rect(self.screen, (0, 0, 200), self.rect_list_affichage[i])
            # Création du texte à afficher
            text = self.font.render(self.list_affichage[i], True, (255, 255, 255))
            self.screen.blit(text, self.rect_list_affichage[i].center)
        
        
    def add_agent_for_mutation(self, number_agents, list_points):
        for _ in range(number_agents):
            new_agent = Agent(list_points)
            new_agent.mutation(0.3)
            self.list_agent.append(new_agent)

    def add_agent(self, number_agent=1):
        for _ in range(number_agent):
            new_agent = Agent(self.list_points)
            new_agent.random_choice()
            self.list_agent.append(new_agent)

    def find_best_agent(self):

        if len(self.list_agent) == 0:
            return

        self.best_agent = self.list_agent[0]
        best_score = self.list_agent[0].score
        
        for agent in self.list_agent:
            if agent.score < best_score:
                self.best_agent = agent
                best_score = agent.score
        
    def add_point(self, x_pt, y_pt):
        self.list_points.append((x_pt, y_pt))

    def generate_random_points(self, number_points=10):
        self.list_points = []
        self.list_agent = []
        self.best_agent = None
        for _ in range(number_points):
            self.add_point(random.randint(0, self.w), random.randint(0, int(self.h * (1 - self.h_division) ) ) )


    def make_research(self):
        self.find_best_agent()

        selection = 0.9
        long_list = len(self.list_agent)

        self.list_agent = [self.best_agent]

        self.add_agent_for_mutation(int(long_list*selection), self.best_agent.order_point)
        self.add_agent(long_list - (1 + int(long_list*selection)))


    def main_loop(self):
        pygame.init()

        self.font = pygame.font.SysFont(None, 36)

        running = True
        research = False

        while running:

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Récupérer les coordonnées du clic de souris
                    mouse_pos = pygame.mouse.get_pos()
                    # Vérifier si les coordonnées du clic sont à l'intérieur du rectangle
                    for i in range(len(self.rect_list_affichage)):
                        if self.rect_list_affichage[i].collidepoint(mouse_pos):
                            if self.list_affichage[i] == "Random":
                                self.generate_random_points(100)
                                research = False
                            if self.list_affichage[i] == "Find":
                                research = True
                                self.add_agent(100)

            self.screen.fill((0, 0, 0))
            if research:
                self.make_research()
            self.affichage_screen()

            # Mettre à jour l'affichage
            pygame.display.flip()