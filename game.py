from grid import Grid  # Importerar Grid-klassen
from player import Player  # Importerar Player-klassen
import pickups  # Importerar pickups-modulen
import random


g = Grid()  # Skapar ny spelplan
player = Player(Grid.width // 2, Grid.height // 2, g)  # Skapar spelare i mitten av spelplanen
score = 0  # Initierar poängräkning
inventory = []  # Skapar tom lista för inventory
move_counter = 0  # Räknare för antal drag, Lägg till en ny variabel i början, efter score = 0
original_items_count = len(pickups.pickups) # Antal föremål i pickups.pickups, Lägg till en ny variabel i början, efter score = 0
collected_items = 0 # Lägg till en ny variabel i början, efter score = 0
grace_steps_remaining = 0 # Lägg till en ny variabel i början, efter score = 0
enemy_positions = []  # Lista för att spara fiendernas positioner
bombs = []  # Lista för placerade bomber


g.set_player(player)  # Kopplar spelaren till spelplanen
g.make_walls()  # Skapar väggar på spelplanen
pickups.randomize(g)  # Placerar ut föremål slumpmässigt
pickups.randomize_traps(g, 5)  # Placerar ut fällor slumpmässigt
pickups.randomize_keys_and_chests(g, 1, 1) # Placerar ut nycklar och kistor slumpmässigt
pickups.place_exit(g)
enemy_positions = pickups.place_enemies(g, random.randint(1, 3)) # Placerar ut fiender slumpmässigt



def disarm_trap():
    global score  # Lägg till denna rad
    # Kontrollera alla omgivande rutor (3x3 grid)
    traps_found = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # Skippa rutan spelaren står på
            if dx == 0 and dy == 0:
                continue
                
            check_x, check_y = player.pos_x + dx, player.pos_y + dy
            if (0 <= check_x < g.width and 0 <= check_y < g.height):
                item = g.get(check_x, check_y)
                if isinstance(item, pickups.Trap):
                    g.clear(check_x, check_y)
                    traps_found += 1
    
    if traps_found > 0:
        print(f"You disarmed {traps_found} trap(s)!")
        score += traps_found * 5  # Bonus för varje desarmerad fälla
    else:
        print("No traps nearby to disarm.")




def place_bomb():
    bomb = pickups.Bomb()
    x, y = player.pos_x, player.pos_y
    g.set(x, y, bomb)
    bombs.append((x, y, bomb))
    print("You placed a bomb! It will explode in 3 moves.")

def update_bombs():
    global score
    to_remove = []
    
    for i, (x, y, bomb) in enumerate(bombs):
        bomb.countdown -= 1
        if bomb.countdown <= 0:
            print(f"BOOM! A bomb exploded!")
            to_remove.append(i)
            
            # Explosionen påverkar 3x3 area
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    ex, ey = x + dx, y + dy
                    if 0 <= ex < g.width and 0 <= ey < g.height:
                        if ex == player.pos_x and ey == player.pos_y:
                            score -= 50
                            print("You were caught in the explosion! -50 points!")
                        g.clear(ex, ey)
    
    # Ta bort exploderade bomber
    for i in sorted(to_remove, reverse=True):
        bombs.pop(i)






def move_enemies():
    global score, enemy_positions
    for i in range(len(enemy_positions)):
        x, y, enemy = enemy_positions[i]
        if random.random() < 0.3:  # 30% chans att röra sig
            options = []
            if x < player.pos_x: options.append((1, 0))
            elif x > player.pos_x: options.append((-1, 0))
            if y < player.pos_y: options.append((0, 1))
            elif y > player.pos_y: options.append((0, -1))
            
            if options:
                dx, dy = random.choice(options)
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < g.width and 0 <= new_y < g.height and g.get(new_x, new_y) == g.empty:
                    g.clear(x, y)
                    g.set(new_x, new_y, enemy)
                    enemy_positions[i] = (new_x, new_y, enemy)
                    
                    if new_x == player.pos_x and new_y == player.pos_y:
                        score += enemy.value
                        print(f"A {enemy.name} caught you! {enemy.value} points!")



def print_status(game_grid):  # Funktion för att visa spelets status
    print("--------------------------------------")  # Skriver ut avgränsare
    print(f"You have {score} points.")  # Visar poäng
    print(game_grid)  # Visar spelplanen

def activate_grace_period(steps=5):
    global grace_steps_remaining
    grace_steps_remaining = steps
    print(f"Grace period activated! Next {steps} steps are free.")


def handle_movement(direction, jumping=False):
    global score, move_counter, collected_items, grace_steps_remaining # Lägg till global för att kunna ändra på variabler
    dx, dy = 0, 0
    if direction == "w": dy = -1 # Kontrollerar om spelaren vill gå uppåt
    elif direction == "s": dy = 1 # Kontrollerar om spelaren vill gå nedåt
    elif direction == "a": dx = -1 # Kontrollerar om spelaren vill gå vänster
    elif direction == "d": dx = 1 # Kontrollerar om spelaren vill gå höger
    next_x, next_y = player.pos_x + dx, player.pos_y + dy # Beräknar nästa position
    
    if player.can_move(dx, dy, g): # Kontrollerar om spelaren kan flytta
        player.move(direction)   # Flyttar spelaren  
        update_bombs()
        move_enemies()  # Flytta fienderna efter spelaren rört sig
        move_counter += 1 # Ökar räknaren med 1
        # Kontrollera grace period innan poängavdrag
        if grace_steps_remaining > 0:
            grace_steps_remaining -= 1
            print(f"Grace period active! ({grace_steps_remaining} steps remaining)")
        else:
            score -= 1
            print("Ouch! The floor is lava! (-1 point)")                             
        current_item = g.get(player.pos_x, player.pos_y) # Hämtar föremål på spelarens position
        if isinstance(current_item, pickups.Enemy):
                    score += current_item.value  # Minska poäng
                    print(f"You walked into a {current_item.name}! {current_item.value} points!")
        
        # Kolla om vi ska lägga till en ny frukt
        if move_counter % 25 == 0:
            import random
            new_item = random.choice(pickups.pickups)
            while True:
                x = g.get_random_x() # Slumpar x-koordinat
                y = g.get_random_y() # Slumpar y-koordinat
                if g.is_empty(x, y): # Kontrollerar om positionen är ledig
                    g.set(x, y, new_item) # Placerar föremålet
                    print(f"The fertile soil has produced a new {new_item.name}!")
                    break

        if jumping: # Om spelaren hoppar
            mid_x, mid_y = player.pos_x + dx, player.pos_y + dy # Beräknar mellanpositionen
            jump_x, jump_y = player.pos_x + (dx*2), player.pos_y + (dy*2) # Beräknar slutpositionen
            # Kontrollera om vi kan hoppa två steg
            if (0 <= jump_x < g.width and 0 <= jump_y < g.height and 
                g.get(jump_x, jump_y) != g.wall): 
                # Hoppa direkt till slutpositionen
                player.pos_x = jump_x 
                player.pos_y = jump_y
                print("You jump over a space!")
                # Hantera saker på landningsplatsen
                current_item = g.get(player.pos_x, player.pos_y)
                # Hantera föremål där spelaren landar
                score -= 1
                move_counter += 1
                return 
            else:
                print("You can't jump there! Moving normally instead.")


        
        # Kolla om nästa position är en vägg och om spelaren har en spade
        if (0 <= next_x < g.width and 0 <= next_y < g.height and 
            g.get(next_x, next_y) == g.wall):
            # Leta efter spade i inventory
            for i, item in enumerate(inventory): # Loopar genom inventory
                if item.name == "shovel": 
                    # Använd spaden
                    g.clear(next_x, next_y)
                    del inventory[i]
                    print("You used a shovel to break through the wall!")
                    break
            
        # Kolla om nästa position är en fälla
        if isinstance(current_item, pickups.Exit): # Kontrollerar om spelaren nått utgången
            if collected_items >= original_items_count: # Kontrollerar om alla föremål är samlade
                print("Congratulations! You found all items and reached the exit!")
                print(f"Final score: {score}")
                exit()  # Avsluta spelet
            else:
                print("You need to collect all items before using the exit!")

               

        elif isinstance(current_item, pickups.Item) and not isinstance(current_item, pickups.Trap) and not isinstance(current_item, pickups.Key) and not isinstance(current_item, pickups.Chest) and not isinstance(current_item, pickups.Enemy): # Kontrollerar om föremålet ger poäng
            inventory.append(current_item) # Lägger till föremålet i inventory
            score += current_item.value # Ökar poängen med föremålets värde
            collected_items += 1 # Ökar räknaren för samlade föremål
            print(f"You found a {current_item.name}, +{current_item.value} points.") # Skriver ut att föremålet hittades
            activate_grace_period() # Aktiverar grace period
            g.clear(player.pos_x, player.pos_y) # Rensar rutan


        # Kolla om nästa position är en fälla
        if isinstance(current_item, pickups.Trap): # Kontrollerar om föremålet är en fälla
            score += current_item.value # Minskar poängen med fällans värde
            print(f"You triggered a {current_item.name}! {current_item.value} points!") # Skriver ut att fällan aktiverades


            # Fällan ligger kvar, så vi rensar inte rutan
        elif isinstance(current_item, pickups.Key): # Kontrollerar om föremålet är en nyckel
            inventory.append(current_item) # Lägger till nyckeln i inventory
            print(f"You found a {current_item.name}!") # Skriver ut att nyckeln hittades
            activate_grace_period() # Aktiverar grace period
            g.clear(player.pos_x, player.pos_y) # Rensar rutan


        elif isinstance(current_item, pickups.Chest): # Kontrollerar om föremålet är en kista
            for i, item in enumerate(inventory):  # Loopar genom inventory
                if isinstance(item, pickups.Key): # Kontrollerar om föremålet är en nyckel
                    score += 100 # Ökar poängen med 100
                    print(f"You used a {item.name} to open the chest and found treasure! +100 points!") # Skriver ut att kistan öppnades
                    activate_grace_period() # Aktiverar grace period
                    del inventory[i]    # Tar bort nyckeln från inventory
                    g.clear(player.pos_x, player.pos_y) # Rensar rutan
                    break
            else:
                print("This chest is locked. You need a key to open it.")





# Lägg till en ny variabel i början, efter score = 0        
command = "" # Initierar variabel för kommando
while command not in ["q", "x"]: # Loopar tills användaren väljer att avsluta
    print_status(g) # Visar spelets status 
    command = input("Use WASD to move, J+WASD to jump, B for bomb, T for disarm trap, I for inventory, Q/X to quit. ").casefold() # Väljer kommando
    if command == "i":  # Om spelaren vill se inventory
        print("\nInventory:")  # Visar inventory-rubrik
        if not inventory:  # Om inventory är tomt
            print("Empty")  # Visar att det är tomt
        else:
            for item in inventory:  # Loopar genom alla föremål
                print(f"- {item.name}")  # Visar varje föremål
        continue  # Fortsätter loopen

    jumping = False # Initierar variabel för hopp
    move_dir = command # Sparar r
    
    if len(command) >= 2 and command[0] == "j" and command[1] in ["w", "a", "s", "d"]: # Kontrollerar om spelaren vill hoppa
        jumping = True # Sätter hopp till True 
        move_dir = command[1] # Sparar riktningen för hoppet
    
    if move_dir in ["w", "a", "s", "d"]: # Kontrollerar om riktningen är giltig
        # Modifierad handle_movement-anrop
        handle_movement(move_dir, jumping) # Flyttar spelaren

    if command == "b":
        place_bomb()
        continue

    if command == "t":
        disarm_trap()
        continue
print("Thank you for playing!")  # Avslutsmeddelande