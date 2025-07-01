from typing import List, Literal, Tuple
from pynput import mouse, keyboard
import pyautogui
import pyperclip
from matplotlib import pyplot as plt

from time import sleep

mode: Literal["start"] | Literal["recording"] | Literal["playing"] | Literal["ended"] = "start"

recorded_positions: List[List[Tuple[int, int]]] = []

values: List[str] = []
end_values: List[int] = []


def end():
    global values, end_values

    for val in values:
        try:
            end_values.append(int(val.replace(",", ".")))
        except ValueError:
            print(f"Couldn't make {val} to a number!")

    print(end_values)
    plt.plot(end_values)
    plt.show()


def play():
    global recorded_positions

    for pos in recorded_positions:
        if pos[0] == pos[1]:
            pyautogui.moveTo(pos[0])
            pyautogui.leftClick()
            sleep(0.3)
            continue

        pyautogui.moveTo(pos[0])
        pyautogui.dragTo(pos[1], duration=0.2, button="left")
        sleep(0.2)
        pyautogui.hotkey("ctrl", "c")
        sleep(0.2)
        values.append(pyperclip.paste().strip())


def on_click_key(key):
    global mode, recorded_positions
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        if key.char == "r":
            mode = "recording"
            recorded_positions = []
        elif key.char == "p":
            mode = "playing"
            play()
        elif key.char == "e":
            mode = "ended"
            end()

    except AttributeError:
        print('special key {0} pressed'.format(key))
        if key == keyboard.Key.esc:
            print(recorded_positions)
            print(values)
            print("Exiting...")
            raise Exception("Exiting")


def on_click_mouse(x, y, button, pressed):

    if pressed and str(button) == "Button.left":
        print(f"left button at {x}, {y}")
        if mode == "recording":
            recorded_positions.append([(x, y)])
    if not pressed and str(button) == "Button.left":
        print(f"left button ending at {x}, {y}")
        if mode == "recording":
            recorded_positions[-1].append((x, y))


with mouse.Listener(on_click=on_click_mouse) as listener, keyboard.Listener(on_press=on_click_key) as listener_keyboard:
    try:
        listener_keyboard.join()
        listener.join()
    except Exception as e:
        print(e)
        listener_keyboard.stop()
        listener.stop()
