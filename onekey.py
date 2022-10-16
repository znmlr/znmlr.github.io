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
    Logger.printGreen("1.创建章节");
    Logger.printGreen("2.创建文章");
    Logger.printGreen("3.本地运行网站");
    Logger.printGreen("4.提交代码到git");
    Logger.printGreen("5.上传到github");
    Logger.printBlue("----------------------------------------------------")
    rst = input("请选择对应数字输入：")
    os.system("cls")
    return rst
    
def main():
    while True:
        os.system("title 杨云召的技术博客")
        deal(menu())
        
def deal(choice):
    switcher = {
        "0": republish,
        "1": createChapter,
        "2": createArticle,
        "3": runLocally,
        "4": gitCommit,
        "5": gitSync
    }
    if switcher.__contains__(choice):
        switcher[choice]()
    os.system("title 杨云召的技术博客")
    
def republish():
    Logger.printGreen("重新发布网站")
    os.system("rd public /s /q")
    os.system("hugo -D")
    
def runLocally():
    Logger.printGreen("本地运行网站")
    os.system("rd public /s /q")
    os.system("hugo -D")
    os.system("http-server public -p 80")
    
def gitCommit():
    Logger.printGreen("提交代码到git")
    os.system("TortoiseGitProc.exe /command:commit")
    
def gitSync():
    Logger.printGreen("上传到github")
    os.system("TortoiseGitProc.exe /command:push")
    
def createChapter():
    Logger.printGreen("创建章节")
    info = input("请输入路径及章节名：")
    os.system("hugo new --kind chapter " + info)
    
def createArticle():
    Logger.printGreen("创建文章")
    info = input("请输入路径及文章名：")
    os.system("hugo new " + info)
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