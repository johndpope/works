''' Movement and Control
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random

screen = curses.initscr()
screen.nodelay(1)
screen.border()
curses.noecho()
curses.curs_set(0)
dims = screen.getmaxyx()
height,width = dims[0]-1, dims[1]-1
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

def game():
    row = col = 2
    head = [row,col]
    body = list()
    deadcell = list()
#   body = [ head[:] ] * 5
#   deadcell = body[-1][:]
    RIGHT,DOWN,LEFT,UP = 0,1,2,3
    direction = RIGHT # 0:right, 1:down, 2:left, 3: up
    gameover = False
    length = 5

    while not gameover:

#       if deadcell not in body:
#           screen.addch(deadcell[0],deadcell[1],".")

        ''' queue
        >>> new -> [ 0->1->2->3->4 ] -> pop
        >>>        [ new->0->1->2->3 ] -> 4
        '''
        body.insert(0,head[:])
        'delete last X'
        if len(body) > length:
            deadcell = body.pop(-1)
            screen.addch(deadcell[0],deadcell[1]," ")
        screen.addch(row,col,ord('X'),curses.color_pair(1)|curses.A_REVERSE )

        action = screen.getch()
        if action == ord('k') and direction != DOWN: # 1
            # action == curses.KEY_UP
            direction = UP # 3
        elif action == ord('j') and direction != UP: # 3
            # action == curses.KEY_DOWN
            direction = DOWN # 1 
        elif action == ord('l') and direction != LEFT: #2
            # action == curses.KEY_RIGHT
            direction = RIGHT  # 2
        elif action == ord('h') and direction != RIGHT:
            # action == curses.KEY_LEFT
            direction = LEFT 

        if   direction == RIGHT:    col += +1
        elif direction == LEFT :    col += -1
        elif direction == DOWN:     row += 1
        elif direction == UP:       row += -1

        head = [row,col]

#       for i in range(len(body)-1,0,-1):
#           body[i] = body[i-1][:]
#       body[0] = head[:]

        screen.addstr(23,10,str(deadcell),curses.color_pair(0)|curses.A_REVERSE)
        screen.addstr(23,20,str(body),curses.color_pair(0)|curses.A_REVERSE)

        if screen.inch( *head ) != ord(' '): #head[0],head[1]) != ord(' '):
            gameover = True
        screen.move(height,width)
        screen.refresh()
        time.sleep(0.2)
game()
curses.endwin()
