# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import socket
import struct

from Crypto.Cipher import AES
from threading import Thread

equalisers = ["Standard", "Bass", "Flat", "Boost", "Treble and Bass", "User",
              "Music", "Cinema", "Night", "News", "Voice", "ia_sound",
              "Adaptive Sound Control", "Movie", "Bass Blast", "Dolby Atmos",
              "DTS Virtual X", "Bass Boost Plus"]

STANDARD = 0
BASS = 1
FLAT = 2
BOOST = 3
TREBLE_BASS = 4
USER_EQ = 5
MUSIC = 6
CINEMA = 7
NIGHT = 8
NEWS = 9
VOICE = 10
IA_SOUND = 11
ASC = 12
MOVIE = 13
BASS_BLAST = 14
DOLBY_ATMOS = 15
DTS_VIRTUAL_X = 16
BASS_BOOST_PLUS = 17

functions = ["Wifi", "Bluetooth", "Portable", "Aux", "Optical", "CP", "HDMI",
             "ARC", "Spotify", "Optical2", "HDMI2", "HDMI3", "LG TV", "Mic",
             "Chromecast", "Optical/HDMI ARC", "LG Optical", "FM", "USB"]
WIFI = 0
BLUETOOTH = 1
PORTABLE = 2
AUX = 3
OPTICAL = 4
CP = 5
HDMI = 6
ARC = 7
SPOTIFY = 8
OPTICAL_2 = 9
HDMI_2 = 10
HDMI_3 = 11
LG_TV = 12
MIC = 13
C4A = 14
OPTICAL_HDMIARC = 15
LG_OPTICAL = 16
FM = 17
USB = 18

class temescal:
    def __init__(self, address, port=9741, callback=None, logger=None):
        self.iv = b'\'%^Ur7gy$~t+f)%@'
        self.key = b'T^&*J%^7tr~4^%^&I(o%^!jIJ__+a0 k'
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = callback
        self.logger = logger
        self.connect()
        if callback is not None:
            self.thread = Thread(target=self.listen, daemon=True)
            self.thread.start()

    def connect(self):
        self.socket.connect((self.address, self.port))
        
    def listen(self):
        while True:
            try:
                data = self.socket.recv(1)
            except Exception:
                self.connect()

            if data[0] == 0x10:
                data = self.socket.recv(4)
                length = struct.unpack(">I", data)[0]
                data = self.socket.recv(length)
                response = self.decrypt_packet(data)
                if response is not None:
                    self.callback(json.loads(response))
                    
    def encrypt_packet(self, data):
        padlen = 16 - (len(data) % 16)
        for i in range(padlen):
            data = data + chr(padlen)
        data = data.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

        encrypted = cipher.encrypt(data)
        length = len(encrypted)
        prelude = bytearray([0x10, 0x00, 0x00, 0x00, length])
        return prelude + encrypted

    def decrypt_packet(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypt = cipher.decrypt(data)
        padding = decrypt[-1:]
        decrypt = decrypt[:-ord(padding)]
        return str(decrypt, 'utf-8')

    def send_packet(self, data):
        packet = self.encrypt_packet(json.dumps(data))
        try:
            self.socket.send(packet)
        except Exception:
            try:
                self.connect()
                self.socket.send(packet)
            except Exception:
                pass

    def get_eq(self):
        data = {"cmd": "get", "msg": "EQ_VIEW_INFO"}
        self.send_packet(data)

    def set_eq(self, eq):
        data = {"cmd": "set", "data": {"i_curr_eq": eq }, "msg": "EQ_VIEW_INFO"}
        self.send_packet(data)

    def get_info(self):
        data = {"cmd": "get", "msg": "SPK_LIST_VIEW_INFO"}
        self.send_packet(data)

    def get_play(self):
        data = {"cmd": "get", "msg": "PLAY_INFO"}
        self.send_packet(data)
        
    def get_func(self):
        data = {"cmd": "get", "msg": "FUNC_VIEW_INFO"}
        self.send_packet(data)

    def get_settings(self):
        data = {"cmd": "get", "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def get_product_info(self):
        data = {"cmd": "get", "msg": "PRODUCT_INFO"}
        self.send_packet(data)

    def get_c4a_info(self):
        data = {"cmd": "get", "msg": "C4A_SETTING_INFO"}
        self.send_packet(data)

    def get_radio_info(self):
        data = {"cmd": "get", "msg": "RADIO_VIEW_INFO"}
        self.send_packet(data)

    def get_ap_info(self):
        data = {"cmd": "get", "msg": "SHARE_AP_INFO"}
        self.send_packet(data)
        
    def get_update_info(self):
        data = {"cmd": "get", "msg": "UPDATE_VIEW_INFO"}
        self.send_packet(data)

    def get_build_info(self):
        data = {"cmd": "get", "msg": "BUILD_INFO_DEV"}
        self.send_packet(data)

    def get_option_info(self):
        data = {"cmd": "get", "msg": "OPTION_INFO_DEV"}
        self.send_packet(data)

    def get_mac_info(self):
        data = {"cmd": "get", "msg": "MAC_INFO_DEV"}
        self.send_packet(data)

    def get_mem_mon_info(self):
        data = {"cmd": "get", "msg": "MEM_MON_DEV"}
        self.send_packet(data)

    def get_test_info(self):
        data = {"cmd": "get", "msg": "TEST_DEV"}
        self.send_packet(data)
    
    def test_tone(self):
        data = {"cmd": "set", "msg": "TEST_TONE_REQ"}
        self.send_packet(data)

    def set_night_mode(self, enable):
        data = {"cmd": "set", "data": {"b_night_mode": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def set_avc(self, enable):
        data = {"cmd": "set", "data": {"b_auto_vol": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def set_drc(self, enable):
        data = {"cmd": "set", "data": {"b_drc": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)
    
    def set_av_sync(self, value):
        data = {"cmd": "set", "data": {"i_av_sync": value}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def set_woofer_level(self, value):
        data = {"cmd": "set", "data": {"i_woofer_level": value}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)
    
    def set_rear_control(self, enable):
        data = {"cmd": "set", "data": {"b_rear": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def set_read_level(self, value):
        data = {"cmd": "set", "data": {"i_rear_level": value}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)
    
    def set_tv_remote(self, enable):
        data = {"cmd": "set", "data": {"i_tv_remote": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)
    
    def set_auto_power(self, enable):
        data = {"cmd": "set", "data": {"b_auto_power": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def set_auto_display(self, enable):
        data = {"cmd": "set", "data": {"b_auto_display": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def set_bt_standby(self, enable):
        data = {"cmd": "set", "data": {"b_bt_standby": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)
    
    def set_bt_restrict(self, enable):
        data = {"cmd": "set", "data": {"b_conn_bt_limit": enable}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)
    
    def set_sleep_time(self, value):
        data = {"cmd": "set", "data": {"i_sleep_time": value}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)
    
    def set_func(self, value):
        data = {"cmd": "set", "data": {"i_curr_func": value}, "msg": "FUNC_VIEW_INFO"}
        self.send_packet(data)

    def set_volume(self, value):
        data = {"cmd": "set", "data": {"i_vol": value}, "msg": "SPK_LIST_VIEW_INFO"}
        self.send_packet(data)

    def set_mute(self, enable):
        data = {"cmd": "set", "data": {"b_mute": enable}, "msg": "SPK_LIST_VIEW_INFO"}
        self.send_packet(data)

    def set_name(self, name):
        data = {"cmd": "set", "data": {"s_user_name": name}, "msg": "SETTING_VIEW_INFO"}
        self.send_packet(data)

    def set_factory(self):
        data = {"cmd": "set", "msg": "FACTORY_SET_REQ"}
        self.send_packet(data)
