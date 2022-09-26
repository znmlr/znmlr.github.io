#!/usr/bin/python3
# -*- coding:utf-8 -*-
import ctypes
import platform
import os
import datetime
######################################################################
# menu
def menu():
    Logger.printBlue("-----------------请选择数字后按回车-----------------")
    Logger.printGreen("0.重新发布网站");
    Logger.printGreen("1.本地运行网站");
    Logger.printGreen("2.提交代码到git");
    Logger.printGreen("3.上传到github");
    Logger.printBlue("----------------------------------------------------")
    rst = input("请选择对应数字输入：")
    os.system("cls")
    return rst
def main():
    while True:
        deal(menu())
def deal(choice):
    switcher = {
        "0": foo0,
        "1": foo1,
        "2": foo2,
        "3": foo3
    }
    if switcher.__contains__(choice):
        switcher[choice]()
def foo0():
    Logger.printGreen("重新发布网站")
    os.system("rd public /s /q && hugo -D")
    
def foo1():
    Logger.printGreen("本地运行网站")
    os.system("http-server public -p 80")
    
def foo2():
    Logger.printGreen("提交代码到git")
    os.system("TortoiseGitProc.exe /command:commit")
    
def foo3():
    Logger.printGreen("上传到github")
    os.system("rd public /s /q && hugo -D && TortoiseGitProc.exe /command:push")
######################################################################
class Logger:
    BLUE = 0x01
    GREEN = 0x02
    RED = 0x04
    INTENSITY = 0x08
    def setCmdColor(color):
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), color)
    def resetColor():
        Logger.setCmdColor(Logger.RED | Logger.GREEN | Logger.BLUE)
    def printRed(msg):
        if platform.system().lower() == "windows":
            Logger.setCmdColor(Logger.RED | Logger.INTENSITY)
            print(msg)
            Logger.resetColor();
        elif platform.system().lower() == "linux":
            info = "\033[31m" + msg + "\033[0m";
            print(info)
    def printGreen(msg):
        if platform.system().lower() == "windows":
            Logger.setCmdColor(Logger.GREEN | Logger.INTENSITY)
            print(msg)
            Logger.resetColor();
        elif platform.system().lower() == "linux":
            info = "\033[32m" + msg + "\033[0m";
            print(info)
    def printBlue(msg):
        if platform.system().lower() == "windows":
            Logger.setCmdColor(Logger.BLUE | Logger.INTENSITY)
            print(msg)
            Logger.resetColor();
        elif platform.system().lower() == "linux":
            info = "\034[31m" + msg + "\033[0m";
            print(info)
######################################################################
main()