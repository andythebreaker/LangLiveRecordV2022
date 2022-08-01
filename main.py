#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time
import threading
import configparser
import json
import os
import signal
import subprocess

from tkinter import *
from tkinter import ttk
from time import sleep

#直播成員資料類別
class MemberData(object):

    def __init__(self, live_id, live_key, live_url, nickname, pfid, hot_val):
        self.__live_id = live_id
        self.__live_key = live_key
        self.__live_url = "https://video-wshls.langlive.com/live/" + self.__live_id + "/playlist.m3u8"
        self.__live_url_ano = "http://video-hls.langlive.com/live/" + self.__live_id + "/online.m3u8"
        self.__nickname = nickname
        self.__pfid = pfid
        self.__hot_val = hot_val
        self.__isLive = True
        #self.__isRequ = False
        self.__isRecording = False

    def setLiveId(self, live_id):
        self.__live_id = live_id

    def setLiveKey(self, live_key):
        self.__live_key = live_key

    def setLiveUrl(self, live_url):
        self.__live_url = live_url

    def setNickname(self, nickname):
        self.__nickname = nickname

    def setPfId(self, pfid):
        self.__pfid = pfid

    def setHotVal(self, hot_val):
        self.__hot_val = hot_val

    def setIsLive(self, isLive):
        self.__isLive = isLive

    #def setIsRequ(self, isRequ):
     #   self.__isRequ = isRequ

    def setIsRecording(self, isRecording):
        self.__isRecording = isRecording

    def getLiveId(self):
        return self.__live_id

    def getLiveKey(self):
        return self.__live_key

    def getLiveUrl(self):
        return self.__live_url

    def getLiveUrlAno(self):
        return self.__live_url_ano

    def getNickname(self):
        return self.__nickname

    def getPfid(self):
        return self.__pfid

    def getHotVal(self):
        return self.__hot_val

    def getIsLive(self):
        return self.__isLive

    #def getIsRequ(self):
    #    return self.__isRequ

    def getIsRecording(self):
        return self.__isRecording

#直播錄製執行緒類別(未使用)
class LiveRecording(threading.Thread):

    def __init__(self, mId):
        threading.Thread.__init__(self)
        self.__mId = mId
        self.__cmd = ''

    def run(self):
        if requests.get(LiveMemberData[id].getLiveUrl()).status_code == 200:
            recvCmd = subprocess.Popen("ffmpeg -i \"" + LiveMemberData[self.__mId].getLiveUrl() +
                                        "\" -c copy " + memberIdJson[self.__mId] + "_" +
                                        time.strftime("%Y-%m-%d_%H-%M-%S",
                                        time.localtime()) + ".ts",
                                        shell=True,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
        else:
            recvCmd = subprocess.Popen("ffmpeg -i \"" + LiveMemberData[self.__mId].getLiveUrlAno() +
                                        "\" -c copy " + memberIdJson[self.__mId] + "_" +
                                        time.strftime("%Y-%m-%d_%H-%M-%S",
                                        time.localtime()) + ".ts",
                                        shell=True,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
        while True:
            str = recvCmd.stdout.readline().decode('big5')
            if str is not '':
                self.__cmd = str
            threading.Thread(sleep(0.01))

    def getCom(self):
        return self.__cmd

class ScanLiveMember():

    def __init__(self):
        self.__liveMemberJson = None
        self.__liveMemberSum = None
        self.__subMemberArray = None

    #讀取直播中成員資料
    def getLiveMember(self):
        global LiveMemberData
        LiveMemberData = {}
        url = 'https://api.lang.live/langweb/v1/home/class_list?psize=40&id=3-100002'
        Mres = requests.post(url)
        #Msoup = BeautifulSoup(Mres.text, "html.parser")
        jsonObj = json.loads(Mres.text)
        #jsonStr = json.dumps(jsonObj, sort_keys=False, indent=6, ensure_ascii=False)
        self.__liveMemberSum = len(jsonObj['data']['list'])
        self.__liveMemberJson = jsonObj['data']['list']
        #將直播資料存入類別陣列
        if self.getLiveMemberSum() > 0:
            for i in range(0, self.getLiveMemberSum()):
                if str(self.getLiveMemberData()[i]['pfid']) not in LiveMemberData:
                    memberData = MemberData(str(self.getLiveMemberData()[i]['live_id']),
                                            str(self.getLiveMemberData()[i]['live_key']),
                                            str(self.getLiveMemberData()[i]['live_url']),
                                            str(self.getLiveMemberData()[i]['nickname']),
                                            str(self.getLiveMemberData()[i]['pfid']),
                                            str(self.getLiveMemberData()[i]['hot_val']))
                    LiveMemberData[str(self.getLiveMemberData()[i]['pfid'])] = memberData
        else:
            print("No One is Liveing")

    def getLiveMemberData(self):
        return self.__liveMemberJson

    def getLiveMemberSum(self):
        return self.__liveMemberSum

class LangLiveWindow(Frame):

    def __init__(self, win):
        Frame.__init__(self, win)
        self.win = win
        self.place(anchor=CENTER)
        self.WindowInit()
        self.j = 0
        self.thr = {}

    #視窗物件建立
    def WindowInit(self):
        self.win.title('LangLiveRecord')
        #self.win.geometry('600x300')
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.resizable(width=False, height=False)
        self.win.config(background="lavender")

        self.subscribe_button = Button(self.win, text='訂閱成員')
        #self.subscribe_button = Button(self.win, text='訂閱成員', command=self.update_data)
        self.subscribe_button.grid(row=1, column=1, sticky=W, pady=10)

        self.setting_button = Button(self.win, text='設定')
        self.setting_button.grid(row=1, column=4, columnspan=2, sticky=E, pady=10)

        self.member_table = ttk.Treeview(self.win, show="headings", columns=('#0','#1','#2','#3','#4'))
        self.member_table.place(width=500)
        self.member_vbar = ttk.Scrollbar(self.win, orient=VERTICAL, command=self.member_table.yview)
        self.member_table.configure(yscrollcommand=self.member_vbar.set)
        self.member_table.heading('#0', text='編號')  # 是否預約
        self.member_table.heading('#1', text='預約')  # 是否預約
        self.member_table.heading('#2', text='成員')  # 姓名
        self.member_table.heading('#3', text='直播')  # 直播情況
        self.member_table.heading('#4', text='直播熱度')  # 直播熱度
        self.member_table.heading('#5', text='錄製')  # 錄製中&錄製訊息
        self.member_table.column('#0', width=50, anchor='center', stretch=0)  # 是否預約
        self.member_table.column('#1', width=100, anchor='center', stretch=0)#是否預約
        self.member_table.column('#2', width=100, anchor='center', stretch=0)#姓名
        self.member_table.column('#3', width=100, anchor='center', stretch=0)#直播情況
        self.member_table.column('#4', width=100, anchor='center', stretch=0)#直播熱度
        self.member_table.column('#5', width=100, anchor='center', stretch=0)#錄製中&錄製訊息
        self.member_table.grid(row=2, column=1, columnspan=4, sticky=NSEW)
        self.member_vbar.grid(row=2, column=5, sticky=NS)

        self.frame_top = Frame(width=400, height=10)
        self.frame_button = Frame(width=400, height=20)
        self.frame_left = Frame(width=20, height=250)
        self.frame_right = Frame(width=20, height=250)

        self.frame_top.grid(row=0, column=0, columnspan=5)
        self.frame_button.grid(row=3, column=0, columnspan=5)
        self.frame_left.grid(row=1, column=0, rowspan=2)
        self.frame_right.grid(row=1, column=6, rowspan=2)

        self.frame_top.config(background="lavender")
        self.frame_button.config(background="lavender")
        self.frame_left.config(background="lavender")
        self.frame_right.config(background="lavender")

        self.frame_top.grid_propagate(0)
        self.frame_button.grid_propagate(0)
        self.frame_left.grid_propagate(0)
        self.frame_right.grid_propagate(0)

        self.member_table_count = 0

    #初始化成員列表
    def init_data(self):
        for i in range(0, len(memberIdArray) - 1):
            self.member_table.insert('', 'end', text=self.member_table_count, value=('', memberIdArray[i][0], '', '', ''))

    '''def insert_data(self, mId, index):
        global LiveMemberData
        readyToRecord = False
        if mId in self.__subMemberArray:
            readyToRecord = True
        if mId in LiveMemberData:
            record = ''
            if readyToRecord is True and mId not in self.thr:
                print(mId)
                self.thr[mId] = threading.Thread(target=test, args=[mId])
                self.thr[mId].start()

                #self.thr[mId] = LiveRecording(mId)
                #self.thr[mId].start()

                print(self.thr[mId])
            elif mId in self.thr:
                record = '錄製中'
            self.member_table.insert('', index, text=self.member_table_count, value=(
            0, LiveMemberData[mId].getNickname(), '直播中', LiveMemberData[mId].getHotVal(), record))
        else:
            self.member_table.insert('', index, text=self.member_table_count, value=(0, memberIdJson[mId], '', '', ''))
        self.member_table_count += 1'''

    #更新成員列表直播與訂閱資訊
    def update_data(self):
        #讀取檔案獲得已訂閱成員
        subMemberFile = open('subscribe_member.txt', 'r')
        self.__subMemberArray = subMemberFile.read().split(';')
        #讀取API獲得直播中成員資料
        ScanLiveMember().getLiveMember()
        self.member_table_count = 0

        #更新成員列表資料
        for member in self.member_table.get_children():
            mId = memberIdJson[self.member_table.item(member, 'value')[1]]

            #更新訂閱與否
            if mId in self.__subMemberArray:
                self.member_table.set(member, 0, value=('已訂閱'))
            else:
                self.member_table.set(member, 0, value=(''))

            #更新是否直播中
            if mId in LiveMemberData:
                self.member_table.set(member, 2, value=('直播中'))
                self.member_table.set(member, 3, value=(LiveMemberData[mId].getHotVal()))
            else:
                self.member_table.set(member, 2, value=(''))
                self.member_table.set(member, 3, value=(''))

            #若直播中且已訂閱但未開始錄影則建立錄影執行緒
            if mId in LiveMemberData and mId in self.__subMemberArray and mId not in self.thr:
                self.member_table.set(member, 4, value=('錄製中'))
                self.thr[mId] = threading.Thread(target=test, args=[mId])
                self.thr[mId].start()

            #若未直播中但有錄影執行緒則刪除該執行緒
            if mId not in LiveMemberData and mId in self.thr:
                if not self.thr[mId].isAlive():
                    del self.thr[mId]
                    self.member_table.set(member, 4, value=(''))


        '''for i in range(0, len(self.member_table.get_children())):
            self.member_table.delete(self.member_table.get_children()[i])
            self.insert_data(memberIdArray[i][1], i)'''
        config = configparser.ConfigParser()
        config.read('setting.ini')
        threading.Timer(int(config['SET']['loop_second']), self.update_data).start()

#讀取成員資料並將姓名與浪Live編號相互指引
memberIdFile = open('member_id.txt','r')
memberIdArray = memberIdFile.read().split(';')
for i in range(0, len(memberIdArray) - 1):
    memberIdArray[i] = memberIdArray[i].split(',')
memberIdStr = '{'
for i in range(0, len(memberIdArray) - 1):
    print("姓名：" + memberIdArray[i][0] + ", ID：" + memberIdArray[i][1])
    memberIdStr += "\"" + memberIdArray[i][0] + "\":\"" + memberIdArray[i][1] + "\","
    memberIdStr += "\"" + memberIdArray[i][1] + "\":\"" + memberIdArray[i][0] + "\""
    if i is not (len(memberIdArray) - 2):
        memberIdStr += ","
    else:
        memberIdStr += "}"
memberIdJson = json.loads(memberIdStr)

#初始化直播中成員陣列
LiveMemberData = {}

#ffmpeg錄製影片
def test(id):
    #threading.Thread(sleep(3))
    '''while True:
        url = LiveMemberData[id].getLiveUrl()
        if requests.get(url) is 200:
            break
        url = LiveMemberData[id].getLiveUrlAno()
        if requests.get(url) is 200:
            break'''

    #直播連結會有兩種,所以需要分別判斷連結是否可以讀取
    if requests.get(LiveMemberData[id].getLiveUrl()).status_code == 200:
        url = LiveMemberData[id].getLiveUrl()
    else:
        url = LiveMemberData[id].getLiveUrlAno()

    #獲得目前時間並作為檔案名稱
    sTime = str(time.time())
    #下錄影指令
    command = subprocess.Popen("ffmpeg -i \"" + url + "\" -c copy -report " + memberIdJson[id] + "_" +
                                time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + sTime[sTime.find('.'):]  + ".ts",
                                shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)


    recvFlag = 1
    out = ''
    while True:
        try:
            if recvFlag is not 0:
                #最初先逐行讀取
                out = command.stderr.readline().decode('big5')
                #讀取到Press字串後開始錄影
                recvFlag = out.find('Press')
            else:
                index = 79
                #之後則逐字讀取
                out += command.stderr.read(1).decode('big5')
                '''if out.find('Lsize') is not -1:
                    out += command.stderr.read(2).decode('big5')
                    index += 1
                if out.find('/s') is not index:
                    print(out)
                    if out.find('video') is not -1:
                        while out.find('%') is -1:
                            out += command.stderr.read(1).decode('big5')
                            return
                    else:
                        while out.find('file.') is -1:
                            out += command.stderr.read(1).decode('big5')
                        out += command.stderr.read(2).decode('big5')'''
        except:
            print("Unexpected error:", sys.exc_info())
        if out is not '':
            if recvFlag is not 0:
                print(out, end='')
            else:
                if out.find('speed') is not -1:
                    #保留讀取錄製訊息,未來可新增至視窗上
                    print(out.rstrip())
                    out = ''
                elif out.find('Opening') is not -1:
                    #每當ffmpeg錄影一小短畫面便會傳回Opening字串
                    #因直播結束ffmpeg不會自行關閉,所以則每次檢查直播連結是否還在
                    #否則傳送指令結束ffmpeg並結束此執行緒
                    if requests.get(url).status_code != 200:
                        command.communicate(input=b'q\n')
                        break
                    else:
                        out = ''

#--------------------測試程式碼-----------------------------------------------------
def cmdTest(num):
    recvFlag = 1
    sTime = str(time.time())
    stri = "ffmpeg -i \"https://playback-ws.langlive.com/live-3650718Y997710SMP--20190425214255.m3u8\" -c copy -t 00:03:30 -report 林潔心_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + sTime[sTime.find('.'):] + ".ts"
    dir = subprocess.Popen(stri, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out = ''
    while True:
        try:
            if recvFlag is not 0:
                out = dir.stderr.readline().decode('big5')
                recvFlag = out.find('Press')
            else:
                index = 79
                out += dir.stderr.read(1).decode('big5')
                '''if out.find('Lsize') is not -1:
                    out += dir.stderr.read(2).decode('big5')
                    index += 1
                if out.find('/s') is not index:
                    print(out)
                    if out.find('video') is not -1:
                        while out.find('%') is -1:
                            out += dir.stderr.read(1).decode('big5')
                            return
                    else:
                        while out.find('file.') is -1:
                            out += dir.stderr.read(1).decode('big5')
                        out += dir.stderr.read(2).decode('big5')'''
        except:
            print("Unexpected error:", sys.exc_info())
        if out is not '':
            if recvFlag is not 0:
                print(out, end='')
            else:
                if out.find('speed') is not -1:
                    if num is 0:
                        dir.communicate(input=b'q\n')
                        break
                    print(out.rstrip())
                    out = ''

i = 0
t = threading.Thread(target=cmdTest, args=[i])
#t.start()
threading.Thread(sleep(1))
i = 1
t2 = threading.Thread(target=cmdTest, args=[i])
#t2.start()
#-------------------------------------------------------------------------

window = Tk()#建立視窗
w = LangLiveWindow(window)
w.init_data()#初始化列表
w.update_data()#撈API更新列表資料
window.mainloop()
