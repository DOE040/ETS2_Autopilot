import vgamepad as vg
import time

gamepad = vg.VX360Gamepad()

# press a button to wake the device up
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)


while True:
    gamepad.right_trigger(value=150)
    gamepad.left_trigger(value=0)
    gamepad.update()
    time.sleep(1)
    gamepad.right_trigger(value=0)
    gamepad.left_trigger(value=150)
    gamepad.update()
    time.sleep(1)
