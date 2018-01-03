import pygame
import os
import sys
import time
import random
from itertools import permutations, combinations

pygame.init()
img = pygame.image.load('queen1.jpg')

white = (255,255,255)
lightsalmon = (255,160,122)
salmon = (250,128,114)
red = (255,0,0)
green = (34,177,76)
blue = (0,0,255)
black = (0,0,0)
font = pygame.font.SysFont(None, 60)
#display params
height=640
width=640

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Chess_Board                press s to checkout different solutions')



size = 80


boxlist=[]
queenlist=[]

def text_objects(msg,color):
    surf = font.render(msg,True,color)
    return surf , surf.get_rect()

def message_to_board(msg,color):
    textSurface, textRect = text_objects(msg,color)
    textRect.center = (width/2),(height/2)
    gameDisplay.blit(textSurface,textRect)
    pygame.display.update()
    
    

def reset_board():
    count =0
    for i in range(0,width,size):
        for j in range(0,height+size,size):
            boxes=[]
            if count % 2 == 1:               
                boxes.append(i)
                boxes.append(j)
                boxlist.append(boxes)
            count += 1

    print(boxlist)
    gameDisplay.fill(white)
    for XnY in boxlist:
            pygame.draw.rect(gameDisplay,black, [XnY[0],XnY[1],size,size])
            
    pygame.display.update()
    
    


def check_for_win():
    print(queenlist)
    for i in range(0,7):
        for j in range(i+1,8):
            if queenlist[i][1] == queenlist[j][1]:
                print(str(queenlist[i][1])+"="+str(queenlist[j][1]))
                print("i="+str(i))
                print("j="+str(j))
                return 0
            
            elif abs(queenlist[i][1] - queenlist[j][1]) == abs(queenlist[i][0] - queenlist[j][0]):
                print(str(queenlist[i][1])+"-"+str(queenlist[j][1])+"="+ str(queenlist[i][0])+"-"+str(queenlist[j][0]))
                return 0
                
                
    return 1            
        


    
def placement(x_val,y_val,circlelist):
    
    pygame.draw.circle(gameDisplay, red, [int(x_val),int(y_val)],10)
    pygame.display.update()
    circle=[]
    circle.append(x_val)
    circle.append(y_val)
    circlelist.append(circle)
    print(circlelist)

    queen=[]
    queen.append(int(x_val/size)+1)
    queen.append(int(y_val/size)+1)
    queenlist.append(queen)
    print(queenlist)


    if len(circlelist) == 8:
        win=check_for_win()
        if win == 1:
            print("You win!!!")
            message_to_board("You win!!!",red)
        else:
            print("You lost!!! Press c to continue")
            message_to_board("You lost!!! Press c to continue",red)
            
            

def remove_queen(x_val,y_val,circlelist):

    for circle in circlelist:
        if circle[0] == int(x_val) and circle[1] == int(y_val):
            for queen in queenlist:
                if queen[0] == (int(x_val/size)+1) and queen[1] == (int(y_val/size)+1):
                    queenlist.remove(queen)
            circlelist.remove(circle)
            print(circlelist)
            print(queenlist)
            for box in boxlist:
                if box[0] == int(x_val)-(size/2) and box[1] == int(y_val)-(size/2):    
                    print("color green")
                    pygame.draw.rect(gameDisplay, black, [(x_val)-(size/2),(y_val)-(size/2),size,size])
                    pygame.display.update()
                    return 0

            print("color white")
            pygame.draw.rect(gameDisplay, white, [(x_val)-(size/2),(y_val)-(size/2),size,size])
            pygame.display.update()
            return 0     
                
    return 1
    
           
def solution():
    sol =[]
    count = 0
    #pygame.event.wait()
    text = 8
    n = int(text)
    x = range(1, n+1)

    for permuation in permutations(range(1, n+1)):
        y = permuation
        all_permutations = list(zip(x,y))
        list_of_permutations.append(all_permutations)

    for possible_solution in list_of_permutations:
        solutions = []
        for piece1, piece2 in combinations(possible_solution, 2):
            solutions.append(is_diagonal(piece1, piece2))

        if True not in solutions:
            #print(possible_solution)
            sol.append(possible_solution)
            count += 1
         
    
    return (sol,count)                    
      

def is_diagonal(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    gradient = (y2-y1)/(x2-x1)
    if gradient == -1 or gradient == 1:
        return(True)
    else:
        return(False)

list_of_permutations = []


def render_solution(solution_tuple):
    print("=============")
    print(solution_tuple)
    for element in solution_tuple:
        x_val = (element[0]-1)*80 + size/2
        y_val = (element[1]-1)*80 + size/2
        
        pygame.draw.circle(gameDisplay, red, [int(x_val),int(y_val)],10)                
    pygame.display.update()
        
    

def gameloop():
    gameExit = False
    circlelist=[]
    sol=[]
    prev_key = "no_sol"
    
    
    while not gameExit:
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0] == 1:    
                #print(pygame.mouse.get_pos())
                vals= pygame.mouse.get_pos()
                x_val = int(vals[0]/size) * size + size/2
                y_val = int(vals[1]/size) * size + size/2
                #print(str(x_val)+ " and "+ str(y_val))
                print("calling function...")
                result=remove_queen(x_val,y_val,circlelist)
                if result:
                    placement(x_val,y_val,circlelist)               

            if event.type == pygame.QUIT:
                 gameExit=True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if prev_key != "sol":
                        sol,count=solution()
                    random_number=round(random.randrange(0,count))   
                    print(sol[random_number])
                    #update board
                    del queenlist[:]
                    del circlelist[:]
                    reset_board()
                    render_solution(sol[random_number])
                    prev_key = "sol"
                if event.key == pygame.K_c:
                    del queenlist[:]
                    del circlelist[:]
                    reset_board()
                    gameloop()        
           
reset_board()            
gameloop()
pygame.quit()
quit()
