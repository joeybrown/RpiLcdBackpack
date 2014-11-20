from RpiLcdBackpack import AdafruitLcd
from time import sleep

if __name__ == '__main__':
    lcd = AdafruitLcd()
    try:
        lcd.back_light(True)
        lcd.blink(False)
        lcd.cursor(False)
        lcd.clear()
        lcd.message("RpiLcd\nHello World!")
        sleep(2)
        lcd.set_line_1_text('change line 1')
        print(lcd.line_1_text)
        print(lcd.line_2_text)
        sleep(2)
        lcd.set_line_2_text('change line 2')
        sleep(2)
        lcd.message("change both!->")
        sleep(2)
        lcd.clear()
        lcd.back_light(False)
    except:
        lcd.back_light(False)
        lcd.clear()
