# Importeren van alle modules en initiatie van pygame-modules 
import random
import pygame

pygame.init() #initialiseert alle Pygame-modules
pygame.mixer.init()


#-----------------------------------------------#
#          Aanmaken van alle variabele          #
#-----------------------------------------------#

# Deck met kaarten aanmaken voor het spel
kaarten = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'B', 'V', 'K', 'A']
kaart_spel = 4 * kaarten
decks = 4 #Met hoeveel kaartspelen wordt gespeeld

# Aanmaken variabele voor de grote van het spel (pygame window/scherm)
WIDTH = 1024
HEIGHT = 700

# Afmetingen kaarten 
card_breedte = 120
card_lengte = 180
card_ruimte = 90  # Horizontale afstand tussen kaarten
text_offset_y = 15

# Positie speler en deler
player_y = 480
dealer_y = 50

# Game instellingen
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Surface-object (een soort canvas)
pygame.display.set_caption("Pygame BlackJack") # Titel voor de adressbalk 
fps = 60 # Frames per seconde
timer = pygame.time.Clock()
font = pygame.font.Font("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/marimpa/Marimpa.ttf", 44) # font-family en font-size
smaller_font = pygame.font.Font("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/marimpa/Marimpa.ttf", 36) # font-family en font-size

# Afbeeldingen inladen en alpha waarde aanpassen
background = pygame.image.load("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/images/backgroundJungleSteampunk.webp").convert_alpha()
background.set_alpha(120)  # Lichter maken
logo_image = pygame.image.load("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/images/logoSteampunkProgramar.webp").convert_alpha()
logo_scaled = pygame.transform.scale(logo_image, (350, 350))    # Grote plaatje instellen
logo_rect = logo_scaled.get_rect(center=(WIDTH // 1.5, HEIGHT // 3))    # Plaatje tekenen ten opzichte van het midden

# Geluiden inladen 
deal_hand_sound = pygame.mixer.Sound("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/gamesounds/game-start-6104.mp3")
winning_sound = pygame.mixer.Sound("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/gamesounds/goodresult-82807.mp3")
losing_sound = pygame.mixer.Sound("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/gamesounds/game-over-arcade-6435.mp3")
draw_sound = pygame.mixer.Sound("pygameDevelopmentProject/pygame-development-project-ao-2425-v2-Fatal-Memory-Leak/blackjack_game/resources/gamesounds/video-game-bonus-323603.mp3")


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



#----------------------------------#
#       Aanmaken button classe     #
#----------------------------------#


class Button:
    def __init__(self, text, x, y, width, height, font, base_color, hover_color, text_color, hover_text_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)    # Rechthoek maken voor vorm knop
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()                  # Muis volgen voor hover
        is_hovered = self.rect.collidepoint(mouse_pos)      # Als muis boven knop hover=true

        # Kleuren op basis van hover instellen
        bg_color = self.hover_color if is_hovered else self.base_color
        txt_color = self.hover_text_color if is_hovered else self.text_color

        # Teken knop en rand
        pygame.draw.rect(screen, bg_color, self.rect, 0, 5)  # knop-achtergrond
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3, 5)  # Zwarte rand knoppen

        # Teken centreren in de knoppen
        text_surface = self.font.render(self.text, True, txt_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True
        return False



#-----------------------------#
#       Functies aanmeken     #
#-----------------------------#

# Deel 1 kaart per keer random uit het game deck 
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck)-1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    # print(current_hand, current_deck)
    return current_hand, current_deck


# Kaarten tekenen op het scherm
def draw_cards(player, dealer, reveal):
    # Kaarten Speler:
    for i in range(len(player)):
        x = 50 + i * card_ruimte
        y = player_y + i * 10  # nieuwe variabele voor de aangepaste y-positie
        
        # groene kaart
        pygame.draw.rect(screen, (0, 100, 0), [x, y, card_breedte, card_lengte], 0, 5)
        
        # tekst bovenaan en onderaan de kaart
        screen.blit(font.render(player[i], True, (0, 0, 0)), (x + 10, y + text_offset_y))
        screen.blit(font.render(player[i], True, (0, 0, 0)), (x + 10, y + card_lengte - 50))
        
        # zwarte rand
        pygame.draw.rect(screen, (0, 0, 0), [x, y, card_breedte, card_lengte], 5, 5)


    # Als de spel nog niet klaar is verberg 1 kaart van de dealer
    for i in range(len(dealer)):
        # Kaarten deler
        x = 50 + i * card_ruimte
        y = dealer_y + i * 10  # nieuwe variabele voor de aangepaste y-positie
        pygame.draw.rect(screen, (144, 238, 144), [x, y, card_breedte, card_lengte], 0, 5)
        
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, (0, 0, 0)), (x + 10, y + text_offset_y))
            screen.blit(font.render(dealer[i], True, (0, 0, 0)), (x + 10, y + card_lengte - 50))
        else:
            screen.blit(font.render('??', True, (0, 0, 0)), (x + 10, y + text_offset_y))
            screen.blit(font.render('??', True, (0, 0, 0)), (x + 10, y + card_lengte - 50))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, card_breedte, card_lengte], 5, 5)

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
    screen.blit(font.render(f"Player Score: {player}", True, 'white'), (50, 400))
    if reveal_dealer:     # De score van de deler wordt alleen getoond aan het eind van het spel als reveal_dealer(=True)
            screen.blit(font.render(f"Dealer Score: {dealer}", True, 'white'), (50, 260))


# Game condities en knoppen toevoegen
def draw_game(act, record, result):
    button_list = [] # button lijst wordt geleegd door hem gelijk te stellen aan een lege lijst

    #Spel opstarten als active(=False), nieuwe hand delen
    if not act:
        # instantie van button voor DEAL HAND
        deal_button = Button(
            text="DEAL HAND",
            x= 530,
            y= 450,
            width=300,
            height= 100,
            font= font,
            base_color= (0, 100, 0),
            hover_color= (144, 238, 144),
            text_color= (0, 0, 0),
            hover_text_color= "white")

        deal_button.draw(screen) # draw() methode aanroepen
        button_list.append(deal_button) # Deal Hand op scherm

    # Als het spel gestart is geef opties voor hit and stand
    else:
        # Hit button
        hit_button = Button(
            text="HIT",
            x= 530,
            y= 620,
            width= 200,
            height= 70,
            font= font,
            base_color= (0, 100, 0),
            hover_color= (144, 238, 144),
            text_color= (0, 0, 0),
            hover_text_color= "white")
        hit_button.draw(screen)
        button_list.append(hit_button)

        # Stand button
        stand_button = Button(
            text="STAND",
            x= 750,
            y= 620,
            width= 200,
            height= 70,
            font= font,
            base_color= (0, 100, 0),
            hover_color= (144, 238, 144),
            text_color= (0, 0, 0),
            hover_text_color= "white")
        stand_button.draw(screen)
        button_list.append(stand_button)

        score_text = smaller_font.render(f"Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}", True, "white")
        screen.blit(score_text, (450, 10))

    # Als er een uitkomst is moet die op het scherm gezet worden, en komt er een herstart knop
    if result != 0:      # Als er een uitslag is
        screen.blit(font.render(results[result], True, "white"), (580, 420))

        new_hand_button = Button(
            text="NEW HAND",
            x= 580,
            y= 500,
            width= 300,
            height= 100,
            font= font,
            base_color= (0, 100, 0),
            hover_color= (144, 238, 144),
            text_color= (0, 0, 0),
            hover_text_color= "white")
        
        new_hand_button.draw(screen)
        button_list.append(new_hand_button)

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
                losing_sound.play()
            elif result == 2:               # Bij wist
                totals[0] += 1
                winning_sound.play()
            else:                           # Bij gelijkspel
                totals[2] += 1
                draw_sound.play()
            add = False

    return result, totals, add



#-----------------------------#
#        Main Game Loop       #
#-----------------------------#

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
                if buttons[0].is_clicked(event):   # button[0] = deal, in de classe methode wordt gekeken naar collidepoint(event.pos) = als er met de muis op deal geklikt wordt
                    deal_hand_sound.play()
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
                if buttons[0].is_clicked(event) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)         # Deelt een nieuwe kaart aan speler
                elif buttons[1].is_clicked(event) and not reveal_dealer:  # Als er geklikt wordt op stand stopt het spel en wordt de score deler zichtbaar
                    reveal_dealer = True        # Kaarten en score deler zichtbaar
                    hand_active = False         # Spel stopt
                elif len(buttons) == 3:
                    if buttons[2].is_clicked(event):
                        deal_hand_sound.play()
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
