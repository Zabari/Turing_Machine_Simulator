import collections
import tty
import sys
import termios
import time
import os


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
# End copy paste


# If you would rather not use stackoverflow code, or above function does not
# work on your system, comment it out and uncomment code below.
# def getch():
#     character = (
#         input("Please input one character. Use return key to submit.\n")
#     )
#     while (len(character) > 1):
#         print("Please input only one character.")
#         character = input()
#     return character


current_state = None
state_table = collections.defaultdict(lambda: False)
tape = ""
head_index = 0
file_path = input("Please enter program file path: ")

while (not os.path.isfile(file_path)):
    print("That file does not exist.")
    file_path = input("Please enter program file path: ")

with open(file_path) as file_:
    for line in file_:
        if (line[:2] != "//"):
            temp = line.split()
            if (current_state is None):
                current_state = temp[0]
            if (temp[0] not in state_table):
                state_table[temp[0]] = collections.defaultdict(lambda: False)
            state_table[temp[0]][temp[1]] = tuple(temp[2:5])

print("Program is running. Head is signified by (q<state number>).")
while True:
    # Sleeps for aesthetics.
    time.sleep(.1)
    print(
        "Tape is currently:\n" +
        tape[:head_index] +
        f"(q{current_state})" + tape[head_index:]
    )
    # Tape is only infinite in one direction, so if head is trying to move
    # past the left edge.
    if (head_index < 0):
        print("Fatal error. Terminating.")
        break
    # If head is at the right end of the tape.
    if (head_index == len(tape)):
        print("Waiting for input. Use B for blank.")
        character = getch()
    # If the head is somewhere else.
    else:
        character = tape[head_index]
    # Close on ctrl-c.
    if (ord(character) == 3):
        break
    print("Tape head is reading:", character)
    # If the state has a transition for the given input.
    if (state_table[current_state][character]):
        # If at right edge, just add to tape.
        if (head_index == len(tape)):
            tape += state_table[current_state][character][1]
        # Otherwise, write in place.
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
        # If there is somehow a mistake in the direction.
        else:
            print("Fatal error. Terminating.")
            break
        # At final state, print tape and exit.
        if (current_state == "f"):
            print("Final state reads:")
            print(
                tape[:head_index] +
                f"(q{current_state})" + tape[head_index:]
            )
            print("Accepted. Terminating.")
            break
    # If no transition for given input exists at state.
    else:
        print("Fatal error. Terminating.")
        break
