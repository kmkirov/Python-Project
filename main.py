import pygame, sys
from pygame.locals import *
import threading
from multiprocessing import Process, Value
import time
import pygame, pygame.font, pygame.event, pygame.draw, string

from game import Game
from GUI_process_fun import *



def end_turner():
    eq_counter = 0 # broqch za chiftove
    main_game.next_player_turn() # sledvashtiq igrach e na hod
    register.status(True)
    

# ------------------------ ======== player icons move, buy, mortaged ====== -------------- 


players_move_icons = {}
players_buy_icons = {}
players_mortage_icons = {} 


players_buy_icons[1]= pygame.image.load( 'players_icons/car - own.gif')
players_mortage_icons[1]= pygame.image.load('players_icons/car - mortage.gif')
players_move_icons[1]= pygame.image.load('players_icons/car.gif')

players_buy_icons[2]=pygame.image.load('players_icons/dog - own.gif')
players_mortage_icons[2]=pygame.image.load('players_icons/dog - mortage.gif')
players_move_icons[2]=pygame.image.load('players_icons/dog.gif')

players_buy_icons[3]=pygame.image.load('players_icons/ship - own.gif')
players_mortage_icons[3]=pygame.image.load('players_icons/ship - mortage.gif')
players_move_icons[3]=pygame.image.load('players_icons/ship.gif')

players_buy_icons[4]=pygame.image.load('players_icons/hat - own.gif')
players_mortage_icons[4]=pygame.image.load('players_icons/hat - mortage.gif')
players_move_icons[4]=pygame.image.load('players_icons/hat.gif')

#---houses ----
house_icons ={}
house_icons[0]=pygame.image.load('players_icons/zero.gif')
house_icons[1]=pygame.image.load('players_icons/one.gif')
house_icons[2]=pygame.image.load('players_icons/two.gif')
house_icons[3]=pygame.image.load('players_icons/three.gif')
house_icons[4]=pygame.image.load('players_icons/four.gif')
house_icons[5]=pygame.image.load('players_icons/hotel.gif')

#-----======== important function for animation
def saver():
    pygame.image.save(DISPLAYSURF,'pictures/resized.bmp')        

def display_current_player(display,player_name,player_budget,x_y_player_name,x_y_budget):
    font = pygame.font.Font(None, 30)
    textImg = font.render( "current player name: " + str(player_name), 1, (255,0,0))
    tImg = font.render( "budget: " + str(player_budget), 1, (255,0,0))
                          # player name coord (20,558) and budget(400,558)
    display.blit( textImg, x_y_player_name)
    display.blit( tImg, x_y_budget )# za da e nai otgore
    pygame.font.quit()



def find_position_x_y(position):
    picx = go_player_picturex
    picy = go_player_picturey
    for a in range(position):
        if picx > end_trip and picy >start_trip:
            
            picx = picx - step_trip
            picy = picy 
            
            
        elif picx <end_trip and picy >end_trip:
              
            picx = picx 
            picy = picy - step_trip
            
        elif picx < start_trip - magic_trip and picy <end_trip:
            picx = picx + step_trip
            picy = picy
        else :
            picx = picx 
            picy = picy + step_trip
    return (picx,picy)


def move_icon(old_poss, new_pos,player_icon,display):   
    picx,picy = find_position_x_y(old_poss)
    mousex = 0
    mousey= 0
    fpsClock = pygame.time.Clock()
    #DISPLAYSURF = pygame.display.set_mode((760, 555), 0, 32)
    bg_image = pygame.image.load('pictures/resized.bmp')
    #windowSurface = pygame.display.set_mode((500, 400),0,32)
    for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
    for a in range(new_pos):
        if picx > end_trip and picy >start_trip: 
            picx = picx - step_trip
            picy = picy 
            
            
        elif picx < end_trip and picy > end_trip:
              
            picx = picx 
            picy = picy - step_trip
            
        elif picx < start_trip - magic_trip and picy <end_trip:
            picx = picx + step_trip
            picy = picy
        else :
            picx = picx 
            picy = picy + step_trip
            
        display.blit(bg_image,(0, 0))
        display.blit(player_icon, (picx,picy))
        
        
        fpsClock.tick(FPS)
        pygame.display.update()        
        fpsClock.tick(FPS)
    return (picx,picy)
    #pygame.image.save(pygame.display.get_surface(),'C:/Python33/pictures/resized.bmp')



#-------======== buy house animation

def buy_or_mortage_property(player_buy_image, new_pos,display):
    bg_image = pygame.image.load('pictures/resized.bmp') # da go mahna 
    
    picx,picy = move_icon(0, new_pos,player_buy_image,display)
    if new_pos in range(0,11):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx ,picy-40))
    elif new_pos in range(11, 21):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx+40 ,picy))
    elif new_pos in range(21,31):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx ,picy+40))
    elif new_pos in range(31, 40):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx-40 ,picy))
    pygame.display.update()
    pygame.image.save(pygame.display.get_surface(),'pictures/resized.bmp')

#-------======== build house animation
def build_or_sell_house(player_buy_image, new_pos,display):
    bg_image = pygame.image.load('pictures/resized.bmp') # da go mahna 
    
    picx,picy = move_icon(0, new_pos,player_buy_image,display)
    if new_pos in range(0,11):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx ,picy-20))
    elif new_pos in range(11, 21):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx+20 ,picy))
    elif new_pos in range(21,31):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx ,picy+20))
    elif new_pos in range(31, 40):
        display.blit(bg_image,(0, 0))
        display.blit(player_buy_image, (picx-20 ,picy))
    pygame.display.update()
    pygame.image.save(pygame.display.get_surface(),'pictures/resized.bmp')







from buttons import *

FPS = 15 # frames per second setting
go_player_picturex = 497
go_player_picturey = 501

WHITE = (255, 255, 255)
start_trip = 500
end_trip = 50
step_trip = 46
magic_trip = 20 #bez popravkata ne e krasivo :)

from multiprocessing import Process, Value



 
menus1= menus()
# monopoly picture with players
def main(menus1):
    game = Game()
    FPS = 15
    picx = go_player_picturex
    picy = go_player_picturey
    global DISPLAYSURF, fpsClock
    pygame.init()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((760, 580), 0, 32)
    #windowSurface = pygame.display.set_mode((500, 400),0,32)
    pygame.display.set_caption('Hello ddddddddd world!')
    catImg1 = pygame.image.load('pictures/resized.bmp')
    catImg = pygame.image.load('pictures/dog.gif')
    #end of main pictures
    DISPLAYSURF.blit(catImg1,(0, 0))
    DISPLAYSURF.blit(catImg, (picx,picy))
    
       
    #end of buttons
    #move_icon(0, 10,players_buy_icons[1],DISPLAYSURF)
    #move_icon(0, 10,players_buy_icons[2],DISPLAYSURF)
    #buy_or_mortage_property(players_buy_icons[1], 3,DISPLAYSURF)
    #build_or_sell_house(players_buy_icons[1],3 ,DISPLAYSURF)
    pygame.display.update()
    menus1.menu(DISPLAYSURF,game,pygame.event.get())
    while True:
        for event in pygame.event.get():
            menus1.menu(DISPLAYSURF,game,event)
            pygame.display.update()
        
        

        #pionkax = 30
        #pionkay = 20
        #player_name = 'goshko'
        #player_budget = 400
         # player name coord (20,558) and budget(400,558)
        #display_current_player(DISPLAYSURF,'goshko',500,(20,558),(400,558))
        #blank_names(DISPLAYSURF, 1,(0,558))
        pygame.display.update()
        #display_current_player(DISPLAYSURF,'gosaddsashko',5200,(20,558),(400,558))
        
       
        
        
main(menus1)









#--------- ne znam za kakvo si
def f():
    FPS = 15
    picx = go_player_picturex
    picy = go_player_picturey
    global DISPLAYSURF, fpsClock
    pygame.init()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((760, 555), 0, 32)
    #windowSurface = pygame.display.set_mode((500, 400),0,32)
    pygame.display.set_caption('Hello ddddddddd world!')
    catImg1 = pygame.image.load('pictures/resized.bmp')
    catImg = pygame.image.load('pictures/dog.gif')
    #end of main pictures
    DISPLAYSURF.blit(catImg1,(0, 0))
    DISPLAYSURF.blit(catImg, (picx,picy))
    
    # buttons on the screen 

    bg_color = (255, 255, 255)
    text_color = (255,   0,   0)
    #windowBgColor = WHITE
    x_position = 600
    y_position = 100
    text_lenght = 150
    x_text_border = 30
    y_text_border =40   

    roll_button = Button()
    roll_button.create_button(DISPLAYSURF,bg_color, x_position ,y_position,text_lenght,x_text_border,y_text_border,'Roll',text_color)
    #                       range(start, end)   step
    y_position =(i for i in range(150,500) if i % 40 == 0)
    
    end_turn = Button()
    end_turn.create_button(DISPLAYSURF,bg_color, x_position ,next(y_position),text_lenght,x_text_border,y_text_border,'end_turn',text_color)
    
#processes = Process(target=f, )
