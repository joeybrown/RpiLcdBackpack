#    Copyright Paul Knox-Kennedy, 2012
#    This file is part of RpiLcdBackpack.

#    Knox-Kennedy did the hard work. Joey Brown made it a bit more Pythonified and extended the API, 2014

#    RpiLcdBackpack is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RpiLcdBackpack is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.#

import smbus
import time


class AdafruitLcd:
    # commands
    clear_display = 0x01
    return_home = 0x02  # todo: are these being used?
    entry_mode_set = 0x04  # ''
    display_control = 0x08
    cursor_shift = 0x10  # ''
    function_set = 0x20
    set_cg_ram_address = 0x40
    set_dd_ram_address = 0x80

    # flags for display entry mode #todo: are these being used?
    entry_right = 0x00
    entry_left = 0x02
    entry_shift_increment = 0x01
    entry_shift_decrement = 0x00

    # flags for display on/off control
    display_on = 0x04
    display_off = 0x00
    cursor_on = 0x02
    cursor_off = 0x00
    blink_on = 0x01
    blink_off = 0x00

    # flags for display/cursor shift
    display_move = 0x08
    cursor_move = 0x00
    move_right = 0x04
    move_left = 0x00

    # flags for function set
    eight_bit_mode = 0x10
    four_bit_mode = 0x00
    line_2 = 0x08
    line_1 = 0x00
    dots_5x10 = 0x04
    dots_5x8 = 0x00

    device_address = None
    smbus_com = None

    rs = 0x02
    e = 0x4
    data_mask = 0x78
    data_shift = 3
    light = 0x80

    line_1_text = ''
    line_2_text = ''

    def write_four_bits(self, value):
        self.data &= ~self.data_mask
        self.data |= value << self.data_shift
        self.data &= ~self.e
        self.bus.write_byte_data(self.device_address, 0x09, self.data)
        time.sleep(0.000001)
        self.data |= self.e
        self.bus.write_byte_data(self.device_address, 0x09, self.data)
        time.sleep(0.000001)
        self.data &= ~self.e
        self.bus.write_byte_data(self.device_address, 0x09, self.data)
        time.sleep(0.000101)

    def write_command(self, value):
        self.data &= ~self.rs
        self.write_four_bits(value >> 4)
        self.write_four_bits(value & 0xf)

    def write_data(self, value):
        self.data |= self.rs
        self.write_four_bits(value >> 4)
        self.write_four_bits(value & 0xf)

    def __init__(self, smbus_com=1, device_address=0x20):
        self.device_address = device_address
        self.smbus_com = smbus_com
        self.bus = smbus.SMBus(self.smbus_com)
        self.bus.write_byte_data(self.device_address, 0x00, 0x00)
        self.display_function = self.four_bit_mode | self.line_2 | self.dots_5x8
        self.display_control = self.display_control | self.display_on | self.cursor_on | self.blink_on
        self.data = 0
        self.write_four_bits(0x03)
        time.sleep(0.005)
        self.write_four_bits(0x03)
        time.sleep(0.00015)
        self.write_four_bits(0x03)
        self.write_four_bits(0x02)
        self.write_command(self.function_set | self.display_function)
        self.write_command(self.display_control)
        self.write_command(0x6)
        self.clear()

    def back_light(self, on):
        if on:
            self.data |= 0x80
        else:
            self.data &= 0x7f
        self.bus.write_byte_data(self.device_address, 0x09, self.data)

    def clear(self):
        self.write_command(self.clear_display)
        time.sleep(0.002)

    def blink(self, on):
        if on:
            self.display_control |= self.blink_on
        else:
            self.display_control &= ~self.blink_on
        self.write_command(self.display_control)

    def no_cursor(self):
        self.write_command(self.display_control)

    def cursor(self, on):
        if on:
            self.display_control |= self.cursor_on
        else:
            self.display_control &= ~self.cursor_on
        self.write_command(self.display_control)

    def message(self, text):
        self.clear()
        lines = text.split('\n')
        if len(lines) == 1:
            lines.append('')
        self.line_1_text = lines[0][:16]
        self.line_2_text = lines[1][:16]
        for char in text:
            if char == '\n':
                self.write_command(0xC0)
            else:
                self.write_data(ord(char))

    def set_line_1_text(self, text):
        self.message(text + '\n' + self.line_2_text)

    def set_line_2_text(self, text):
        self.message(self.line_1_text + '\n' + text)





