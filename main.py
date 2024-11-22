import pygame
from collections import namedtuple
from random import randint
from grid import get_available_grid_pos, get_grid_lines, get_all_grid_cells, get_cell_rect, get_next_cell_pos, get_next_cell_rect, get_cell_position
from utils.constants.constants import SCREEN_DIMENSIONS
import utils.constants.colours as COLOURS;
import utils.constants.grid as GRID;


class Snake:
    def __init__(self):
        self.x_pos = 6
        self.y_pos = 4
        self.cells_rects = [get_cell_rect(all_grid_cells, self.x_pos, self.y_pos)]

    @property
    def cells_rects(self):
        return self._cells_rects
    
    @cells_rects.setter
    def cells_rects(self, value):
        
        # Update the private attribute with the new value
        self._cells_rects = value
        
        # Get/Set the x and y position of the snake head in the snake's body
        if len(self.cells_rects):
            # TODO: Update usage of this to get x/y positiong of rect in the grid
            _,_,_,_, self.x_pos, self.y_pos = self.cells_rects[0]


class Food:
    def __init__(self, snake_instance: Snake):
        self.place_random(snake_instance)
    
    def place_random(self, snake_instance: Snake):
        available_cells_pos = get_available_grid_pos(all_grid_cells, snake_instance.cells_rects)
        if available_cells_pos:
            # // TODO, either use rect class or set x,y when rect is assigned from outside
            x, y = available_cells_pos[randint(0, len(available_cells_pos) - 1)]
            self.rect = get_cell_rect(all_grid_cells, x, y)

class Game:
    def __init__(self):
        self.start()

    def start(self, running=False):
        self.snake = Snake()
        self.food = Food(self.snake)

        self.score = 0
        self.running = running
        self.lost = False
        self.won = False
        self.next_direction = GRID.DIRECTION_RIGHT
        self.food.place_random(self.snake)
        
        if running:
            self.start_snake_position_timer()
    
    def update_snake_position(self, next_direction: str):
        next_cell_rect = get_next_cell_rect(all_grid_cells, self.snake.x_pos, self.snake.y_pos, next_direction)
        
        if next_cell_rect:
            # TODO: check this logic to make sure the game can actually end
            # If Next cell is avaialble, check if the snake hit itself or eats the food
            if next_cell_rect in self.snake.cells_rects:
                # Snake hit itself
                print("Hitting snake, game over!")
                self.game_over()
            else:
                z  = get_next_cell_pos(all_grid_cells, self.snake.x_pos, self.snake.y_pos, next_direction) # TODO: Function not needed, this is already included in last 2 values of rect, use class
                snake_x_pos, snake_y_pos = z

                _,_,_,_, food_cell_pos_x, food_cell_pos_y = self.food.rect
                if snake_x_pos == food_cell_pos_x and snake_y_pos == food_cell_pos_y:
                    self.snake.cells_rects = [next_cell_rect, *self.snake.cells_rects]
                        
                    available_cells_pos = get_available_grid_pos(all_grid_cells, self.snake.cells_rects)
                    if not available_cells_pos:
                        # No more cells available, the user wins
                        print('You Win!!!')
                        self.game_won()
                    else:

                        food_cell_pos_x, food_cell_pos_y = available_cells_pos[randint(0,len(available_cells_pos) -1 )]
                        food_cel_rect = get_cell_rect(all_grid_cells, food_cell_pos_x, food_cell_pos_y)
                        self.food.rect = food_cel_rect

                    self.increment_score()
                else:
                    # Advance snake
                    self.snake.cells_rects = [next_cell_rect, *self.snake.cells_rects[:-1]]
        else:
            # If No cell rect was returned, the user would hit a wall
                print("Hitting a wall, game over!")
                self.game_over()

    def game_over(self):
        self.running = False
        self.lost = True
        self.stop_snake_position_timer()

    def game_won(self):
        self.running = False
        self.won = True
        self.stop_snake_position_timer()
    
    def increment_score(self):
        self.score += 1

    def start_snake_position_timer(self):
        pygame.time.set_timer(MOVE_SNAKE_EVENT, 500)

    def stop_snake_position_timer(self):
        pygame.time.set_timer(MOVE_SNAKE_EVENT, 0)
    
    def restart_snake_position_timer(self):
        # This function will reset the running timer
        self.start_snake_position_timer()

# Initialize Pygame and create the screen
pygame.init()
pygame.display.set_caption("Fake Snake")
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)

# Fonts
score_font = pygame.font.Font(None, 18)
win_lose_font = pygame.font.Font(None, 64)
start_game_font = pygame.font.Font(None, 32)

# Grid lines and cells
grid_lines = get_grid_lines(SCREEN_DIMENSIONS, GRID.LINE_WIDTH, GRID.CELL_WIDTH)
all_grid_cells = get_all_grid_cells(SCREEN_DIMENSIONS, GRID.LINE_WIDTH, 50)

# Timers and events
MOVE_SNAKE_EVENT = pygame.USEREVENT + 1


def main():

    game = Game()
    # Create Set of pygame direction key
    pygame_direction_keys_set = { pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT }                      

    # TODO: Make this a class member
    next_direction = GRID.DIRECTION_RIGHT

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(COLOURS.TEAL)
        
        # Draw grid lines
        for start_pos, end_pos in grid_lines:
            pygame.draw.line(screen, COLOURS.BLACK, start_pos, end_pos, GRID.LINE_WIDTH)
        
        # Draw snake
        for index, snake_cell in enumerate(game.snake.cells_rects):
            color = COLOURS.SNAKE_HEAD if (index == 0) else COLOURS.GREEN
            pygame.draw.rect(screen, color, snake_cell[:4]) # Get first 4 items for x,y,w,h, TODO: Update to use a rect class

        # Draw food
        pygame.draw.rect(screen, COLOURS.FOOD, game.food.rect[:4]) # Get first 4 items for x,y,w,h, TODO: Update to use a rect class

        
        # Draw Score
        score_text = score_font.render(f"{game.score}", True, COLOURS.BLACK)  # White text
        screen.blit(score_text, (10, 10))  # 10, 10 positions it near the upper left corner
        
        if not game.running:
            start_game_text = start_game_font.render("Press [Enter] to start the game", True, COLOURS.BLACK, COLOURS.WHITE)
            screen.blit(start_game_text, (180, 400)) # TODO: Move these dimensions to a constants file

        if game.won:
            win_game_text = win_lose_font.render("You won!", True, COLOURS.GREEN, COLOURS.WHITE)
            screen.blit(win_game_text, (240, 160))

        if game.lost:
            lost_game_text = win_lose_font.render("You lost! :'\(", True, COLOURS.RED, COLOURS.WHITE)
            screen.blit(lost_game_text, (220, 160))

        pygame.display.update()

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    next_direction = GRID.DIRECTION_UP
                elif event.key == pygame.K_DOWN:
                    next_direction = GRID.DIRECTION_DOWN
                elif event.key == pygame.K_LEFT:
                    next_direction = GRID.DIRECTION_LEFT
                elif event.key == pygame.K_RIGHT:
                    next_direction = GRID.DIRECTION_RIGHT
                elif event.key == pygame.K_RETURN and not game.running:
                    next_direction = GRID.DIRECTION_RIGHT # TODO: Move this to a class member
                    game.start(True)

                # Immediately update the snake position if the snake is running and a direction key was pressed
                if  game.running and event.key in pygame_direction_keys_set:
                    game.restart_snake_position_timer() # TODO: This seems hacky, create a new class method to update the position immediately? 
                    game.update_snake_position(next_direction)
                    
            elif event.type == MOVE_SNAKE_EVENT and game.running:
                # Update snake position every time the timer ticks
                game.update_snake_position(next_direction)
            elif event.type == pygame.QUIT:
                return

if __name__ == "__main__":
    main()
