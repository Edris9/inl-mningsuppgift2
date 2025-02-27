import random  # Importerar random-modulen för slumptal

class Grid:  # Definierar Grid-klassen för spelplanen
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """
    width = 46  # Sätter spelets bredd till 36-----> 46 rutor
    height = 22  # Sätter spelets höjd till 12-----> 22 rutor
    empty = "."  # Symbol för tom ruta
    wall = "■"   # Symbol för vägg

    def __init__(self):  # Konstruktor för Grid-klassen
        # Skapar en 2D-lista för spelplanen fylld med tomma rutor
        self.data = [[self.empty for y in range(self.width)] for z in range(self.height)]

    def is_wall(self, x, y):  # Kontrollerar om en position är en vägg
        return self.get(x, y) == self.wall

    def get(self, x, y):  # Hämtar värdet på en specifik position
        return self.data[y][x]

    def set(self, x, y, value):  # Sätter ett värde på en specifik position
        self.data[y][x] = value

    def set_player(self, player):  # Kopplar en spelare till spelplanen
        self.player = player

    def clear(self, x, y):  # Tömmer en position (sätter den till empty)
        self.set(x, y, self.empty)

    def __str__(self):  # Konverterar spelplanen till en sträng för utskrift
        xs = ""  # Initierar tom sträng för utskrift
        for y in range(len(self.data)):  # Loopar genom varje rad
            row = self.data[y]  # Hämtar aktuell rad
            for x in range(len(row)):  # Loopar genom varje kolumn
                if x == self.player.pos_x and y == self.player.pos_y:  # Kollar om positionen är spelarens position
                    xs += "@"  # Lägger till spelarsymbolen
                else:
                    xs += str(row[x])  # Lägger till rutans innehåll
            xs += "\n"  # Lägger till radbrytning efter varje rad
        return xs  # Returnerar den färdiga strängen

    def make_walls(self):  # Skapar väggar på spelplanen
        # Skapar ytterväggar vertikalt
        for i in range(self.height):
            self.set(0, i, self.wall)
            self.set(self.width - 1, i, self.wall)
        # Skapar ytterväggar horisontellt
        for j in range(1, self.width - 1):
            self.set(j, 0, self.wall)
            self.set(j, self.height - 1, self.wall)

        # Skapar vertikal vägg med öppning i mitten
        for i in range(2, self.height - 2):
            if i != self.height // 2:
                self.set(self.width // 3, i, self.wall)

        # Skapar horisontell vägg med öppning
        for j in range(self.width // 3, 2 * self.width // 3):
            if j != self.width // 2:
                self.set(j, self.height // 2, self.wall)

        # Skapar extra vertikal vägg med annan öppning
        for i in range(3, self.height - 3):
            if i != self.height // 2 + 1:
                self.set(2 * self.width // 3, i, self.wall)

    def get_random_x(self):  # Genererar slumpmässig x-koordinat
        return random.randint(0, self.width-1)

    def get_random_y(self):  # Genererar slumpmässig y-koordinat
        return random.randint(0, self.height-1)

    def is_empty(self, x, y):  # Kontrollerar om en position är tom
        return self.get(x, y) == self.empty