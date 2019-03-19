import collections
import tty
import sys
import termios


# Taken from https://stackoverflow.com/a/510364/3217409.
# For aesthetics only, input could be taken in some other way.
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


CURRENT_STATE = None

STATE_TABLE = collections.defaultdict(lambda: False)

TAPE = ""

with open("program.txt") as file_:
    for line in file_:
        if (line[:2] != "//"):
            temp = line.split()
            if (CURRENT_STATE is None):
                CURRENT_STATE = temp[0]
            if (temp[0] not in STATE_TABLE):
                STATE_TABLE[temp[0]] = collections.defaultdict(lambda: False)
            STATE_TABLE[temp[0]][temp[1]] = tuple(temp[2:5])

while True:
    character = getch()
    # Close on ctrl-c.
    if (ord(character) == 3):
        break
    if (STATE_TABLE[CURRENT_STATE][character]):
        TAPE += STATE_TABLE[CURRENT_STATE][character][1]
        CURRENT_STATE = STATE_TABLE[CURRENT_STATE][character][0]
        if (CURRENT_STATE == "f"):
            print("Accepted. Terminating.")
            break
    else:
        print("Fatal error. Turing Machine crashing.")
        break
    print(TAPE)
