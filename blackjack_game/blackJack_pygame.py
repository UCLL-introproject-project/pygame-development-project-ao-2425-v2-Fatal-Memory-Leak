###################### Importeren van alle modules en initiatie van pygame-modules #####################
import random
import pygame
import copy

pygame.init() #initialiseert alle Pygame-modules


##################################### Aanmaken van alle variabele ####################################

# Deck met kaarten aanmaken voor het spel
kaarten = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'B', 'V', 'K', 'A']
kaart_spel = 4 * kaarten
decks = 4 #Met hoeveel kaartspelen wordt gespeeld
# print(game_deck) #controlle

# Aanmaken variabele voor de grote van het spel (pygame window/scherm)
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Surface-object (een soort canvas)
pygame.display.set_caption("Pygame BlackJack") # Titel voor de adressbalk 
fps = 60 # Frames per seconde
timer = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 44) # font-family en font-size
smaller_font = pygame.font.Font("freesansbold.ttf", 36) # font-family en font-size
active = False # Is er een spel gaande
records = [0, 0, 0] # winst, verlies, gelijkspel
player_score = 0 # Bereken hoeveel punten de speler in zijn handen heeft aan kaarten
dealer_score = 0 # Hoeveel punten heeft de dealer
initial_deal = False # Eerste beurt wijkt af omdat er dan 2 kaarten gedeeld worden
my_hand = [] # Kaarten in spelers hand
dealer_hand = [] # Kaarten in de delers hand
outcome = 0 # 


################################################################################


#Game condities en knoppen toevoegen
def draw_game(act, record):
    button_list = [] # button lijst wordt geleegd door hem gelijk te stellen aan een lege lijst

    #Spel opstarten als active(=False), nieuwe hand delen
    if not act:
        deal = pygame.draw.rect(screen, "white", [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, "green", [150, 20, 300, 100], 3, 5)
        deal_text = font.render("DEAL HAND", True, "black")
        screen.blit(deal_text, (165, 50))
        button_list.append(deal) # Deal Hand op scherm

    # Als het spel gestart is geef opties voor hit and stand
    else:
        #hit button
        hit = pygame.draw.rect(screen, "white", [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, "green", [0, 700, 300, 100], 3, 5)
        hit_text = font.render("HIT ME", True, "black")
        screen.blit(hit_text, (55, 735)) #Plakt de tekst (text_surface) op deze coördinaten (x, y) op het scherm
        button_list.append(hit)

        #stand button
        stand = pygame.draw.rect(screen, "white", [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, "green", [300, 700, 300, 100], 3, 5)
        stand_text = font.render("STAND", True, "black")
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)

        score_text = smaller_font.render(f"Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}", True, "white")
        screen.blit(score_text, (15, 840))
    return button_list


################################################################################


# Main game loop
run = True
while run:          #Blijft lopen zolang de game "draait"abs
    
    #Game laten draaien op framerate en achtergrond instellen
    timer.tick(fps)
    screen.fill("black")
    buttons = draw_game(active, records)

    # Event handling, voor afsluiten spel
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Event voor klik op de button "deal"
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:   # Als er geen spel actief is dan is de "deal" button zichtbaar
                if buttons[0].collidepoint(event.pos):   #button[0] = deal, collidepoint(event.pos) = als er met de muis op deal geklikt wordt
                    
                    # Game wordt gestart
                    # Reset van hand, dealer en deck
                    active = True 
                    initial_deal = True #Eerste beurt worden er 2 kaarten gedeeld
                    game_deck = copy.deepcopy(decks * kaart_spel) #Lijkt niet direct nodig aangezien game_deck 1 lange lijst is geen nested lists bevat en de elementen strings zijn(imutabel)
                    my_hand = [] 
                    dealer_hand = []
                    outcome = 0



    
    pygame.display.flip() #Werkt je scherm bij (je “tekent” de frame op het scherm).
pygame.quit()
