import collections
import tty
import sys
import termios
import time


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


current_state = None

state_table = collections.defaultdict(lambda: False)

tape = ""
head_index = 0

with open("program.txt") as file_:
    for line in file_:
        if (line[:2] != "//"):
            temp = line.split()
            if (current_state is None):
                current_state = temp[0]
            if (temp[0] not in state_table):
                state_table[temp[0]] = collections.defaultdict(lambda: False)
            state_table[temp[0]][temp[1]] = tuple(temp[2:5])

# character = getch()
print("Program is running. Head is signified by @.")
while True:
    time.sleep(.1)
    # print(head_index, len(tape))
    print("Tape is currently:\n" + tape[:head_index] + "@" + tape[head_index:])
    if (head_index < 0):
        print("Fatal error. Terminating.")
        break
    if (head_index == len(tape)):
        print("Waiting for input. Use B for blank.")
        character = getch()
    else:
        character = tape[head_index]
    # print(character)
    # Close on ctrl-c.
    if (ord(character) == 3):
        break
    print("Tape head is reading:", character)
    if (state_table[current_state][character]):
        if (head_index == len(tape)):
            tape += state_table[current_state][character][1]
        else:
            tape = (tape[:head_index] +
                    state_table[current_state][character][1] +
                    tape[head_index + 1:]
                    )
        direction = state_table[current_state][character][2]
        current_state = state_table[current_state][character][0]
        if (direction == "R"):
            head_index += 1
        elif (direction == "L"):
            head_index -= 1
        else:
            print("Fatal error. Terminating.")
            break
        if (current_state == "f"):
            # print(tape)
            print("Final state reads:")
            print(tape[:head_index] + "@" + tape[head_index:])
            print("Accepted. Terminating.")
            break
    else:
        print("Fatal error. Terminating.")
        break
    # print(tape)
