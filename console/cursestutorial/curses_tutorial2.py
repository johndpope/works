import curses,random,time

def get_new_joke():
    import string
    li = list(string.letters)
    s = random.shuffle(li)
    li = li[:1+random.randint(0,len(li)) ]
    return ''.join(li)

screen = curses.initscr()

# Property initialize the screen
curses.noecho()
curses.cbreak()
curses.curs_set(0)

# check for and begin color support
if curses.has_colors():
    curses.start_color()
# Optionally enable the
#screen.keypad(1)

# Initialize the color combinations we're going to use
curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_BLACK, curses.COLOR_WHITE)

# BEGIN PROGRAM
height,width = curses.LINES, curses.COLS
screen.addstr(' '* (width/3) +'RANMOM QUOTES', curses.color_pair(3)|curses.A_REVERSE)
screen.chgat(-1, curses.color_pair(3)|curses.A_REVERSE)
screen.addstr(height-1,0, 'Press R to request a new quote, Q to quit')
screen.addstr(height-1,70, "{},{}".format(curses.LINES,width) )

# Change the R to green
screen.chgat(curses.LINES-1,6,1,curses.A_BOLD|curses.color_pair(2) )
# Change the Q to green
screen.chgat(curses.LINES-1,32,1,curses.A_BOLD|curses.color_pair(1))

# Set up the window to hold the random quotes
# curses.newwin(nlines, ncols, begin_row, begin_col)
quote_window = curses.newwin(curses.LINES-2, curses.COLS-2,1,1)
# set background
quote_window.bkgd(' ',curses.color_pair(4))
quote_window.refresh()

# Draw a border around the main quote window
quote_window.border(*tuple('+'*8 ) )
quote_window.addstr(1,1,'Press R to get your first quote')

screen.getch()

# Update the internal window data structures
screen.noutrefresh()
quote_window.noutrefresh()
# Redraw the screen
curses.doupdate()

# Create the event loop
while True:
    c = quote_window.getch()
    if c == ord('r') or c == ord('R'):
        quote_window.clear()
        quote_window.addstr(2,2,'Gettting quote...', curses.color_pair(3) )
        quote_window.refresh()
        quote_window.addstr(3,2,get_new_joke())
    elif c == ord('q') or c == ord('Q'):
        break

    # Refresh the window from the bottom up
    screen.noutrefresh()
    quote_window.noutrefresh()
    curses.doupdate()

# Restore the terminal setttings
curses.nocbreak()
curses.echo()
curses.curs_set(1)
# Restore the terminal itself to its 'former glory'
curses.endwin()
