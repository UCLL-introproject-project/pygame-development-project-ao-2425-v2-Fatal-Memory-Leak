###################### Importeren van alle modules en initiatie van pygame-modules #####################
import random
import pygame

pygame.init() #initialiseert alle Pygame-modules


##################################### Aanmaken van alle variabele ####################################

# Deck met kaarten aanmaken voor het spel
kaarten = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'B', 'V', 'K', 'A']
kaart_spel = 4 * kaarten
decks = 4 #Met hoeveel kaartspelen wordt gespeeld

# Aanmaken variabele voor de grote van het spel (pygame window/scherm)
WIDTH = 1024
HEIGHT = 700

# game instellingen
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Surface-object (een soort canvas)

# Afbeeldingen inladen en alpha waarde aanpassen
background = pygame.image.load("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/backgroundJungleSteampunk.webp").convert_alpha()
background.set_alpha(120)  # Lichter maken
logo_image = pygame.image.load("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/logoSteampunkProgramar.webp").convert_alpha()
logo_scaled = pygame.transform.scale(logo_image, (350, 350))
logo_rect = logo_scaled.get_rect(center=(WIDTH // 1.5, HEIGHT // 3))

pygame.display.set_caption("Pygame BlackJack") # Titel voor de adressbalk 
fps = 60 # Frames per seconde
timer = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 44) # font-family en font-size
smaller_font = pygame.font.Font("freesansbold.ttf", 36) # font-family en font-size

# variabelen voor de gameplay
active = False # Is er een spel gaande
records = [0, 0, 0] # winst, verlies, gelijkspel
player_score = 0 # Bereken hoeveel punten de speler in zijn handen heeft aan kaarten
dealer_score = 0 # Hoeveel punten heeft de dealer
initial_deal = False # Eerste beurt wijkt af omdat er dan 2 kaarten gedeeld worden
my_hand = [] # Kaarten in spelers hand
dealer_hand = [] # Kaarten in de delers hand
outcome = 0 # Waarde wordt gebruikt om een element uit de lijst results te kiezen
reveal_dealer = False # kaarten van de deler zijn geheim tot het einde van het spel
hand_active = False #Na de deeling wordt de hand active gemaakt door event handling
add_score = False
results = ["", "Player Busted", "Player Wins", "Dealer Wins", "Tie Game"]



####################################### Functies aanmaken #########################################

# Deel 1 kaart per keer random uit het game deck 
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck)-1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    #print(current_hand, current_deck)
    return current_hand, current_deck


# Kaarten tekenen op het scherm
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, "white", [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, "black"), (75 + 70*i, 465 + 5*i))
        screen.blit(font.render(player[i], True, "black"), (75 + 70*i, 635 + 5*i))
        pygame.draw.rect(screen, "red", [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    # Als de spel nog niet klaar is verberg 1 kaart van de dealer
    for i in range(len(dealer)):
        pygame.draw.rect(screen, "white", [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i !=0 or reveal:
            screen.blit(font.render(dealer[i], True, "black"), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render(dealer[i], True, "black"), (75 + 70*i, 335 + 5*i))
        else:
            screen.blit(font.render("???", True, "black"), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render("???", True, "black"), (75 + 70*i, 335 + 5*i))
        pygame.draw.rect(screen, "blue", [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# Bereken de score van de kaarten in een hand (speler of deler)
def calculate_score(hand):
    hand_score = 0
    ace_count = hand.count("A") # count telt het aantal elementen van de parametern ("A")

    # Deze for loop berekend de maximale score van de hand 
    for kaart in hand:
        if kaart in kaarten[0:8]:           # Als de kaart in de hand waarde tussen 2 en 9 heeft
            hand_score += int(kaart)        # String naar int en optelen bij totaal
        elif kaart in kaarten[8:12]:        # Alle kaarten die 10 waard zijn 
            hand_score += 10                # optellen maar....
        else:
            hand_score += 11                # voor een Aas nemen we standaard 11 punten
    if hand_score > 21 and ace_count > 0:
        for i in range(ace_count):
            if hand_score > 21:
                hand_score -= 10
    
    return hand_score


# De berekende score per hand tekenen in de game
def draw_score(player, dealer):
    screen.blit(font.render(f"Score: {player}", True, 'white'), (350, 400))
    if reveal_dealer:     # De score van de deler wordt alleen getoond aan het eind van het spel als reveal_dealer(=True)
            screen.blit(font.render(f"Score: {dealer}", True, 'white'), (350, 100))


# Game condities en knoppen toevoegen
def draw_game(act, record, result):
    button_list = [] # button lijst wordt geleegd door hem gelijk te stellen aan een lege lijst

    #Spel opstarten als active(=False), nieuwe hand delen
    if not act:
        deal = pygame.draw.rect(screen, "white", [150, 20, 300, 100], 0, 5) # Met draw.rect een rechthoek tekenen op het scherm
        pygame.draw.rect(screen, "green", [150, 20, 300, 100], 3, 5) # Rand maken om rechthoek
        deal_text = font.render("DEAL HAND", True, "black") # tekst maken
        screen.blit(deal_text, (165, 50)) # tekst op het scherm plakken
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

    # Als er een uitkomst is moet die op het scherm gezet worden, en komt er een herstart knop
    if result != 0:      # Als er een uitslag is
        screen.blit(font.render(results[result], True, "white"), (15, 25))
        deal = pygame.draw.rect(screen, "white", [150, 220, 300, 100], 0, 5) # Met draw.rect een rechthoek tekenen op het scherm
        pygame.draw.rect(screen, "green", [150, 220, 300, 100], 3, 5) # Rand maken om rechthoek
        pygame.draw.rect(screen, "black", [153, 223, 294, 94], 3, 5) # Rand maken om rechthoek
        deal_text = font.render("NEW HAND", True, "black") # tekst maken
        screen.blit(deal_text, (165, 250)) # tekst op het scherm plakken
        button_list.append(deal) # Deal Hand op scherm

    return button_list


# Uitkomst van het spel bepalen, winst/verlies/gelijkspel
def check_endgame(hand_act, dealer_score, player_score, result, totals, add):
    # Mogelijke resultaten, spelerscore <21, speler stood of blackjack
    # Resutaat 1-speler >21, 2-win, 3-loss, 4-gelijkspel
    if not hand_active and dealer_score >= 17:     
        if player_score > 21:       # meer dan 21 punten is standaard verlies
            result = 1              # speler verliest
        elif dealer_score < player_score <= 21 or dealer_score > 21:    #Speler wint
            result = 2                                                  
        elif player_score < dealer_score <= 21:                         # Deler wint   
            result = 3
        else:                                                           # Gelijk spel
            result = 4

        if add:
            if result == 1 or result == 3:  # Bij verlies
                totals[1] += 1
            elif result == 2:               # Bij wist
                totals[0] += 1
            else:                           # Bij gelijkspel
                totals[2] += 1
            add = False

    return result, totals, add



################################################################################


# Main game loop
run = True
while run:          # Blijft lopen zolang de game "draait"abs
    
    # Game laten draaien op framerate en achtergrond instellen
    timer.tick(fps)
    screen.blit(background, (0, 0))
    screen.blit(logo_scaled, logo_rect)     # Logo erbovenop

    # Eerst beurt voor speler en dealer
    if initial_deal:
        for i in range(2):      # Eerste beurt worden er om en om in totaal twee kaarten gedeeld voor speler en dealer
            my_hand,game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        #print(my_hand, dealer_hand)
        initial_deal = False    # na de eerste beurt 1 kaart per beurt

    # Als het stel active(true) is, er kaarten gedeeld zijn, bereken de score en teken de kaarten
    if active:
        player_score = calculate_score(my_hand)             # score speler worden berekend door de functie
        draw_cards(my_hand, dealer_hand, reveal_dealer)     # kaarten worden getekend op het scherm

        if reveal_dealer:                                   # als reveal dealer is true dan stopt de speler en vraagt naar de kaarten van de deler
            dealer_score = calculate_score(dealer_hand)     # bereken deler score
            if dealer_score < 17:                           # Als de score deler lager dan 17 is pakt hij een extra kaart
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)

        draw_score(player_score, dealer_score)              # teken de score op het scherm
    buttons = draw_game(active, records, outcome)           


    # Event handling, voor afsluiten spel
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Event voor klik op de button "deal"
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:   # Als er geen spel actief is dan is de "deal" button zichtbaar
                if buttons[0].collidepoint(event.pos):   # button[0] = deal, collidepoint(event.pos) = als er met de muis op deal geklikt wordt
                    
                    # Game wordt gestart
                    # Reset van hand, dealer en deck
                    active = True 
                    initial_deal = True # Eerste beurt worden er 2 kaarten gedeeld
                    game_deck = decks * kaart_spel # deepcopy niet direct nodig aangezien game_deck 1 lange lijst is geen nested lists bevat en de elementen strings zijn(imutabel)
                    my_hand = []            # resetten hand
                    dealer_hand = []        # reset deler hand
                    outcome = 0             # uitkomst reset
                    hand_active = True      # hand wordt actief
                    reveal_dealer = False   # reset kaarten deeler verborgen
                    add_score = True        # resset zodat score geteld kan worden       

            else: # Hier onder kijken we naar een klick op hit me als de speler score lager is dan 21 en het spel actief is
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)         # Deelt een nieuwe kaart aan speler
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:  # Als er geklikt wordt op stand stopt het spel en wordt de score deler zichtbaar
                    reveal_dealer = True        # Kaarten en score deler zichtbaar
                    hand_active = False         # Spel stopt
                elif len(buttons) == 3:
                    if buttons[2]. collidepoint(event.pos):
                        # Alles wordt gereset
                        active = True 
                        initial_deal = True 
                        game_deck = decks * kaart_spel
                        my_hand = []            
                        dealer_hand = []        
                        outcome = 0             
                        hand_active = True      
                        reveal_dealer = False   
                        add_score = True
                        dealer_score = 0
                        player_score = 0           


    # Als de speler over 21 gaat automatisch spel stoppen
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)    

    
    pygame.display.flip() #Werkt je scherm bij (je “tekent” de frame op het scherm).
pygame.quit()
