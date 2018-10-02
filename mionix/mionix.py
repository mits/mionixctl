#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from enum import Enum
from device_utils import *
from profile_templates import avior7000_default_profile1
import time

MIONIX_AVIOR_7000_HID_ID = '0003:000022D4:00001308'
MIONIX_AVIOR_7000_USB_ID = ("22d4", "1308")
MIONIX_AVIOR_7000_USB_INTERFACE_NUM = 1



class Avior7000(object):

    def __init__(self, usb_id=MIONIX_AVIOR_7000_USB_ID):
        # constructor
        # needs a hidraw device
        device = open_hiddevice(usb_id, MIONIX_AVIOR_7000_USB_INTERFACE_NUM)
        self.__device = device
        # print(self.__device.getInfo())
        # print(self.__device.getName())

    def send(self, report, report_num=97):
        # send a report packet to the device
        self.__device.sendFeatureReport(report, report_num)

    def set_apply_profile(self, txt, num):
        self.set_profile(txt, num)
        time.sleep(0.1)
        self.apply_profile(num)
        # time.sleep(0.1)
        # self.send_that_other_frame(num)
        # time.sleep(0.1)
        # self.apply_profile(num)

    def set_profile(self, txt, num):
        """
        set_profile writes the profile to the mouse's memory

        :param txt: the yaml config filename
        :param num: profile slot to write to
        :return:
        """
        serial_profile = yaml.load(txt)
        profile = serial_profile.to_profile()
        buf = profile.create_profile_bytes(num)
        self.send(bytes(buf))

    def send_that_other_frame(self,  profile_num):
        """
        the official avior7000 configuration utility seems to send that,
         not sure what it does
        :param profile_num:
        :return:
        """
        if profile_num < 0 or profile_num > 4:
            raise Exception("Invalid profile number: {}". format(profile_num))
        buf = bytearray(1040)
        buf[0] = 0x08
        buf[4] = profile_num
        buf[5] = 0x01
        self.send(bytes(buf))

    def apply_profile(self, profile_num):
        if profile_num < 0 or profile_num > 4:
            raise Exception("Invalid profile number: {}". format(profile_num))
        buf2 = bytearray(63)
        buf2[0] = 0x04
        buf2[4] = profile_num
        self.send(bytes(buf2), 96)


class LedMode(Enum):
    Off = 0
    On = 1
    Selective = 2


class LedEffect(Enum):
    Solid = 1
    Blinking = 2
    Pulsating = 3
    Breathing = 4


class LedColorType(Enum):
    Single = 0
    Shifting = 0x10


class MButtonFunction(Enum):
    disabled             = 0xff00
    left_click           = 0x0001
    right_click          = 0x0002
    scroll_click         = 0x0004
    back                 = 0x0008
    forward              = 0x0010
    dpi_up               = 0x09f0
    dpi_down             = 0x09f2
    profile_switch_up    = 0x08f0
    profile_switch_down  = 0x08f2
    profile_switch_roll  = 0x08f1
    scroll_up            = 0x0101
    scroll_down          = 0x01ff
    key_a                = 0x0204
    key_b                = 0x0205
    key_c                = 0x0206
    key_d                = 0x0207
    key_e                = 0x0208
    key_f                = 0x0209
    key_g                = 0x020a
    key_h                = 0x020b
    key_i                = 0x020c
    key_j                = 0x020d
    key_k                = 0x020e
    key_l                = 0x020f
    key_m                = 0x0210
    key_n                = 0x0211
    key_o                = 0x0212
    key_p                = 0x0213
    key_q                = 0x0214
    key_r                = 0x0215
    key_s                = 0x0216
    key_t                = 0x0217
    key_u                = 0x0218
    key_v                = 0x0219
    key_w                = 0x021a
    key_x                = 0x021b
    key_y                = 0x021c
    key_z                = 0x021d
    # ...


class PollingRate(Enum):
    Rate1000 = 1
    Rate500  = 2
    Rate250  = 4
    Rate125  = 8

    @classmethod
    def to_real_val(cls, val):
        val_map = {PollingRate.Rate1000: 1000, PollingRate.Rate500: 500,
                   PollingRate.Rate250: 250, PollingRate.Rate125: 125}
        return val_map[val]

    @classmethod
    def from_real_val(cls, val):
        val_map = {1000: PollingRate.Rate1000, 500: PollingRate.Rate500,
                   250: PollingRate.Rate250, 125: PollingRate.Rate125}
        return val_map[val]

    @classmethod
    def representer(cls, dumper, data):
        return dumper.represent_scalar(u'!PollingRate', u'{}'.format(PollingRate.to_real_val(data)))

    @classmethod
    def constructor(cls, loader, node):
        value = loader.construct_scalar(node)
        return PollingRate.from_real_val(int(value))


OFFSET_PROFILE_NUM = 0x0c-8
OFFSET_PROFILE_NAME = 0x18-8
OFFSET_POLLING_RATE = 0x2c-8
OFFSET_MB_LEFT = 0x7c-8
OFFSET_MB_RIGHT = 0x83-8
OFFSET_MB_SCROLL = 0x8a-8
OFFSET_MB_SIDE_LEFT_UP = 0x91-8
OFFSET_MB_SIDE_LEFT_DOWN = 0x98-8
OFFSET_MB_MID_UP = 0x9f-8
OFFSET_MB_MID_DOWN = 0xa6-8
OFFSET_MB_SIDE_RIGHT_UP = 0xc2-8
OFFSET_MB_SIDE_RIGHT_DOWN = 0xc9-8
OFFSET_LED_SCROLLWHEEL = 0x26
OFFSET_LED_SCROLLWHEEL_EFFECT = 0x26+3
OFFSET_LED_LOGO = 0x2a
OFFSET_LED_LOGO_EFFECT = 0x2a+3


class Avior7000Profile(object):

    def __init__(self):
        # self.led_activation = LedMode.On
        self.led_effect = LedEffect.Solid
        self.button_left = MButtonFunction.left_click
        self.button_right = MButtonFunction.right_click
        self.button_wheel = MButtonFunction.scroll_click
        self.button_side_left_up = MButtonFunction.forward
        self.button_side_left_up = MButtonFunction.back
        self.button_mid_up = MButtonFunction.dpi_up
        self.button_mid_down = MButtonFunction.dpi_down
        self.button_side_right_up = MButtonFunction.disabled
        self.button_side_right_down = MButtonFunction.disabled
        self.polling_rate = PollingRate.Rate1000
        self.led_color_wheel = [0, 0, 255] #blue, cause why not
        self.led_color_logo  = [0, 0, 255]
        self.led_colortype = LedColorType.Single
        self.name = "Profile1"

    def create_profile_bytes(self, place):
        if place < 0 or place > 4:
            return None
        buf = avior7000_default_profile1[:]
        self._apply_profile_num(buf, place)
        self._apply_profile_name(buf, self.name)
        self._apply_button(buf, OFFSET_MB_LEFT, self.button_left)
        self._apply_button(buf, OFFSET_MB_RIGHT, self.button_right)
        self._apply_button(buf, OFFSET_MB_SCROLL, self.button_wheel)
        self._apply_button(buf, OFFSET_MB_SIDE_LEFT_UP, self.button_side_left_up)
        self._apply_button(buf, OFFSET_MB_SIDE_LEFT_DOWN, self.button_side_left_up)
        self._apply_button(buf, OFFSET_MB_MID_UP, self.button_mid_up)
        self._apply_button(buf, OFFSET_MB_MID_DOWN, self.button_mid_down)
        self._apply_button(buf, OFFSET_MB_SIDE_RIGHT_UP, self.button_side_right_up)
        self._apply_button(buf, OFFSET_MB_SIDE_RIGHT_DOWN, self.button_side_right_down)
        self._apply_polling_rate(buf, self.polling_rate)
        self._apply_led_color(buf, OFFSET_LED_SCROLLWHEEL, self.led_color_wheel)
        self._apply_led_color(buf, OFFSET_LED_LOGO, self.led_color_logo)
        self._apply_led_effect(buf, self.led_effect)
        self._apply_led_colortype(buf, self.led_colortype)

        # shifting color : every 3th byte is 0x11, or  | 0x10 ???
        #first two bunches are color?
        #first bunch scroll
        #second body

        #solid 1
        #blinking: every 4th byte 2
        #pulsating: 3
        #breathing 4

        return buf

    @staticmethod
    def _apply_profile_num(buf, place):
        buf[OFFSET_PROFILE_NUM] = place

    @staticmethod
    def _apply_profile_name(buf, name):
        # truncate to 15 chars
        n = name[:15]
        buf[OFFSET_PROFILE_NAME:OFFSET_PROFILE_NAME + len(n)] = bytearray(n, encoding="UTF-8")

    @staticmethod
    def _apply_button(buf, offset, func):
        if func not in MButtonFunction:
            Exception("Invalid button function selection")
        field = func.value.to_bytes(2, byteorder="big") + bytearray([0x00, 0x00, 0x00, 0x00, 0x0f])
        buf[offset: offset + 7] = bytearray(field)

    @staticmethod
    def _apply_polling_rate(buf, rate):
        if rate not in PollingRate:
            Exception("Invalid polling rate")
        buf[OFFSET_POLLING_RATE] = rate.value

    @staticmethod
    def _apply_led_color(buf, offset, color):
        if not isinstance(color, list) or not len(color) == 3:
            return
        fixedcolor = [int(max(min(255, c), 0)) for c in color]
        buf[offset:offset + 3] = bytearray(fixedcolor)

    @staticmethod
    def _apply_led_effect(buf, effect):
        buf[OFFSET_LED_SCROLLWHEEL_EFFECT] = effect.value
        buf[OFFSET_LED_LOGO_EFFECT] = effect.value

    @staticmethod
    def _apply_led_colortype(buf, type):
        if type == LedColorType.Shifting:
            buf[OFFSET_LED_SCROLLWHEEL_EFFECT] |=  0x10 # |= LedColorType.Shifting.value
            buf[OFFSET_LED_LOGO_EFFECT] |=  0x10
        else:
            buf[OFFSET_LED_SCROLLWHEEL_EFFECT] &=  0xef
            buf[OFFSET_LED_LOGO_EFFECT] &=  0xef


class Avior7000SerializableProfile(yaml.YAMLObject):
    yaml_tag = u"avior_7000_profile"

    def __init__(self, profile=Avior7000Profile()):
        if isinstance(profile, Avior7000Profile):
            # self.led_activation = profile.led_activation.name
            self.led_effect = profile.led_effect.name
            self.button_left = profile.button_left.name
            self.button_right = profile.button_right.name
            self.button_wheel = profile.button_wheel.name
            self.button_side_left_up = profile.button_side_left_up.name
            self.button_side_left_down = profile.button_side_left_up.name
            self.button_mid_up = profile.button_mid_up.name
            self.button_mid_down = profile.button_mid_down.name
            self.button_side_right_up = profile.button_side_right_up.name
            self.button_side_right_down = profile.button_side_right_down.name
            self.polling_rate = PollingRate.to_real_val(profile.polling_rate)
            self.led_colortype = profile.led_colortype.name
            self.led_color_wheel = profile.led_color_wheel
            self.led_color_logo = profile.led_color_logo
            self.name = profile.name

    def to_profile(self):
        p = Avior7000Profile()
        # p.led_activation = LedMode[self.led_activation]
        p.led_effect = LedEffect[self.led_effect]
        p.button_left = MButtonFunction[self.button_left]
        p.button_right = MButtonFunction[self.button_right]
        p.button_wheel = MButtonFunction[self.button_wheel]
        p.button_side_left_up = MButtonFunction[self.button_side_left_up]
        p.button_side_left_up = MButtonFunction[self.button_side_left_down]
        p.button_mid_up = MButtonFunction[self.button_mid_up]
        p.button_mid_down = MButtonFunction[self.button_mid_down]
        p.button_side_right_up = MButtonFunction[self.button_side_right_up]
        p.button_side_right_down = MButtonFunction[self.button_side_right_down]
        p.polling_rate = PollingRate.from_real_val(self.polling_rate)
        p.led_color_wheel = self.led_color_wheel
        p.led_color_logo = self.led_color_logo
        p.led_colortype = LedColorType[self.led_colortype]
        return p

