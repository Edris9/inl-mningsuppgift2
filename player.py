class Player:  # Definierar Player-klassen
    marker = "@"  # Symbol som representerar spelaren på spelplanen

    def __init__(self, x, y, grid):  # Konstruktor som tar startposition och spelplan
        self.pos_x = x  # Sparar spelarens x-position
        self.pos_y = y  # Sparar spelarens y-position
        self.grid = grid  # Sparar referens till spelplanen

    def move(self, direction):  # Metod för att flytta spelaren
        new_x, new_y = self.pos_x, self.pos_y  # Sparar nuvarande position
        if direction == 'w': new_y -= 1  # Flyttar uppåt
        elif direction == 's': new_y += 1  # Flyttar nedåt
        elif direction == 'a': new_x -= 1  # Flyttar vänster
        elif direction == 'd': new_x += 1  # Flyttar höger
        
        if (0 <= new_x < self.grid.width and  # Kontrollerar om ny position är inom spelplanens bredd
            0 <= new_y < self.grid.height and  # Kontrollerar om ny position är inom spelplanens höjd
            self.grid.get(new_x, new_y) != self.grid.wall):  # Kontrollerar om ny position inte är en vägg
            self.pos_x = new_x  # Uppdaterar x-position
            self.pos_y = new_y  # Uppdaterar y-position

    def can_move(self, dx, dy, grid):  # Metod som kontrollerar om spelaren kan flytta
        new_x = self.pos_x + dx  # Beräknar ny x-position
        new_y = self.pos_y + dy  # Beräknar ny y-position
        return (0 <= new_x < grid.width and  # Kontrollerar om ny position är inom spelplanens bredd
                0 <= new_y < grid.height and  # Kontrollerar om ny position är inom spelplanens höjd
                grid.get(new_x, new_y) != grid.wall)  # Kontrollerar om ny position inte är en vägg