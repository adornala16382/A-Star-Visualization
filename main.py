from graph_util import *
from search import *
import sys, time
import pygame
import os

from pygame.locals import *
from pygame import mixer


# main file
sys.setrecursionlimit(25000)
COLOR = (155, 100, 98)
A_STAR = 0
REPEATED_A_STAR = 1
ADAPTIVE_A_STAR = 2

def run(screen, repeated_path1, BLOCK_SIZE, speed):
    i = 0
    prev = False
    while(True):
        if(repeated_path1 and i < len(repeated_path1)):
            time.sleep(1/speed)
            if(prev):
                pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(prev[0], prev[1], BLOCK_SIZE-1, BLOCK_SIZE-1))
            x = repeated_path1[i].position[1]*BLOCK_SIZE + 1
            y = repeated_path1[i].position[0]*BLOCK_SIZE + 1
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, BLOCK_SIZE-1, BLOCK_SIZE-1))
            prev = (x, y)
            #draw_grid()
            i += 1

            #stop music
            if(i>=len(repeated_path1)):
                mixer.music.stop()
            
            #transition
            # if(i%2==0):
            #     bg.set_alpha(3*(i/len(repeated_path1)))
            #     screen.blit(bg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        


        pygame.display.update()

def draw_grid(g, DIM, BLOCK_SIZE, screen, SCREEN_HEIGHT, SCREEN_WIDTH):

    for i in range(DIM):
        for j in range(DIM):
            if(g[(i,j)].is_blocked()):
                left = BLOCK_SIZE * j
                top = BLOCK_SIZE * i
                width = BLOCK_SIZE
                height = BLOCK_SIZE
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(left, top, width, height)) 

    for i in range(DIM+1):
        pygame.draw.line(surface = screen, color=(255,255,255), start_pos=(BLOCK_SIZE * i, 0), end_pos=(BLOCK_SIZE * i,SCREEN_HEIGHT), width=1)
        pygame.draw.line(surface = screen, color=(255,255,255), start_pos=(0,(SCREEN_HEIGHT/(DIM)) * i), end_pos=(SCREEN_WIDTH,(SCREEN_HEIGHT/(DIM)) * i), width=1)

def start_game(DIM, forward, speed, iterations, method):
    for _ in range(iterations):
        DIM = 5
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 1000
        BLOCK_SIZE = SCREEN_WIDTH/DIM
        OFFSET = 1
        pygame.init()
        mixer.init()
        mixer.music.load("song.mp3")
        mixer.music.set_volume(0.1)
        screen = pygame.display.set_mode((SCREEN_WIDTH+OFFSET, SCREEN_HEIGHT+OFFSET))
        bg = pygame.image.load(os.path.join("./", "background.png"))
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        head = pygame.image.load(os.path.join('./', 'head.png'))
        head = pygame.transform.scale(head, (BLOCK_SIZE, BLOCK_SIZE))
        
        m = Maze()
        s = Search()

        # TESTING GRAPH THATS SHOWN IN THE ASSIGNMENT PDF
        g = Graph(1, 5)
        g.set_cell_status((1, 2), True)
        g.set_cell_status((2, 2), True)
        g.set_cell_status((3, 2), True)
        g.set_cell_status((2, 3), True)
        g.set_cell_status((3, 3), True)
        g.set_cell_status((4, 3), True)
        print(g)

        # g,_ = m.generate_graph(1, dim = DIM)
        start_t = time.perf_counter()
        # forward or backward
        if(forward):
            repeated_path1,_ = s.repeated_A_star(g, (4, 1), (4, 4))
        else:
            repeated_path1,_ = s.repeated_A_star(g,  (DIM-1, DIM-1), (0, 0))
        end_t = time.perf_counter()
        draw_grid(g, DIM, BLOCK_SIZE, screen, SCREEN_HEIGHT, SCREEN_WIDTH)
        if not repeated_path1:
            print("Path not found using repeated A*...\n")
        else:
            mixer.music.play()
            print(repeated_path1)
            print(f"Found path in {end_t-start_t}.")
        run(screen, repeated_path1, BLOCK_SIZE, speed)


if __name__ == "__main__":
     
     start_game(DIM = 5, forward = False, speed = 10, iterations = 5, method = REPEATED_A_STAR)
