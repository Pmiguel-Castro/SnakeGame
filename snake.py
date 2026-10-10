import curses
from collections import deque
from random import randint 

def grab_apple(snake, height, width):
    in_snake = True
    while in_snake:
        apple = (randint(0, width-1), randint(0, height-1))
        if apple not in snake: 
            in_snake = False
    return apple

def walk(snake, is_horizontal, is_positive):
    snk_head_x, snk_head_y = snake[-1]
    if is_horizontal == False and is_positive == True:
        snake.append((snk_head_x, snk_head_y+1))
    elif is_horizontal == False and is_positive == False:
        snake.append((snk_head_x, snk_head_y-1))
    elif is_horizontal == True and is_positive == True:
        snake.append((snk_head_x+1, snk_head_y))
    else:
        snake.append((snk_head_x-1, snk_head_y))
    
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    height = 10
    width = 10
    snake = deque([(0,0)])
    apple = (randint(1, width-1), randint(1, height-1))
    alive = True
    win = False
    is_horizontal = False
    is_positive = True

    while alive and not win:
        action = stdscr.getch()
        
        if action == curses.KEY_UP:
            is_horizontal = False
            is_positive = False
        elif action == curses.KEY_DOWN:
            is_horizontal = False
            is_positive = True
        elif action == curses.KEY_RIGHT:
            is_horizontal = True
            is_positive = True
        elif action == curses.KEY_LEFT:
            is_horizontal = True
            is_positive = False
        
        walk(snake, is_horizontal, is_positive)
        
        for i in range(len(snake)-1):
            if snake[-1] == snake[i]:
                alive = False
        if snake[-1] == apple:
            apple = grab_apple(snake, height, width)
        elif snake[-1][0] > 9 or snake[-1][1] > 9 or snake[-1][0] < 0 or snake[-1][1] < 0:
            alive = False 
            break
        elif len(snake) == 100:
            win = True
            break
        else:
            snake.popleft()

        stdscr.clear()
        stdscr.addch(apple[1]+1, apple[0]+1, "*")
        for snk_part in snake:
            stdscr.addch(snk_part[1]+1, snk_part[0]+1, "#")
        for i in range(12):
            stdscr.addch(0, i, "□")
            stdscr.addch(11, i, "□")
            stdscr.addch(i, 11, "□")
            stdscr.addch(i, 0, "□")
        stdscr.refresh()

    if not alive:
        print("You died!")
    elif win:
        print("You win!")

if __name__ == "__main__":
    curses.wrapper(main)