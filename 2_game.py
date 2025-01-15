from tkinter import messagebox
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import random


def Report(roi_total, roi_round):
    xar = np.arange(1, len(roi_total)+1)
    r1 = np.array(roi_total)
    r2 = np.array(roi_round)
    plt.plot(xar, r1, 'b', label='Total', linestyle="-",
             linewidth="2", markersize="16", marker=".")
    plt.plot(xar, r2, 'r', label='Round', linestyle="-",
             linewidth="2", markersize="16", marker=".")
    plt.xlabel('Round')
    plt.ylabel('ROI(%)')
    plt.xticks(xar, rotation='vertical')
    plt.legend(loc='upper left')
    plt.show()


def ExistGame(roi_total, roi_round):
    win.destroy()
    Report(roi_total, roi_round)
    print('Quit game')


def Replay(bankerbase, playerbase, bet, poker, totals, fm_card, fm_result, fm_str, label_player, prebase, roi_total, roi_round, fm_raise):
    fm_str.pack_forget()
    fm_card.pack_forget()
    fm_raise.pack_forget()
    fm_result.pack_forget()

    if playerbase <= 40:
        label_player.config(bg='pink', fg='red')

    if playerbase <= 0:
        messagebox.showwarning(title='遊戲結束', message='你沒錢了')
        win.destroy()
        Report(roi_total, roi_round)

    print('Play again')
    print()
    ShowTitle(bankerbase, playerbase, poker,
              totals, prebase, roi_total, roi_round)


def Playgame(bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, fm_card, fm_raise, label_player, card3, num1, num2, flag, bet, btn_raise):
    print('Play')
    btn_raise['state'] = tk.DISABLED

    num3 = int(card_number[card3[1:]])
    if num1 == num2:
        if num3 == num1:
            bankerbase -= bet
            playerbase += bet
            result_poker = '撞撞撞,賠三倍'
        elif (flag == 1 and num3 < num1) or (flag == 0 and num3 > num1):
            bankerbase += bet
            playerbase -= bet
            result_poker = '猜錯了'
        else:
            bankerbase -= bet
            playerbase += bet
            result_poker = '猜對了'
    elif num3 == num1 or num3 == num2:
        bankerbase += 2*bet
        playerbase -= 2*bet
        result_poker = '撞柱!'
    elif min(num1, num2) < num3 < max(num1, num2):
        bankerbase -= bet
        playerbase += bet
        result_poker = '在範圍內,贏錢!'
    else:
        bankerbase += bet
        playerbase -= bet
        result_poker = '超出範圍,給錢!'
    print('Result:', result_poker)

    totals += +1
    roi = round(((playerbase-100)/100)*100, 1)
    round_roi = round(((playerbase-prebase)/prebase)*100, 1)
    prebase = playerbase
    roi_total.append(roi)
    roi_round.append(round_roi)
    print('ROI(total):', roi_total)
    print('ROI(round):', roi_round)
    print('Round', totals, 'over')

    fm_result = tk.Frame(win, bg='lightblue', width=400, height=280)
    label_card3 = tk.Label(fm_result, text=card3,
                           bg='white', fg='red', font=('Elephant', 20))
    label_ans = tk.Label(fm_result, text=result_poker,
                         font=('Segoe Print', 12))
    btn_again = tk.Button(fm_result, text='Coutinue', font=('Segoe Print', 12), borderwidth=3, command=lambda: Replay(
        bankerbase, playerbase, bet, poker, totals, fm_card, fm_result, fm_str, label_player, prebase, roi_total, roi_round, fm_raise))
    btn_exist = tk.Button(fm_result, text='Exist', font=(
        'Segoe Print', 12), borderwidth=3, command=lambda: ExistGame(roi_total, roi_round))

    fm_result.pack()
    label_card3.place(x=125, y=5, width=150, height=200)
    label_ans.place(x=100, y=215, width=200, height=20)
    btn_again.place(x=120, y=245, width=85, height=25)
    btn_exist.place(x=220, y=245, width=55, height=25)


def Quitgame(bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, fm_card):
    print('Quit')
    fm_card.pack_forget()
    fm_str.pack_forget()

    totals += 1
    if totals-2 < 0:
        roi_total.append(0)
    else:
        roi_total.append(roi_total[totals-2])
    roi_round.append(0)
    print('ROI(total):', roi_total)
    print('ROI(round):', roi_round)
    print('Round', totals, 'over')
    print()

    ShowTitle(bankerbase, playerbase, poker,
              totals, prebase, roi_total, roi_round)


def RaiseBet(bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, fm_card, label_player, card3, num1, num2, flag, btn_quit, btn1, btn2):
    btn1['state'] = tk.DISABLED
    btn2['state'] = tk.DISABLED
    btn_quit['state'] = tk.DISABLED

    def defbet():
        if int(input_raise.get()) > playerbase:
            messagebox.showerror(title='金額有誤', message='下注金額不可高於玩家金額')
        else:
            bet = int(input_raise.get())
            print('Bet:', bet)
            Playgame(bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round,
                     fm_str, fm_card, fm_raise, label_player, card3, num1, num2, flag, bet, btn_raise)

    fm_raise = tk.Frame(win, bg='lightyellow', width=400, height=35)
    label_bet = tk.Label(fm_raise, bg='white', font=(
        'Kristen ITC', 11), text='下注金額:')
    input_raise = tk.Entry(fm_raise, width=15)
    btn_raise = tk.Button(fm_raise, text='下注', bg='lightgray', font=(
        'Segoe Print', 12), borderwidth=3, command=lambda: defbet())

    fm_raise.pack()
    label_bet.place(x=120, y=5, width=70, height=25)
    input_raise.place(x=195, y=5, width=30, height=25)
    btn_raise.place(x=230, y=5, width=40, height=25)


def PlayOrQuit(bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, label_player, card1, card2, card3):
    fm_card = tk.Frame(win, bg='lightblue', width=400, height=250)
    label_card1 = tk.Label(fm_card, bg='white', fg='red',
                           font=('Elephant', 20), text=card1)
    label_card2 = tk.Label(fm_card, bg='white', fg='red',
                           font=('Elephant', 20), text=card2)
    btn_quit = tk.Button(fm_card, text='Quit', font=('Segoe Print', 12), borderwidth=3, command=lambda: Quitgame(
        bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, fm_card))

    fm_card.pack()
    label_card1.place(x=35, y=10, width=150, height=200)
    label_card2.place(x=215, y=10, width=150, height=200)
    btn_quit.place(x=210, y=220, width=50, height=25)

    num1 = int(card_number[card1[1:]])
    num2 = int(card_number[card2[1:]])

    if num1 == num2:
        up = tk.Button(fm_card, text='Big', font=('Segoe Print', 12), borderwidth=3, command=lambda: RaiseBet(
            bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, fm_card, label_player, card3, num1, num2, 1, btn_quit, up, down))
        down = tk.Button(fm_card, text='Small', font=('Segoe Print', 12), borderwidth=3, command=lambda: RaiseBet(
            bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, fm_card, label_player, card3, num1, num2, 0, btn_quit, up, down))
        up.place(x=70, y=220, width=50, height=25)
        down.place(x=140, y=220, width=50, height=25)
    else:
        play = tk.Button(fm_card, text='Play', font=('Segoe Print', 12), borderwidth=3, command=lambda: RaiseBet(
            bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, fm_card, label_player, card3, num1, num2, 0, btn_quit, play, play))
        play.place(x=140, y=220, width=50, height=25)


def Startgame(bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, label_player, btn_start):
    btn_start['state'] = tk.DISABLED
    print("Draw 3 cards")
    random.shuffle(poker)
    card1, card2, card3 = random.sample(poker, 3)
    print(card1, card2, card3)
    PlayOrQuit(bankerbase, playerbase, poker, totals, prebase,
               roi_total, roi_round, fm_str, label_player, card1, card2, card3)


def ShowTitle(bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round):
    print('Game start')
    str1 = "莊家金額:" + str(bankerbase)
    str2 = "玩家餘額:" + str(playerbase)

    fm_str = tk.Frame(win, bg='pink', width=500, height=70)
    label_banker = tk.Label(
        fm_str, bg='white', font=('Kristen ITC', 11), text=str1)
    label_player = tk.Label(
        fm_str, bg='white', font=('Kristen ITC', 11), text=str2)
    btn_start = tk.Button(fm_str, text='Start', font=('Segoe Print', 12), borderwidth=3, command=lambda: Startgame(
        bankerbase, playerbase, poker, totals, prebase, roi_total, roi_round, fm_str, label_player, btn_start))

    fm_str.pack(padx=100, pady=5)
    label_banker.place(x=90, y=10, width=100, height=25)
    label_player.place(x=210, y=10, width=100, height=25)
    btn_start.place(x=175, y=45, width=55, height=25)

    if playerbase <= 40:
        label_player.config(bg='pink', fg='red')


# 初始設定
bankerbase = 100    # 莊家餘額
playerbase = 100    # 玩家餘額
totals = 0          # 累積局數
prebase = 100       # 前次餘額
roi_total = []      # 總投資報酬率
roi_round = []      # 單局投資報酬率


# 外框架
win = tk.Tk()
win.title('POKER')
win.geometry('600x650')
win.config(bg='green')

parent_menu = tk.Menu(win)
win.config(menu=parent_menu)
file_menu = tk.Menu(parent_menu, tearoff=0,
                    activebackground='lightgray', activeforeground='black')
parent_menu.add_cascade(label='遊戲', menu=file_menu)
file_menu.add_command(
    label='投資報酬率', command=lambda: Report(roi_total, roi_round))
file_menu.add_separator()
file_menu.add_command(label='離開', command=lambda: win.destroy())


# 洗牌
card_color = ['♠', '♥', '♦', '♣']
card_number = {'K': '13', 'Q': '12', 'J': '11', '10': '10', '9': '9', '8': '8',
               '7': '7', '6': '6', '5': '5', '4': '4', '3': '3', '2': '2', 'A': '1'}
poker = []
for x in card_color:
    for y in card_number.keys():
        card = x+y
        poker.append(card)
random.shuffle(poker)
ShowTitle(bankerbase, playerbase, poker,
          totals, prebase, roi_total, roi_round)


win.mainloop()
