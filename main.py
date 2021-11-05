import pygame
from pygame import *
import sys
import os
import time
from random import randint

pygame.init()

#Screen Settings
info = pygame.display.Info()
screen_size = info.current_w, info.current_h
mainsurface = pygame.display.set_mode(screen_size)
screen = pygame.Surface((1280, 720))
screen.fill((255,255,255))

#colors
blue = (0,0,255)
light_blue = (0,255,255)
red = (235,0,0)
green  = (0,255,0)
purple = (128,0,128)
orange = (255,153,0)
brown = (29,0,0)
pink = (255,0,255)
colors = [orange, purple, green, brown, purple, light_blue, purple, pink, pink, orange, blue, blue, brown, red, orange, pink, pink, red, green, green, brown, light_blue, light_blue,
          orange, blue, purple, brown, red]

#Data
data = ["START", "KODAIKKANAL",  "THOOTHUKUDI", "MTC BUS",   "POLLAACHI", "KANCHIPURAM",  "KUMBAKONAM", "PUDUKKOTTAI", "THENI", "SIRAI",
        "CHENNAI", "VELLORE", "INCOME TAX", "COIMBATORE", "KAILASH", "MALABAAR", "KARAIKKUDI", "ERODE","MADURAI", "NAGAR KOVIL", "CORPORATION", "TRICHY", "DINDIGUL",
        "TREAT VAI", "OOTY", "CUDDALORE", "RAILWAYS", "HOSUR"]

price = [None, 4000, 3000, 8000, 3000, 3000, 2000, 5000, 3000, None, 5000, 4000, 10000, 5000, None, 2000, 4000, 4000, 5000, 4000, 8000, 5000, 4000, None, 3000, 5000, 9000, 3000]
font = pygame.font.Font("freesansbold.ttf", 15)     #Font


class Block:

    def __init__(self, pos, color, name, price, font, buyable):

        self.base_price = price
        self.pos = [pos[0] * 128, pos[1] * 124]
        self.color = color
        self.name = name
        self.text = font.render(self.name, True, (255,255,255))
        self.diff = (128 - self.text.get_size()[0])/2           #Used to place the text label in the center of the block
        self.sold = False
        self.buyable = buyable
        self.owner = None
        self.level = 0
        self.rent = 500
        self.Surface = pygame.Surface((15, 15))
        self.owner_color = (0,0,0)
        
        
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos[0] + 1, self.pos[1] + 1, 126, 122))
        pygame.draw.rect(screen, (0,0,0), (self.pos[0], self.pos[1], 128,124), 2)
        screen.blit(self.text, (self.pos[0] + self.diff, self.pos[1] + 52))
        self.level_text = font.render(str(self.level), True, (0,0,0))
        if(self.sold == True):
            self.Surface.fill(self.color)
            pygame.draw.circle(self.Surface, self.owner_color, (7,8), 8) 
            self.Surface.blit(self.level_text, (3, 2))
            screen.blit(self.Surface, (self.pos[0] + 100, self.pos[1] + 10))

    def get_info(self):
        return(self.name, self.sold, self.buyable, self.base_price, self.owner, self.name, self.rent)

    def change_info(self, player, color):
        self.owner = player
        self.owner_color = color
        self.sold = True
        self.owner_text = font.render(str(self.owner), True, (0, 0, 0))

    def upgrade(self):
        if(self.level < 4):
            upgrade_price = int((self.base_price/5) + (self.rent * self.level))
            ch = input("Price : " + str(upgrade_price) + " (y/n):")
            if(ch == 'y' or ch == 'Y'):
                self.level += 1
                self.rent += 500
                return(upgrade_price)
            
        
    
#Instantiating 28 Blocks
blocks = []
count = 0
for i in range(10):
    if(i in [0, 9]):
        a = Block([i, 0], colors[i], data[i], price[i], font, False)
        blocks.append(a)
    else:
        a = Block([i, 0], colors[i], data[i], price[i], font, True)
        blocks.append(a)
for i in range(5):
    if(i == 4):
        a = Block([9, i + 1], colors[10 + i], data[10 + i],  price[10 + i],font, False)
        blocks.append(a)
    else:
        a = Block([9, i + 1], colors[10 + i], data[10 + i], price[10 + i], font, True)
        blocks.append(a)
for i in range(9):
    if(i == 8):
        a = Block([8 - i, 5], colors[15 + i], data[15 + i], price[15 + i], font, False)
        blocks.append(a)
    else:
        a = Block([8 - i, 5], colors[15 + i], data[15 + i], price[15 + i], font, True)
        blocks.append(a)
for i in range(4):
        a = Block([0, 4 - i], colors[24 + i], data[24 + i], price[24 + i], font, True)
        blocks.append(a)

    
class Player:

    def __init__(self, space,  num, color, font):

        self.cash = 20000
        self.index = 0
        self.status = True              # Tells that whether the player is in or out of the game..
        self.path = []
        self.value = space * 10
        self.color = color
        self.num = num
        self.jail = False
        self.text = font.render(str(self.num), True, (0,0,0))
        self.Surface = pygame.Surface((15,15))
        for i in range(10):
            route = ((i * 128) + self.value, 10)
            self.path.append(route)
        for i in range(5):
            route = ((9 * 128) + self.value, ((i + 1) * 124) + 10)
            self.path.append(route)
        for i in range(9):
            route = (((8 - i) * 128) + self.value, (5 * 124) + 10)
            self.path.append(route)
        for i in range(4):
            route = (self.value, ((4 - i) * 124) +10)
            self.path.append(route)

    def draw(self):
        pygame.draw.rect(self.Surface, self.color, ( 0, 0 , 15, 15))
        self.Surface.blit(self.text, (3,2))
        screen.blit(self.Surface, (self.path[self.index][0], self.path[self.index][1]))
        
    def move(self, roll):
        if(self.index + roll <= 26):
            self.index += roll
        else:
            self.index = (self.index + roll) - 28
            print("Tamil Natta oru vaatti mulusa suthittu vandhutta...Indha Vechukko 5000 Rubaai\n")
            self.cash += 5000

    def display(self):
        print("Player" + str(self.num) + ": Rs." + str(self.cash) + "\t\t", end = '')

    def buying_logic(self):
        global blocks
        info = blocks[self.index].get_info()
        if(info[1] == False and info[2] == True):
            ch = input("Do you want to buy " + info[0] + " for Rs." + str(info[3]) +  " (y/n): ")
            if(ch == 'y' or ch == 'Y'):
                self.cash -= info[3]
                blocks[self.index].change_info(self.num, self.color)
                print("\nCongratulations...You bought " + info[0] + "....")
        else:
            if(info[4] != None):
                print("You have entered into player" + str(info[4]) + "'s Property...\n")
                print("You paid Rs." + str(info[6]) + " as rent")
                self.cash -= info[6]
                
            elif(info[4] == None and info[5] == "KAILASH"):
                print("\nBaktha... Indha Swamiji oda parisa vechukko....(Rs.4000)")
                self.cash += 4000

            elif(info[4] == None and info[5] == "TREAT VAI"):
                print("\nEdhukkunu laam kekkaadha...Aana Treat mattum vechudu....(Rs.5000)\n")
                self.cash -= 5000

            elif(info[4] == None and info[5] == "SIRAI"):
                print("\nOru Turn unakku Cut...")
                self.jail = True
                
                                
        ch2 = input("\n\nDo you want to build hotels on your owned cities? (y/n): ")
        if(ch2 == 'y' or ch2 == 'Y'):
            owned = []
            for j in blocks:
                if(j.owner == self.num):
                    owned.append(j.name)
                    print(j.name + "\tlevel: " + str(j.level))
            build = str(input("\nEnter the city name to upgrade: "))
            if(build in owned):
                for k in blocks:
                    if(build == k.name):
                        cost = k.upgrade()
                        self.cash -= cost
        input()
        

#console
def clear():         
    os.system("cls")
    print("\t\t\t\tWELCOME TO CK'S BUSSINESS GAME\n")
    for i in players:
        i.display()
    print("\n\n")
os.system("cls")
print("\t\t\t\tWELCOME TO CK'S BUSSINESS GAME\n")
player_num = int(input("Enter the number of players (MAX 4 & MIN 2) : "))
players = []

if(player_num == 2):
    player1 = Player(1, 1,(255,50,0), font)
    player2 = Player(3, 2, (51,204,204), font)
    players.append(player1)
    players.append(player2)
elif(player_num == 3):
    player1 = Player(1, 1, (255,50,0), font)
    player2 = Player(3,  2, (51,204,204), font)
    player3 = Player(5, 3, (153, 204,0), font)
    players.append(player1)
    players.append(player2)
    players.append(player3)
else:
    player1 = Player(1, 1, (255,50,0), font)
    player2 = Player(3, 2, (51,204,204), font)
    player3 = Player(5, 3, (153, 204,0), font)
    player4 = Player(7, 4, (255,255,0), font)
    players.append(player1)
    players.append(player2)
    players.append(player3)
    players.append(player4)

os.system("cls")

def loop():

    for i in blocks:
        i.draw()
        
    for i in players:
        i.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                player1.move()
                player2.move()
                player3.move()
                player4.move()

    mainsurface.blit(pygame.transform.scale(screen, screen_size), (0,0))
    pygame.display.update()
    
def gamelogic():
    while(True):
        for i in players:
            if(i.jail == False and i.status == True):
                clear()
                print("Player" + str(i.num) + "'s Turn\n")
                input("Press Enter to roll THE INVISIBLE DICE....\n")
                roll = randint(2,12)
                print("DICE : " + str(roll))
                i.move(roll)
                i.draw()
                loop()
                i.buying_logic()
            elif(i.jail == True and i.status == True):
                clear()
                i.jail = False
                print("\nPlayer" + str(i.num) + " is in jail...You can play on the next round...")
                input()
            if(i.cash < 0):
                if(i.status == True):
                    clear()
                    print("\nPlayer" + str(i.num) + " went BankRupt...\nAll his properties will be taken over by the RBI\n\nSo...Veettukku kelambu!!!")
                    for l in blocks:
                        if(l.owner == i.num):
                            l.sold = False
                            l.owner = None
                            l.level = 0
                    i.status = False
                    input()
                else:
                    pass
        count = 0
        for m in players:
            if(m.status == True):
                count += 1
                winner = str(m.num)
        if(count <  2):
            clear()
            print("\n\nPlayer" + winner + " has won the game!!!!!")
            input()
            pygame.quit()
            sys.exit()
loop()
gamelogic()



    
