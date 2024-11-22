import pygame
from collections import namedtuple
from random import randint
from grid import get_available_grid_pos, get_grid_lines, get_all_grid_cells, get_cell_rect, get_next_cell_pos, get_next_cell_rect, get_cell_position
from utils.constants import COLOR_SNAKE_HEAD, COLOUR_BLACK, COLOUR_FOOD, COLOUR_RED, COLOUR_TEAL, COLOUR_GREEN, COLOUR_WHITE, GRID_CELL_WIDTH, GRID_DIRECTION_DOWN, GRID_DIRECTION_LEFT, GRID_DIRECTION_RIGHT, GRID_DIRECTION_UP, SCREEN_DIMENSIONS, GRID_LINE_WIDTH

Colour = namedtuple("Colour", ["red", "green", "blue"])

BALL_COLOUR = Colour(red=255, green=253, blue=65)
BALL_RADIUS = 20

pygame.init()
pygame.display.set_caption("Fake Snake")
clock = pygame.time.Clock()
screen = pygame.display.set_mode([640, 480])

score_font = pygame.font.Font(None, 18)
win_lose_font = pygame.font.Font(None, 64)
start_game_font = pygame.font.Font(None, 32)





MOVE_SNAKE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_SNAKE_EVENT, 500)

ball_position = [(screen.get_width() // 2), (screen.get_height() // 2)]
ball_velocity = [randint(-5, 5), randint(-5, 5)]

grid_lines = get_grid_lines(SCREEN_DIMENSIONS, GRID_LINE_WIDTH, GRID_CELL_WIDTH)
all_grid_cells = get_all_grid_cells(SCREEN_DIMENSIONS, GRID_LINE_WIDTH, 50)
snake_x_pos = 6
snake_y_pos = 4
snake_cells_rects = [get_cell_rect(all_grid_cells, snake_x_pos, snake_y_pos)]

available_cells_pos = get_available_grid_pos(all_grid_cells, snake_cells_rects)

food_cell_pos_x, food_cell_pos_y = available_cells_pos[randint(0,len(available_cells_pos) -1 )]
food_cel_rect = get_cell_rect(all_grid_cells, food_cell_pos_x, food_cell_pos_y)

game_running = False
game_lost = False
game_won = False

score = 0


def move_snake(next_move_direction: str) -> None:
    global snake_x_pos
    global snake_y_pos
    global snake_cells_rects
    global food_cell_pos_x
    global food_cell_pos_y
    global food_cel_rect
    global score

    next_cell_rect = get_next_cell_rect(all_grid_cells, snake_x_pos, snake_y_pos, next_move_direction)
    # print('next_cell_rect:', next_cell_rect)
    if next_cell_rect:

        if next_cell_rect in snake_cells_rects:
            print("Hitting snake, game over!")
            play_game_lost()
        else:
            snake_x_pos, snake_y_pos = get_next_cell_pos(all_grid_cells, snake_x_pos, snake_y_pos, next_move_direction)

            if snake_x_pos == food_cell_pos_x and snake_y_pos == food_cell_pos_y:
                snake_cells_rects = [next_cell_rect, *snake_cells_rects]
                    
                available_cells_pos = get_available_grid_pos(all_grid_cells, snake_cells_rects)
                if not available_cells_pos:
                    print('You Win!!!')
                    play_game_won()
                else:
                    food_cell_pos_x, food_cell_pos_y = available_cells_pos[randint(0,len(available_cells_pos) -1 )]
                    food_cel_rect = get_cell_rect(all_grid_cells, food_cell_pos_x, food_cell_pos_y)
                score += 1
            else:
                # Advance snake
                snake_cells_rects = [next_cell_rect, *snake_cells_rects[:-1]]
    else:
            print("Hitting a wall, game over!")
            play_game_lost()

def play_game_lost():
    global game_running
    global game_lost

    game_running = False
    game_lost = True

def play_game_won():
    global game_running
    global game_won

    game_running = False
    game_won = True

def restart_game():

    global score
    global game_running
    global game_lost
    global game_won
    global next_direction

    global snake_x_pos
    global snake_y_pos
    global snake_cells_rects
    global available_cells_pos
    global food_cell_pos_x
    global food_cell_pos_y
    global food_cel_rect
        
    score = 0
    game_running = True
    game_lost = False
    game_won = False
    next_direction = GRID_DIRECTION_RIGHT

    snake_x_pos = 6
    snake_y_pos = 4
    snake_cells_rects = [get_cell_rect(all_grid_cells, snake_x_pos, snake_y_pos)]

    available_cells_pos = get_available_grid_pos(all_grid_cells, snake_cells_rects)

    food_cell_pos_x, food_cell_pos_y = available_cells_pos[randint(0,len(available_cells_pos) -1 )]
    food_cel_rect = get_cell_rect(all_grid_cells, food_cell_pos_x, food_cell_pos_y)


def main():

    next_direction = GRID_DIRECTION_RIGHT

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(COLOUR_TEAL)
        pygame.draw.circle(screen, BALL_COLOUR, ball_position, BALL_RADIUS)
        # pygame.draw.lines(screen, COLOUR_BLACK, False, grid_lines, GRID_LINE_WIDTH)
        
        # Draw grid lines
        for start_pos, end_pos in grid_lines:
            pygame.draw.line(screen, COLOUR_BLACK, start_pos, end_pos, GRID_LINE_WIDTH)


        # if(next_direction):
        #     move_snake(next_direction)
        #     # next_direction = None
        
        # Draw snake
        for index, snake_cell in enumerate(snake_cells_rects):
            color = COLOR_SNAKE_HEAD if (index == 0) else COLOUR_GREEN
            pygame.draw.rect(screen, color, snake_cell)

        # Draw food
        pygame.draw.rect(screen, COLOUR_FOOD, food_cel_rect)

        
        # Draw Score
        score_text = score_font.render(f"{score}", True, COLOUR_BLACK)  # White text
        screen.blit(score_text, (10, 10))  # 10, 10 positions it near the upper left corner
        
        if not game_running:
            start_game_text = start_game_font.render("Press [Enter] to start the game", True, COLOUR_BLACK, COLOUR_WHITE)
            screen.blit(start_game_text, (180, 400))

        if game_won:
            win_game_text = win_lose_font.render("You won!", True, COLOUR_GREEN, COLOUR_WHITE)
            screen.blit(win_game_text, (240, 160))

        if game_lost:
            lost_game_text = win_lose_font.render("You lost! :'(", True, COLOUR_RED, COLOUR_WHITE)
            screen.blit(lost_game_text, (220, 160))

        pygame.display.update()

        # Check for left and right collisions
        if ball_position[0] - BALL_RADIUS < 0:
            ball_velocity[0] = -ball_velocity[0]
        elif ball_position[0] + BALL_RADIUS > screen.get_width():
            ball_velocity[0] = -ball_velocity[0]

        # Check for top and bottom collisions
        if ball_position[1] - BALL_RADIUS < 0:
            ball_velocity[1] = -ball_velocity[1]
        elif ball_position[1] + BALL_RADIUS > screen.get_height():
            ball_velocity[1] = -ball_velocity[1]

        ball_position[0] += ball_velocity[0]
        ball_position[1] += ball_velocity[1]

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # print('event key:', event)
                if event.key == pygame.K_UP: # Up
                    next_direction = GRID_DIRECTION_UP
                elif  event.key == pygame.K_DOWN: # Down
                    next_direction = GRID_DIRECTION_DOWN
                elif event.key == pygame.K_LEFT: # Left
                    next_direction = GRID_DIRECTION_LEFT
                elif event.key == pygame.K_RIGHT: # Right
                    next_direction = GRID_DIRECTION_RIGHT
                elif event.key == pygame.K_RETURN and not game_running:
                    restart_game()
            elif event.type == MOVE_SNAKE_EVENT and game_running:
                move_snake(next_direction)
            elif event.type == pygame.QUIT:
                return

main()
