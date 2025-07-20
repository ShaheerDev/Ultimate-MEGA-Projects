from PIL import ImageGrab
import pyautogui
import time

print("Bot starting in 5 seconds...")
time.sleep(5)
pyautogui.click(x=100, y=700)
while True:
    # print(pyautogui.position())
    screenshot = ImageGrab.grab(bbox=(250, 640, 300, 660))
    pixels = screenshot.getdata()

    for pixel in pixels:
        if pixel[0] < 100 and pixel[1] < 100 and pixel[2] < 100:
            pyautogui.press("space")
            break