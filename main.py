import os
from graph_util import *
from search import *
import sys, time, pygame, random
from pygame import mixer
import math

# main file
sys.setrecursionlimit(12000)
SCREEN_HEIGHT, SCREEN_WIDTH = 800, 800

def run(screen, path, block_size):
    isSplit = True if len(path)==2 else False
    bg = pygame.image.load("background.png")
    bg = pygame.transform.scale(bg, ((SCREEN_WIDTH * 2) + 5, SCREEN_HEIGHT))
    mixer.init()
    mixer.music.load("song.mp3")
    mixer.music.play()
    i = 0
    j = 0
    prev1 = False
    prev2 = False
    while True:
        time.sleep(0.05)
        if path[0] and i < len(path[0]):
            draw_grid(g, block_size, screen, split = isSplit)
            if(len(path[0]) > len(path[1])):
                bg.set_alpha(math.sin(i/3)*255)
            else:
                bg.set_alpha(math.sin(j/3)*255)
            screen.blit(bg, (0, 0))
            if prev1:
                pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(prev1[0], prev1[1], block_size-1, block_size-1))
            x1 = path[0][i].position[1]*block_size + 1
            y1 = path[0][i].position[0]*block_size + 1
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x1, y1, block_size-1, block_size-1))
            prev1 = (x1, y1)
            i += 1
        if len(path) == 2 and path[1] and j < len(path[1]):
            if prev2:
                pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(prev2[0], prev2[1], block_size-1, block_size-1))
            x2 = path[1][j].position[1]*block_size + 1 + SCREEN_WIDTH + 4
            y2 = path[1][j].position[0]*block_size + 1
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x2, y2, block_size-1, block_size-1))
            prev2 = (x2, y2)
            j += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()


def draw_grid(g, block_size, screen, split):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    for i in range(g.get_dim()):
        for j in range(g.get_dim()):
            if g[(i, j)].is_blocked():
                left = block_size * j
                top = block_size * i
                width = block_size
                height = block_size
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(left, top, width, height))

    for i in range(g.get_dim()+1):
        pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(block_size * i, 0),
                         end_pos=(block_size * i, SCREEN_HEIGHT), width=1)
        pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(0, (SCREEN_HEIGHT/(g.get_dim())) * i),
                         end_pos=(SCREEN_WIDTH, (SCREEN_HEIGHT/(g.get_dim())) * i), width=1)
    
    if(split == True):
        offs = 4
        pygame.draw.line(surface=screen, color=(0, 0, 255), start_pos=(SCREEN_WIDTH + 2, 0),end_pos=(SCREEN_WIDTH + 2, SCREEN_HEIGHT), width=offs)
        for i in range(g.get_dim()):
            for j in range(g.get_dim()):
                if g[(i, j)].is_blocked():
                    left = (block_size * j) + SCREEN_WIDTH + offs
                    top = block_size * i
                    width = block_size
                    height = block_size
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(left, top, width, height))

        for i in range(g.get_dim()+1):
            pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=((block_size * i) + SCREEN_WIDTH + offs, 0),
                                end_pos=((block_size * i) + SCREEN_WIDTH + offs, SCREEN_HEIGHT), width=1)
            pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(SCREEN_WIDTH + offs, (SCREEN_HEIGHT/(g.get_dim())) * i),
                                end_pos=((SCREEN_WIDTH * 2) + offs, (SCREEN_HEIGHT/(g.get_dim())) * i), width=1)       

def repeated_vs_adaptive_statistics(graph_count=50):
    count = graph_count
    test_start = time.perf_counter()

    # ran on 50 graphs of dimensions 101x101
    s, m = Search(), Maze()
    test_graphs = m.get_testing_graphs(count=graph_count)
    print("Generated graphs!")

    r_time, r_expanded = 0, 0
    a_time, a_expanded = 0, 0

    for graph in test_graphs:
        print(f"{graph.get_label()/graph_count: .2%} completed.", end="\r")
        c_start, c_end = (0, 0), (100, 100)
        # REPEATED A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.repeated_A_star(graph, c_start, c_end)

        if not cur_path: # if no path exists, don't use for statistics
            graph_count -= 1
            continue

        end_time = time.perf_counter()
        r_time += (end_time - start_time)
        r_expanded += num_expanded

        # ADAPTIVE A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.adaptive_A_star(graph, c_start, c_end)
        end_time = time.perf_counter()
        a_time += (end_time - start_time)
        a_expanded += num_expanded

    r_time, r_expanded = r_time/count, r_expanded/count
    a_time, a_expanded = a_time/count, a_expanded/count

    if r_time == 0:
        raise Exception("None of the graphs generated had a viable path.")

    print(f"Average time taken for repeated A star: {r_time} seconds, with average number of nodes expanded: {r_expanded: .2f}")
    print(f"Average time taken for adaptive A star: {a_time} seconds, with average number of nodes expanded: {a_expanded: .2f}")

    diff_time, diff_expanded = (r_time - a_time)/r_time, (r_expanded - a_expanded)/r_expanded
    print(f"On average, adaptive A star took {diff_time: .2%} less time, with {diff_expanded: .2%} less nodes expanded.")
    test_end = time.perf_counter()
    print(f"Testing took {test_end - test_start : .4f} seconds.")

def forward_vs_backward_statistics(graph_count=50):
    count = graph_count
    test_start = time.perf_counter()

    # ran on 50 graphs of dimensions 101x101
    s, m = Search(), Maze()
    test_graphs = m.get_testing_graphs(count=graph_count)
    print("Generated graphs!")

    f_time, f_expanded = 0, 0
    b_time, b_expanded = 0, 0

    for graph in test_graphs:
        print(f"{graph.get_label()/count: .2%} completed.", end="\r")
        c_start, c_end = (0, 0), (100, 100)
        # REPEATED A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.repeated_A_star(graph, c_start, c_end)

        if not cur_path: # if no path exists, don't use for statistics
            graph_count -= 1
            continue

        end_time = time.perf_counter()
        f_time += (end_time - start_time)
        f_expanded += num_expanded

        # ADAPTIVE A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.adaptive_A_star(graph, c_start, c_end)
        end_time = time.perf_counter()
        b_time += (end_time - start_time)
        b_expanded += num_expanded

    f_time, f_expanded = f_time/count, f_expanded/count
    b_time, b_expanded = b_time/count, b_expanded/count

    if f_time == 0:
        raise Exception("None of the graphs generated had a viable path.")

    print(f"Average time taken for repeated forward A star: {f_time} seconds, with average number of nodes expanded: {f_expanded: .2f}")
    print(f"Average time taken for repeated backwards A star: {b_time} seconds, with average number of nodes expanded: {b_expanded: .2f}")

    diff_time, diff_expanded = (f_time - b_time)/f_time, (f_expanded - b_expanded)/f_expanded
    print(f"On average, repeated backwards A star took {diff_time: .2%} less time, with {diff_expanded: .2%} less nodes expanded.")
    test_end = time.perf_counter()
    print(f"Testing took {test_end - test_start : .4f} seconds.")    

def forward_vs_backward(g, screen, block_size):
    screen = pygame.display.set_mode(((SCREEN_WIDTH*2)+OFFSET+5, SCREEN_HEIGHT+OFFSET))
    forward_path, _ = s.repeated_A_star(g, (0, 0), (g.get_dim() - 1, g.get_dim() -1))
    backward_path, _ = s.repeated_A_star(g, (g.get_dim() - 1, g.get_dim() - 1), (0, 0))
    if(backward_path):
        backward_path.reverse()
    a_path = []
    a_path.append(forward_path)
    a_path.append(backward_path)
    draw_grid(g, block_size, screen, split = True)
    run(screen, a_path, BLOCK_SIZE)

if __name__ == "__main__":
    # repeated_vs_adaptive_statistics(2)
    # forward_vs_backward_statistics()

    OFFSET = 1
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH+OFFSET, SCREEN_HEIGHT+OFFSET))

    m = Maze()
    s = Search()

    # TESTING GRAPH THATS SHOWN IN THE ASSIGNMENT PDF
    # g = Graph(1, 5)
    # g.set_cell_status((1, 2), True)
    # g.set_cell_status((2, 2), True)
    # g.set_cell_status((3, 2), True)
    # g.set_cell_status((2, 3), True)
    # g.set_cell_status((3, 3), True)
    # g.set_cell_status((4, 3), True)
    # print(g)
    g, _ = m.generate_graph(1, dim=50)

    BLOCK_SIZE = SCREEN_WIDTH/g.get_dim()

    path, _ = s.repeated_A_star(g, (0, 0), (g.get_dim() - 1, g.get_dim() -1))
    a_path = []
    a_path.append(path)

    print(path)

    # draw_grid(g, BLOCK_SIZE, screen)
    # run(screen, a_path, BLOCK_SIZE)

    forward_vs_backward(g, screen, BLOCK_SIZE)

