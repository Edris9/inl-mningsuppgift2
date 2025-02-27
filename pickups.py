class Item:  # Definierar Item-klassen
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="?"):  # Konstruktor med standardvärden
        self.name = name  # Sparar föremålets namn
        self.value = value  # Sparar föremålets värde
        self.symbol = symbol  # Sparar föremålets symbol

    def __str__(self):  # Metod för strängrepresentation
        return self.symbol  # Returnerar föremålets symbol


# Lista med alla föremål som kan placeras ut
pickups = [
    Item("carrot", 20),  # Skapar en morot värd 20 poäng
    Item("apple", 20),  # Skapar ett äpple värd 20 poäng
    Item("strawberry", 20),  # Skapar en jordgubbe värd 20 poäng
    Item("cherry", 20),  # Skapar ett körsbär värd 20 poäng
    Item("watermelon", 20),  # Skapar en vattenmelon värd 20 poäng
    Item("radish", 20),  # Skapar en rädisa värd 20 poäng
    Item("cucumber", 20),  # Skapar en gurka värd 20 poäng
    Item("meatball", 20),  # Skapar en köttbulle värd 20 poäng
    Item("shovel", 0, "S") # skapar en spade som inte ger poäng
]


def randomize(grid):  # Funktion för att placera ut föremål slumpmässigt
    for item in pickups:  # Loopar genom alla föremål
        while True:  # Fortsätter tills en ledig position hittas
            x = grid.get_random_x()  # Slumpar x-koordinat
            y = grid.get_random_y()  # Slumpar y-koordinat
            if grid.is_empty(x, y):  # Kontrollerar om positionen är ledig
                grid.set(x, y, item)  # Placerar föremålet
                break  # Avbryter while-loopen


class Trap(Item):  # Ny klass för fällor
    """Representerar fällor som ger minuspoäng."""
    def __init__(self, name="trap", value=-10, symbol="^"):
        super().__init__(name, value, symbol)

# Lägg till i slutet av filen
traps = [Trap("beartrap"), Trap("spikes")]

def randomize_traps(grid, num_traps=5): # Funktion för att placera ut fällor slumpmässigt
    import random
    for _ in range(num_traps): # Loopar lika många gånger som num_traps
        trap = random.choice(traps) # Slumpar en fälla
        while True:
            x = grid.get_random_x() # Slumpar x-koordinat
            y = grid.get_random_y() # Slumpar y-koordinat
            if grid.is_empty(x, y): # Kontrollerar om positionen är ledig
                grid.set(x, y, trap) # Placerar fällan
                break



class Key(Item): # Ny klass för nycklar
    """Representerar en nyckel för kistor."""
    def __init__(self, name="key", value=0, symbol="🔑"):
        super().__init__(name, value, symbol)

class Chest(Item): # Ny klass för kistor
    "Representerar en kista som öppnas med nyckel."""
    def __init__(self, name="chest", value=0, symbol="📦"):
        super().__init__(name, value, symbol)

# Skapa nycklar och kistor
keys = [Key()]
chests = [Chest()]

def randomize_keys_and_chests(grid, num_keys=1, num_chests=1): # Funktion för att placera ut nycklar och kistor slumpmässigt
    import random
    # Placera nycklar
    for _ in range(num_keys): # Loopar lika många gånger som num_keys
        key = random.choice(keys) # Slumpar en nyckel
        while True:
            x, y = grid.get_random_x(), grid.get_random_y() # Slumpar x- och y-koordinat
            if grid.is_empty(x, y): # Kontrollerar om positionen är ledig
                grid.set(x, y, key) # Placerar nyckeln
                break
    
    # Placera kistor
    for _ in range(num_chests): # Loopar lika många gånger som num_chests
        chest = random.choice(chests) # Slumpar en kista
        while True:
            x, y = grid.get_random_x(), grid.get_random_y() # Slumpar x- och y-koordinat
            if grid.is_empty(x, y): # Kontrollerar om positionen är ledig
                grid.set(x, y, chest) # Placerar kistan
                break 



class Exit(Item): # Ny klass för utgång
    """Representerar utgången från spelet."""
    def __init__(self, name="exit", value=0, symbol="E"):
        super().__init__(name, value, symbol)

# Skapa en exit
exit_point = Exit()

def place_exit(grid): # Funktion för att placera en utgång
    """Placerar en utgång på kartan."""
    while True: # Fortsätter tills en ledig position hittas
        x, y = grid.get_random_x(), grid.get_random_y() # Slumpar x- och y-koordinat
        if grid.is_empty(x, y): # Kontrollerar om positionen är ledig
            grid.set(x, y, exit_point)  
            break



class Enemy(Item): # Ny klass för fiender
    """Fiender som jagar spelaren."""
    def __init__(self, name="enemy", value=-20, symbol="👹"):
        super().__init__(name, value, symbol)

# Lägg till i slutet
enemies = [Enemy("ghost", -20, "💀"), Enemy("monster", -20, "👾"), Enemy("zombie", -20, "👹")]

def place_enemies(grid, num_enemies=2): # Funktion för att placera fiender slumpmässigt
    import random  
    from player import Player
    enemy_positions = [] # Lista för att spara fiendernas positioner
    for _ in range(num_enemies): # Loopar lika många gånger som num_enemies
        enemy = random.choice(enemies) # Slumpar en
        while True: # Fortsätter tills en ledig position hittas
            x, y = grid.get_random_x(), grid.get_random_y() # Slumpar x- och y-koordinat
            if grid.is_empty(x, y) and abs(x - grid.player.pos_x) > 3 and abs(y - grid.player.pos_y) > 3:
                grid.set(x, y, enemy)
                enemy_positions.append((x, y, enemy))
                break
    return enemy_positions




class Bomb(Item):
    """Representerar en bomb som exploderar efter 3 drag."""
    def __init__(self, name="bomb", value=-50, symbol="💣"):
        super().__init__(name, value, symbol)
        self.countdown = 3  # Antal drag innan explosion