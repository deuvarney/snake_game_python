from utils.constants.constants import TYPE_SCREEN_DIMENSIONS
import utils.constants.grid as GRID

GRID_COORDINATES = list[list[tuple[int, int]]]

def get_grid_lines(screen_dimensions: TYPE_SCREEN_DIMENSIONS, line_width: int, distance: int) -> GRID_COORDINATES:
    """
    Create a list of points representing the grid lines.

    Args:
        screen_dimensions (TYPE_SCREEN_DIMENSIONS): A tuple containing the width and height of the screen.
        line_width (int): The width of the line.
        distance (int): The distance between the lines.

    Returns:
        list[tuple[int, int]]: A list of points, where each point is a tuple of x and y coordinates.
        Note: These return the coordinates along the x-axis, it is up to the user to handle filling in the height
    """

    width, height = screen_dimensions
    # print(f"width: {width}, height: {height}")

    points = []

    #  Draw x position lines
    for x_pos in range(distance, width, line_width + distance):
        points.append([
            (x_pos, 0),
            (x_pos, height),
        ])

    for y_pos in range(distance, height, line_width + distance):
        points.append([
            (0, y_pos),
            (width, y_pos),
        ])
    return points


def _custom_range(start, stop, evenStep, oddStep):
    i = start
    index = 0
    while i < stop:
        yield i
        if index % 2 == 0:
            if i + evenStep > stop: ## TODO: Hacky solution to get remainder column space, create better solution
                i = stop -1
            else:
                i += evenStep
        else:
            i += oddStep
        index += 1


def get_all_grid_cells(screen_dimensions: TYPE_SCREEN_DIMENSIONS, line_width: int, distance: int) -> list[list[GRID_COORDINATES]]:
    
    width, height = screen_dimensions

    points = []

    y_pos_list = list(_custom_range(0, height, distance, line_width))
    x_pos_list = list(_custom_range(0, width, distance, line_width))


    offset = 1

    for y_idx, y_pos in enumerate(zip(y_pos_list[::2], y_pos_list[1::2])):
        y_pos1,y_pos2 = y_pos
        row = []
        for x_idx, x_pos in enumerate(zip(x_pos_list[::2], x_pos_list[1::2])):
            x_pos1,x_pos2 = x_pos
            row.append([
                (
                    (x_pos1, y_pos1), 
                    (x_pos2 - offset, y_pos1), 
                    (x_pos1, y_pos2), 
                    (x_pos2-offset, y_pos2)
                ),
                (x_pos2 - offset) - x_pos1,
                (y_pos2 - offset) - y_pos1,
                x_idx,
                y_idx,
            ])
        points.append(row)

    return points

def get_available_grid_pos(grid_data, used_cells_rects: list[tuple[int, int]]):
    
    available_grid_pos = []
    
    for grid_row_y in grid_data:
        for grid_column_x in grid_row_y:
            _,_,_,x_idx,y_idx = grid_column_x
            grid_cell_rect = get_cell_rect(grid_data, x_idx, y_idx)
            if not grid_cell_rect in used_cells_rects:
                available_grid_pos.append((x_idx, y_idx))
    
    return available_grid_pos




def get_grid_dimension_count(grid_data):
    y_len = len(grid_data)
    x_len = len(grid_data[0])
    return x_len, y_len

def get_cell_rect(grid_data, x_idx, y_idx):
    try:
        grid_row = grid_data[y_idx]
        cell = grid_row[x_idx]
        cell_rect = (
            cell[0][0][0], # left
            cell[0][0][1], # top
            cell[1], # width
            cell[2], # height
            cell[3], # x position
            cell[4], # y position
        )
        return cell_rect
    except:
        return None

def get_cell_position(grid_data, x_idx, y_idx):
    try:
        grid_row = grid_data[y_idx]
        cell = grid_row[x_idx]
        return (cell[3], cell[4])
    except:
        return None
    
def get_next_cell_pos(grid_data, x_idx: int, y_idx: int, next_direction: str):
    next_x_idx = x_idx
    next_y_idx = y_idx
    if(next_direction == GRID.DIRECTION_UP):
        next_y_idx = y_idx - 1
    elif(next_direction == GRID.DIRECTION_DOWN):
        next_y_idx = y_idx + 1
    elif(next_direction == GRID.DIRECTION_LEFT):
        next_x_idx = x_idx - 1
    elif(next_direction == GRID.DIRECTION_RIGHT):
        next_x_idx = x_idx + 1

    grid_x_count, grid_y_count = get_grid_dimension_count(grid_data)
    # print("grid_x_count", grid_x_count, "grid_y_count", grid_y_count)

    if next_x_idx < 0 or next_x_idx >= grid_x_count:
        next_x_idx = None
    elif next_y_idx < 0 or next_y_idx >= grid_y_count:
        next_y_idx = None
    
    return (next_x_idx,next_y_idx)
    
def get_next_cell_rect(grid_data, x_idx: int, y_idx: int, next_direction: str):
    next_x_idx, next_y_idx = get_next_cell_pos(grid_data, x_idx, y_idx, next_direction)
    return get_cell_rect(grid_data, next_x_idx, next_y_idx)



