# Gamepad tester working with Scratch.
# Based on the sample code from pygame.joystick reference
# at https://www.pygame.org/docs/ref/joystick.html

# You can check information from gamepads on screen and the Scratch cat can
# receive the information via Scratch-RSP.
# python3 gamepad_tester.py -p 20   # you can change font size.

import datetime
import argparse
from array import array
import time
import sys
import struct
import unicodedata
from decimal import Decimal, ROUND_HALF_UP

import pygame
from textprint import TextPrint
import scratchRSP
from send_joystick import send_joystick, axis_value


PORT = 42001        # Scratch Remote Sensors Protocol port, never change this.
HOST = 'localhost'  # Scratch is running on my raspi.
# HOST = 'nao2g006.local'  # Scratch is at his-raspi.local or 192.168.1.22

# Process command line argument(s)
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--font_size',
                    type=int, default=20, help='font size 18 - 36')
args = parser.parse_args()
font_size = args.font_size

# Possible joystick actions
JOYSTICK_ACTIONS = (
    pygame.JOYAXISMOTION,
    pygame.JOYBUTTONDOWN,
    pygame.JOYBUTTONUP,
    pygame.JOYHATMOTION
)

# Define some colors
BLACK = (80, 80, 80)
GRAY = (180, 180, 180)
NAVY = (80, 80, 180)
PURPLE = (255, 210, 255)
WHITE = (255, 255, 255)
# for the pygame window, named Gamepad Tester
background_color = PURPLE
text_color = BLACK


def event_process():
    # EVENT PROCESSING STEP
    global done
#    global scratch
    global event
    for event in pygame.event.get():   # User did something
        # now = datetime.datetime.now()
        if event.type == pygame.QUIT:  # If user closed the window
            done = True  # Flag that we are done so we exit this loop
            print("\n\nGamepad Testerウィンドウが閉じられました。")
        # send broadcast and/or sensor-update message via Scratch-RSP
        if event.type in JOYSTICK_ACTIONS:
            if send_joystick(scratch, event):
                print("Scratchとの再接続を試みます。\n\n\n")
                wait_scratch()
    return


def drawing_window():
    # DRAWING STEP
    # Rewriting all data everytime...
    # First, clear the screen. Don't put other drawing commands
    # above this, or they will be erased with this command.
    global joystick_count
    global text_color
    global background_color

    screen.fill(background_color)
    textPrint.reset()

    textPrint.printS(
        screen, GRAY,
        "(Number of joysticks: {})[{:>2.2f}fps]"
        .format(joystick_count, clock.get_fps())
        )

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        textPrint.printSB(screen, NAVY, "Joystick {}".format(i))

        # Get the name for the controller/joystick
        name = joystick.get_name()
        textPrint.printS(screen, text_color, "Joystick name:")
        if len(name) < 31:
            textPrint.printS(screen, text_color, "  [{}]".format(name))
            textPrint.printS(screen, text_color, " ")
        else:
            textPrint.printS(screen, text_color, "  [{}".format(name[:31]))
            textPrint.printS(screen, text_color, "   {}]".format(name[31:]))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.printSB(screen, NAVY, "Number of axes: {}".format(axes))
        textPrint.indent()
        for i in range(axes):
            axis = axis_value(joystick.get_axis(i))
            textPrint.printS(screen, text_color, "Axis_{} [{}]".format(i, axis))

        textPrint.unindent()
        buttons = joystick.get_numbuttons()
        textPrint.printSB(screen, NAVY, "Number of buttons: {}".format(buttons))
        textPrint.indent()
        for i in range(buttons):
            button = joystick.get_button(i)
            if button == 1:
                button = "on"
            else:
                button = "off"
            textPrint.printS(screen, text_color, "Button_{:0>2} [{}]".format(i, button))

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        textPrint.unindent()
        hats = joystick.get_numhats()
        textPrint.printSB(screen, NAVY, "Number of hats: {}".format(hats))
        textPrint.indent()
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.printS(screen, text_color, "Hat_{}_X, Y {}".format(i, str(hat)))
        textPrint.unindent()
        textPrint.move_right()  # for the next joystick
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # Limit to n frames per second. maximum 60FPS
    clock.tick(30)


def wait_scratch():
    global scratch
    # -------- connection to Scratch -----------
    print("\nConnecting...     ", end='', flush=True)
    while True:
        scratch = scratchRSP.ScratchRSP()
        check_scratch = scratch.connect(HOST, PORT)
        if check_scratch:  # no Scrath-RSP there
            print("Press [Enter] to reconnect. Press [q] to quit.")
            ans = input("[エンター]キーを押すと再接続します。一旦終了するなら、[q]を。")
            if ans == 'q':
                sys.exit()
            print("再接続を試みます。About to retry.")
            time.sleep(0.5)
            print("")
        else:
            print("Connected to Scratch.")
            print("The cat is alive and kickin' at [{}] !!".format(HOST))
            print("[{}]で、ねこ元気です!!\n".format(HOST))
            break

def wait_joysticks():
    global joystick_count
    while joystick_count == 0:
        print(".", end='', flush=True)
        time.sleep(1)
        pygame.joystick.quit()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()


# Gamepad tester --------------------------------------------------------------
# -------- establish the connection to Scratch -----------
wait_scratch()
# -------- start PyGame to use joystick -----------
pygame.init()
# Initialize the joysticks
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("ゲームパッドが見つかりません。接続されるまで待ちます。", end="")
    wait_joysticks()
print("\nゲームパッドが{}個、接続されています。{} Gamepads connected.".format(joystick_count, joystick_count))
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    sensor_name = str(i) + "_name"
    sensor_value = joystick.get_name()
    print("Joystick {}:".format(sensor_name))
    print("  name:{}".format(sensor_value))
    scratch.sensor_update(sensor_name, sensor_value[0:sensor_value.find(' ')])
print("")

input("[エンター]キーを押してください。Press [Enter] to continue.")
print("ゲームパッド　テスター、はじまりー。 Gamepad tester started...\n")
print("このウィンドウで[ctrl-c]を押すか、Gamepad Testerウィンドウを閉じると終了します。")
print("Press ctrl-c in this window or close the Gamepad Tester window to finish.\n")

# -------- Gamepad Tester Window -----------
# Set the width and height of the screen [width,height]
size = [int(font_size * 18 * joystick_count), int(font_size * 1.1 * 30)]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gamepad Tester")
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# Get ready to print
textPrint = TextPrint(font_size)

# -------- Main Program Loop -----------
# Loop until the user clicks the close button.
done = False
while not done:
    try:
        event_process()
    except BrokenPipeError as e:
        print("切れてる！", e)
    except Exception as e:
        print("event_loop", e)
    try:
        drawing_window()
    except KeyboardInterrupt as e:
        print("\n\nctrl-cが押されました。", e)
        break
    except pygame.error as e:
        print("pygameエラー", e)
    except Exception as e:
        print("drawing_loop", e)

# -------- Finishing -----------
# Close the connection to Scratch.
scratch.close()
# Close the pygame window and quit.
pygame.quit()
print("\n", "bye...")
sys.exit()
