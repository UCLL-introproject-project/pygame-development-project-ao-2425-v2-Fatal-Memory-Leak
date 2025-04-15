# 📋 Naslagwerk voor het Pygame project. 

In dit document zal ik de theorie die ik nodig heb om dit project te maken en moet opzoeken schematiseren. 
Dit dient als geheugen steuntje en is een mooie oefening in **marktdown**. Daarnaast kan ik het gebruiken als voorbereiding voor het examen. 
<br> 
<br> 
<br> 


# 1. 🎯 Wat zijn modules in Python?

Een **module** is in feite een Python-bestand (`.py`) dat functies, klassen, variabelen of zelfs direct uitvoerbare code bevat. Je kunt:

- Zelf modules schrijven.
- Gebruik maken van ingebouwde modules.
- Externe modules installeren van andere ontwikkelaars.


### 🧱 Types modules:

- 🔹 **Built-in modules** → zoals `random`, `math`, `datetime` (standaard beschikbaar in Python).
- 🔹 **Externe modules** → zoals `pygame`, die je installeert via `pip install pygame`.
- 🔹 **Zelfgemaakte modules** → bijvoorbeeld `mijn_utils.py` met eigen functies en logica.
<br>
<br>
<br>


## 1.1. 🃏 Modules gebruikt in het Blackjack-project

### 1.1.1. `copy`
- **Doel**: Objecten kopiëren.
- **Belangrijke functies**:
  - `copy.copy(obj)` → shallow copy (oppervlakkige kopie).
  - `copy.deepcopy(obj)` → deep copy (volledige duplicatie, ook van nested lijsten/dicts).
- **Toepassing in blackjack**: origineel deck behouden terwijl je werkt met kopieën per speler.

### Syntax:
<pre>
origineel = [[1, 2], [3, 4]]   

python shallow = copy.copy(origineel) 
shallow[0][0] = 99 print(origineel) # [[99, 2], [3, 4]] 
</pre>

### 1.1.2. `random`
- **Doel**: Willekeurigheid genereren.
- **Belangrijke functies**:
  - `random.shuffle(deck)` → schudt een deck kaarten.
  - `random.choice(lijst)` → kiest een willekeurig item.
  - `random.randint(1, 10)` → getal tussen 1 en 10.
- **Toepassing in blackjack**: random kaarten uitdelen, of bijvoorbeeld random startspeler (mogelijke uitbreiding).

### 1.1.3. `pygame`
- **Doel**: Bibliotheek voor game-ontwikkeling.
- **Bevat**:
  - Klassen zoals `pygame.Surface`, `pygame.Rect`, `pygame.sprite.Sprite`.
  - Functies voor beeld, geluid, toetsenbord- en muisinput.
  - Hulpmiddelen voor animatie, event loops en framerate control.
- **Toepassing in blackjack**: Graphical User Interface (GUI) bouwen, speelkaarten tonen, knoppen om "HIT" of "STAY" te selecteren, geluidseffecten.
<br>
<br>
<br>


## 1.2. Overzicht in tabelvorm

| Module   | Type        | Wat bevat het?                      | Toepassing in Blackjack             |
|----------|-------------|-------------------------------------|-------------------------------------|
| `copy`   | built-in     | functies (`copy`, `deepcopy`)       | Kopie van deck/speltoestand maken   |
| `random` | built-in     | functies (`shuffle`, `choice`, etc) | Kaarten schudden, random keuzes     |
| `pygame` | extern (pip) | klassen, functies voor games        | Interface, interactie, geluid       |

<br>
<br>
<br>


# 2. Uitleg methode binnen pygame
Met de uitbreiding van de **pygame module** komen er een heel aantal nieuwe methodes langs die ik nog niet kende via **python** of **JS**. 

Hieronder kort wat het verschil is tussen `fill()`, `draw`, `blit()` en `flip()` in Pygame

Deze functies zijn allemaal betrokken bij wat je op het scherm ziet, maar ze hebben elk een eigen rol:
<br>
<br>
<br>


## 2.1. 🧽 `fill()`

**Doel:** vult het hele scherm (of een deel) met een kleur.

- ✅ Gebruik je om de achtergrond te "wissen" vóór je nieuwe dingen tekent.
- 🔁 Meestal de **eerste** stap in de game-loop.
- 🧼 Werkt als een soort **reset** van je canvas.

### Syntax:
<pre>
screen.fill("black")  # Maak het scherm zwart
</pre>
<br>
<br>
<br>


## 2.2. 🎨 `draw`

**Wat het doet:** tekent vormen (rects, circles, lijnen, etc.) op een surface.

- ✅ Gebruik je om knoppen, randen, vormen, enz. te maken.  
- 📦 Onderdeel van de `pygame.draw` module (zoals `pygame.draw.rect()`).  
- ❌ Kan **geen tekst of afbeeldingen** tekenen.

### Syntax:
<pre>
pygame.draw.rect(screen, "white", [50, 50, 100, 100])  # Vierkant tekenen
</pre>
<br>
<br>
<br> 

## 2.3. ✍️ `font.render()`
**Wat het doet:** maakt een tekst-"surface" van een string die je daarna met `blit()` op het scherm kunt zetten.

✅ Gebruik je om tekst om te zetten naar iets wat je op het scherm kunt plakken.  
🎨 Je bepaalt hierbij ook meteen de kleur en of anti-aliasing aan staat.  
📄 Het resultaat is een `Surface` object — een soort afbeelding van je tekst.

### Syntax:
<pre>
tekst_surface = font.render("Je tekst hier", True, "kleur")
</pre>
- Eerste argument: de tekst die je wilt tonen (string)
- Tweede argument: anti-aliasing (True = gladde randen, False = pixelachtig)
- Derde argument: tekstkleur (kan een kleurnaam of RGB zijn)
<br>
<br>
<br> 



## 2.4. 🖼 blit()

**Wat het doet:** plaatst een andere surface (tekst, afbeelding, sprite, etc.) op je hoofdscherm.

- ✅ Gebruik je voor het tonen van tekst, afbeeldingen of sprites.

- 📌 Superbelangrijk voor alles wat niet standaard-vorm is (zoals tekst of een .png van een kaart).

- 🧷 Plakt iets op het scherm, maar maakt het nog niet zichtbaar (zie flip()).

### Syntax:
<pre>
screen.blit(tekst_surface, (100, 100))  # Tekst plaatsen
</pre>
<br>
<br>
<br>


## 2.5. 🔄 flip() (of update())
Wat het doet: maakt alles zichtbaar wat je net hebt getekend.

- ✅ Moet je aan het einde van elke frame aanroepen.

- 📺 Zonder deze zie je niks op je scherm, ook al heb je alles "getekend".

- 🔄 Zet het "buffered" scherm om naar je echte scherm (double buffering).

### Syntax:
<pre>
pygame.display.flip()  # Laat alles op het scherm zien
</pre>
<br>
<br>
<br>


## In volgorde binnen een game-loop ziet het er dus vaak zo uit:
<pre>
screen.fill("black")              # Achtergrond wissen
pygame.draw.rect(...)             # Knoppen of vormen tekenen
tekst_surface = font.render(...)  # Tekst renderen
screen.blit(text_surface, ...)    # Tekst of plaatjes plakken
pygame.display.flip()             # Alles op het scherm tonen
</pre>