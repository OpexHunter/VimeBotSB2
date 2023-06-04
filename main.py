# https://www.autohotkey.com/ (v1.1 версия AHK)
import os
import sys
import ahk
import numpy as np
import time
import keyboard
from win10toast import ToastNotifier
import datetime
import PySimpleGUI as sg
import subprocess
import threading
if getattr(sys, "frozen", ""):
    # переназначаем путь к AutoHotkey.exe
    AHK = ahk.AHK(executable_path=os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.realpath(sys.executable))), "C:\Program Files\AutoHotkey\AutoHotkey.exe"))
else:
    AHK = ahk.AHK() # используем путь по умолчанию


def work(dur, shutdown, tpd):
    win = ''
    while win != ahk.AHK().find_window(title=b'VimeWorld'):
        win = ahk.AHK().get_active_window()
    time.sleep(0.2)
    keyboard.send('ESC')
    time.sleep(0.2)
    tdur = (dur - 30) * int(tpd)
    time1 = datetime.timedelta(seconds=int(np.around(sum(tdur))))
    print(time1)
    mess = 'Я буду копать ' + str(np.around(sum(tdur) / 60, 2)) + 'минут\nДо ' + (datetime.datetime.now() + time1).strftime("%H:%M:%S")
    toaster.show_toast("Лёша 2.0", mess, duration=10, threaded=True)

    for j in range(len(dur)):
        ahk.AHK().key_down('LButton')
        keyboard.send(str(j + 1))
        time.sleep(tdur[j])
        ahk.AHK().key_up('LButton')

    if shutdown:
        subprocess.call(['shutdown', '/s', '/t', '90'])

#
toaster = ToastNotifier()

#Граф интерфейс
layout = [
    [sg.Text('Прочности (через запятую)'), sg.InputText()
     ],
    [sg.Checkbox('Выключить по завершении')
     ],
    [sg.Text('Скорость ломания прочности в секунду. \nДля каждого уровня острова, зачарований - разные коэффиценты.\nВсе кирки должны быть однотипными'
             '\nВвод в формате (секунд ломания)/(потерянная прочность)\n-------------\n6ур п3 эфф4 = 2218 / 1391', background_color='White', text_color= 'Black'),
     ],
    [sg.InputText()
    ],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Лёша 2.0 - Лучше, чем вчера!', layout)
while True:                             # The Event Loop
    event, values = window.read()
    #print(event, values) #debug
    if event in (None, 'Exit'):
        break
    elif values[0] == '':
        toaster.show_toast("Ты даун ?", '-ДА', duration=2, threaded=True)
        break
    elif event == 'Submit':
        print(values)
        dp = np.array([int(i) for i in values[2].replace(' ', '').split('/')])
        print(dp)
        tdp = dp[0]/dp[1]
        dur = np.array([int(i) for i in values[0].replace(' ', '').split(',')])
        print(tdp, dur)
        threading.Thread(target=work, args=(dur, values[1], tdp), daemon=True).start()
