from graph_util import *
from search import *
from sprite import Sprite
import sys, time
import pygame
import os

from pygame.locals import *
from pygame import mixer


# main file
sys.setrecursionlimit(25000)
COLOR = (155, 100, 98)

def run():
    i = 0
    prev = False
    while(True):
        if(repeated_path1 and i < len(repeated_path1)):
            time.sleep(0.05)
            if(prev):
                pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(prev[0], prev[1], BLOCK_SIZE-1, BLOCK_SIZE-1))
            x = repeated_path1[i].position[0]*BLOCK_SIZE + 1
            y = repeated_path1[i].position[1]*BLOCK_SIZE + 1
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, BLOCK_SIZE-1, BLOCK_SIZE-1))
            prev = (x, y)
            pygame.display.flip()
            #draw_grid()
            i += 1

            #stop music
            if(i>=len(repeated_path1)):
                mixer.music.stop()
            
            #transition
            if(i%2==0):
                bg.set_alpha(3*(i/len(repeated_path1)))
                print(3*(i/len(repeated_path1)))
                screen.blit(bg,(0,0))

        # x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        


        pygame.display.update()

def draw_grid():

    for i in range(DIM):
        for j in range(DIM):
            if(g[(i,j)].is_blocked()):
                left = BLOCK_SIZE * i
                top = BLOCK_SIZE * j
                width = BLOCK_SIZE
                height = BLOCK_SIZE
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(left, top, width, height)) 

    for i in range(DIM+1):
        pygame.draw.line(surface = screen, color=(255,255,255), start_pos=(BLOCK_SIZE * i, 0), end_pos=(BLOCK_SIZE * i,SCREEN_HEIGHT), width=1)
        pygame.draw.line(surface = screen, color=(255,255,255), start_pos=(0,(SCREEN_HEIGHT/(DIM)) * i), end_pos=(SCREEN_WIDTH,(SCREEN_HEIGHT/(DIM)) * i), width=1)


if __name__ == "__main__":

    DIM = 40
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    BLOCK_SIZE = SCREEN_WIDTH/DIM
    OFFSET = 1
    pygame.init()
    mixer.init()
    mixer.music.load("song.mp3")
    screen = pygame.display.set_mode((SCREEN_WIDTH+OFFSET, SCREEN_HEIGHT+OFFSET))
    bg = pygame.image.load(os.path.join("./", "background.png"))
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    head = pygame.image.load(os.path.join('./', 'head.png'))
    head = pygame.transform.scale(head, (BLOCK_SIZE, BLOCK_SIZE))
    
    m = Maze()
    s = Search()

    # test_graphs = m.get_testing_graphs(count=5)
    start_t = time.perf_counter()
    g,_ = m.generate_graph(1, dim = DIM)
    
    repeated_path1, num_expanded1 = s.repeated_A_star(g, (0, 0), (DIM-1, DIM-1))
    draw_grid()
    if not repeated_path1:
        print("Path not found using repeated A*...\n")
    else:
        mixer.music.play()
        print(repeated_path1)
    run()
    

     

    # for graph in test_graphs:
    #     print(f"############# GRAPH {graph.get_label()}")
    #     repeated_path1, num_expanded1 = s.repeated_A_star(graph, (0, 0), (4, 4))
    #     print(graph)
    #     if not repeated_path1:
    #         print("Path not found using repeated A*...\n")
    #         continue

    #     print(repeated_path1)

    end_t = time.perf_counter()
    print(f"Time taken to complete all path test cases: {end_t - start_t}")

    '''
    # TESTING GRAPH THATS SHOWN IN THE ASSIGNMENT PDF
    g = Graph(1, 5)
    g.set_cell_status((1, 2), True)
    g.set_cell_status((2, 2), True)
    g.set_cell_status((3, 2), True)
    g.set_cell_status((2, 3), True)
    g.set_cell_status((3, 3), True)
    g.set_cell_status((4, 3), True)
    print(g)
    '''