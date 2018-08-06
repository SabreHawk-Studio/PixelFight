# !/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Zhiquan Wang'
__date__ = '2018/7/24 22:09'

import socket
import pfmap
from pfmessage import *


class PixelFightClient(object):
    def __init__(self, *, usr_name='DefaultUser', ip=None, port=None):
        self.__server_ip = ip
        self.__server_port = port
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__usr_name = usr_name
        self.__login_id = None
        self.__pfmap = None
        self.__is_busy = False
        self.__message = None
        self.__cur_pos = [0, 0]
        self.__cur_round = 0

    def __connect(self):
        self.__client_socket.connect((self.__server_ip, self.__server_port))

    def __request(self, msg=None):
        self.__is_busy = True
        self.__client_socket.send(msg)
        data = self.__client_socket.recv(1024).decode('utf-8')
        self.__is_busy = False
        return data

    def launch_socket(self):
        self.__connect()
        while True:
            if self.__login_id is None:
                continue
            if self.__is_busy is False:
                data = self.__client_socket.recv(1024).decode('utf-8')
                print("Client Receive:" + data + ":End")
                if get_msg_type(data) == MessageType.game_info:
                    tmp_info = GameInfo(json_info=data)
                    self.attack_request(tmp_info)

    def login_request(self):
        log_req = LoginRequest(uname=self.__usr_name).dump_json().encode('utf-8')
        reply_msg = self.__request(log_req)
        if get_msg_type(reply_msg) == MessageType.login_reply:
            log_rep = LoginReply(json_info=reply_msg)
            self.__login_id = log_rep.login_id
            print("Login Succeed")
        else:
            print("Error:pfclient.login_request")

    def attack_request(self, tmp_info):
        tmp_pos = self.attack(tmp_info)
        tmp_cmd = AttackRequest(x=tmp_pos[0], y=tmp_pos[1])
        rep_msg = self.__request(tmp_cmd)
        if get_msg_type(rep_msg) == MessageType.attack_reply:
            attack_rep = AttackReply(json_info=rep_msg)
            print("Round:" + str(self.__cur_round) + " : Attack ( " + str(self.__cur_pos[0]) + " , " + str(
                self.__cur_pos[1]) + " ) " + str(attack_rep.is_suc))
        else:
            print("Error:pfclient.attack_request")

    def attack(self, tmp_info):
        attack_pos = self.__cur_pos
        # beign
        # your codes here

        # end
        self.__cur_pos = attack_pos
        return attack_pos