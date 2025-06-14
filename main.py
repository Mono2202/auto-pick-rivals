import pyautogui
import cv2
import pytesseract
import time
import numpy as np

# In-game character selection screen positions in Marvel Rivals (On main display)
SUPPORT_ROLE = (1804, 442)
ULTRON_CHARACTER = (1426, 320)
CONFIRM_BUTTON = (1634, 712)
CONFIRM_BUTTON_REGION = (*CONFIRM_BUTTON, 100, 50)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def _find_current_mouse_position():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Position: ({x}, {y})", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDone.")


def check_for_confirm_button():
    screenshot = pyautogui.screenshot(region=CONFIRM_BUTTON_REGION)
    img = np.array(screenshot)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    inverted = cv2.bitwise_not(thresh)
    text = pytesseract.image_to_string(inverted, config='--psm 6')
    return 'confirm' in text.lower()


def _press_button(position: tuple[int, int]):
    pyautogui.moveTo(*position)
    pyautogui.click()


def pick_character():
    _press_button(SUPPORT_ROLE)
    time.sleep(0.1)
    _press_button(ULTRON_CHARACTER)
    time.sleep(0.1)
    _press_button(CONFIRM_BUTTON)


def main():
    while not check_for_confirm_button():
        ...
    
    pick_character()


if __name__ == "__main__":
    main()
