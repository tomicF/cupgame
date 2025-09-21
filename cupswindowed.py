import matplotlib.pyplot as plt
import numpy as np
import pygame
import random

pygame.init()

window = pygame.display.set_mode((1200,600))
pygame.display.set_caption("CUP GAME")

#imgs
cup_red_img = pygame.image.load('./windowedimgs/cupred.png').convert_alpha()
cup_blue_img = pygame.image.load('./windowedimgs/cupblue.png').convert_alpha()
cup_green_img = pygame.image.load('./windowedimgs/cupgreen.png').convert_alpha()
cup_lightblue_img = pygame.image.load('./windowedimgs/cuplightblue.png').convert_alpha()
cup_lightgreen_img = pygame.image.load('./windowedimgs/cuplightgreen.png').convert_alpha()
cup_orange_img = pygame.image.load('./windowedimgs/cuporange.png').convert_alpha()
cup_pink_img = pygame.image.load('./windowedimgs/cuppink.png').convert_alpha()
cup_purple_img = pygame.image.load('./windowedimgs/cuppurple.png').convert_alpha()
cup_yellow_img = pygame.image.load('./windowedimgs/cupyellow.png').convert_alpha()
cup_green_img = pygame.image.load('./windowedimgs/cupgreen.png').convert_alpha()
cup_cyane_img = pygame.image.load('./windowedimgs/cupcyane.png').convert_alpha()

img_arr = [cup_red_img, cup_yellow_img, cup_lightgreen_img, 
           cup_orange_img, cup_pink_img, cup_lightblue_img, 
           cup_green_img, cup_cyane_img, cup_blue_img, 
           cup_purple_img]

#logic----------------------------------------------------------------------------------------------------------------------

#setup
problems_array = [
    [1, 0],
    [0, 2, 1],
    [3, 1, 0, 2],
    [2, 0, 4, 1, 3],
    [5, 2, 0, 4, 3, 1],
    [1, 4, 0, 6, 2, 5, 3],
    [7, 0, 3, 6, 5, 2, 1, 4],
    [8, 5, 2, 9, 0, 4, 7, 3, 6, 1]
]

currents_array = [
    [0, 1], 
    [0, 1, 2], 
    [0, 1, 2, 3], 
    [0, 1, 2, 3, 4], 
    [0, 1, 2, 3, 4, 5], 
    [0, 1, 2, 3, 4, 5, 6], 
    [0, 1, 2, 3, 4, 5, 6, 7], 
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
]

correct_solution = []  
current_solution = []

def solve_by_swapping(current_solution, correct_solution):
    def count_matches(a, b):
        return sum(1 for x, y in zip(a, b) if x == y)
    
    swaps = []
    x = 0
    k = 1
    n = len(current_solution)
    moves = []
    k_counter = []
    point_counter = []
    move_counter = 0

    working_solution = current_solution.copy()
    max_attempts = 10000
    attempts = 0

    while working_solution != correct_solution and attempts < max_attempts:
        start_correct = count_matches(working_solution, correct_solution)
        moves.append(move_counter)
        move_counter += 1
        k_counter.append(k)
        point_counter.append(count_matches(working_solution, correct_solution))

        improved = False

        while k < n:
            if x + k >= n:
                x = 0
                k += 1
                continue

            # swap elements
            working_solution[x], working_solution[x + k] = working_solution[x + k], working_solution[x]

            if count_matches(working_solution, correct_solution) < start_correct:
                # Undo the swap in-place
                working_solution[x], working_solution[x + k] = working_solution[x + k], working_solution[x]
                x += 1
            else:
                swaps.append([x, x + k])
                x += 1
                improved = True
                break  # found an improving swap, break to outer loop

        if not improved:
            # No improving swap found, do a random swap to escape local maxima
            i = random.randint(0, n - 2)
            j = random.randint(i + 1, n - 1)
            working_solution[i], working_solution[j] = working_solution[j], working_solution[i]
            swaps.append([i, j])
            # Reset x and k to start over
            x = 0
            k = 1

        attempts += 1

    return working_solution, moves, k_counter, point_counter, swaps


#logic---------------------------------------------------------------------------------------------------------------------

running = True
x = 0
clock = pygame.time.Clock()

cup_ammount = int(input("Enter your cup ammount: "))

#SETUP VARIABELS
current_solution = currents_array[cup_ammount]

drawn_solution = current_solution #THE SEQUENCE DISPLAYED ON SCREEN


correct_solution = problems_array[cup_ammount]

result = solve_by_swapping(current_solution, correct_solution)

swaps = result[4]

#CHECKING VALUES

print("correct solution: ", correct_solution)
print("current solution: ", drawn_solution)
print("swaps: ", swaps)

#RUUNING LOGIC

counter = 0
swap1, swap2 = None, None

while running:
    window.fill((255,255,255))
    
    #SOLUTION DRAWNIG
    for pos, cup_index in enumerate(correct_solution):
     cup = img_arr[cup_index]          # get correct cup image
     window.blit(cup, (pos * 100, 180))  
    
    for pos, cup_index in enumerate(drawn_solution):
     cup = img_arr[cup_index]          # get correct cup image
     if pos == swap1 or pos == swap2:
      window.blit(cup, (pos * 100, 430))  
     else: 
      window.blit(cup, (pos * 100, 380))  
     
    #ANSWER DRAWNIG
    if(drawn_solution != correct_solution):
        print("drawn solution: ", drawn_solution)
        to_do_swap = swaps[counter]
        swap1 = to_do_swap[0]
        swap2 = to_do_swap[1]
        
        drawn_solution[swap1], drawn_solution[swap2] = drawn_solution[swap2], drawn_solution[swap1]
        
        counter += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
    clock.tick(1)

            
pygame.quit()