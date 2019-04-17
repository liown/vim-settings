#!/usr/bin/env python
#-*-coding:utf-8 -*-
#
#Author: tony - birdaccp at gmail.com
#Create by:2018-03-21 10:44:23
#Last modified:2018-03-21 10:44:26
#Filename:security.py
#Description:

import random
import hashlib
import binascii
import string

SALT_STR = string.ascii_letters + string.digits

def generate_password(password, hash_name: str='sha256', salt_length: int=8, iterations: int=1000) -> str:
    if not isinstance(password, bytes):
        password_byte = password.encode()
    else:
        password_byte = password

    salt_str = get_random_str(salt_length)
    salt_byte = salt_str.encode()

    iterations_str = str(iterations)

    hash_body = hashlib.pbkdf2_hmac(hash_name=hash_name, salt=salt_byte, iterations=iterations, password=password_byte)
    hash_str = binascii.hexlify(hash_body).decode()

    hash_password = '{}:{}:{}:{}'.format(hash_name, salt_str, hash_str, iterations_str)
    return hash_password


def verify_password(password, hash_password):
    if not isinstance(password, bytes):
        password_byte = password.encode()
    else:
        password_byte = password

    hash_name, salt, hash_pass, iterations_str = hash_password.split(':')
    salt_byte = salt.encode()
    iterations = int(iterations_str)
    user_password_byte = hashlib.pbkdf2_hmac(password=password_byte, hash_name=hash_name, salt=salt_byte, iterations=iterations)
    user_password = binascii.hexlify(user_password_byte).decode()
    if user_password == hash_pass:
        return True
    else:
        return False


def get_random_str(length: int):
    __random = ''.join(random.sample(SALT_STR, length))
    return __random


# coding: utf8
import sys
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
import base64

class prpcrypt():
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + (' ' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(b' ')


if __name__ == '__main__':
    salt = b'\xe4\xa4\xca8\x0f\xdbE\xfc\x03\xe3S\x01\xf9tNW'
    # _iv = b'oH\xc4\x8c\\\xd8\xf4U\xf7\xf2:\xe4,\x1a\xeen'
    iv = Random.new().read(AES.block_size)
    pc = prpcrypt(salt, iv)  # 初始化密钥
    e = pc.encrypt("1234asd")

    print(e)
    # pc1 = prpcrypt(salt, _iv)
    d = pc.decrypt(e)
    print(d)