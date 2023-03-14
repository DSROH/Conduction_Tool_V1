# %%
import tkinter as tk
import ttkbootstrap as ttkbst
import tkinter.font as font
from ttkbootstrap.constants import *
import tkinter.scrolledtext as st
import tkinter.messagebox as msgbox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import matplotlib.pyplot as plt

plt.rc("xtick", labelsize=8)
plt.rc("ytick", labelsize=8)
# plt.rcParams.update({'font.size': 8})

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import threading

import Function as func
import Band_list as blist

# %%
CB_list, PS_list1, PS_list2, CP_list = func.Equipment_scan()

Win_GUI = ttkbst.Window(title="LSI Conduction Test V1.0")
Win_GUI.attributes("-topmost", True)
Win_GUI.geometry("1620x865")


def change_theme():
    themename = Win_GUI.getvar("themename")
    Win_GUI.style.theme_use(themename)


themes = Win_GUI.style.theme_names()

# %%
Left_frame = ttkbst.Frame(Win_GUI)
Left_frame.place(x=0, y=0, width=765, height=865)

# %%
canvas_frame = ttkbst.Labelframe(Left_frame, text="Canvas")  # Frame의 크기 따로 지정하지 않고, figsize로 결정됨
canvas_frame.place(x=5, y=410, width=755, height=405)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(7.50, 3.85), dpi=100)
fig.set_facecolor("white")

canvas = FigureCanvasTkAgg(fig, canvas_frame)

ax1 = plt.subplot(2, 2, (1, 3))
ax1.axis(xmin=0, xmax=25)
ax1.axis(ymin=0, ymax=650)
ax1.set_xlabel("Measured Power (dBm)", fontsize=8)
ax1.set_ylabel("PA Current (mA)", fontsize=8)
ax1.grid(True, color="black", alpha=0.3, linestyle="--")

ax2 = plt.subplot(2, 2, 2)
ax2.axis(xmin=0, xmax=25)
ax2.axis(ymin=-2, ymax=2)
ax2.set_xlabel("Measured Power (dBm)", fontsize=8)
# ax2.set_ylabel("Power Diff (dB)", fontsize=8)
ax2.grid(True, color="black", alpha=0.3, linestyle="--")

ax3 = plt.subplot(2, 2, 4)
ax3.axis(xmin=0, xmax=25)
ax3.set_xlabel("Measured Power (dBm)", fontsize=8)
# ax3.set_ylabel("ACLR (dBc)", fontsize=8)
ax3.grid(True, color="black", alpha=0.3, linestyle="--")

canvas.draw
canvas.get_tk_widget().grid(row=0, column=0, sticky=NSEW)
plt.tight_layout()

plt.close()

# %%
Scrolled_txt_frame = ttkbst.Frame(Win_GUI)
Scrolled_txt_frame.place(x=765, y=0, width=855, height=820)

text_area = st.ScrolledText(Scrolled_txt_frame, font=("Consolas", 9))
text_area.place(x=0, y=5, width=855, height=810)

Auth_frame = ttkbst.Frame(Win_GUI)
Auth_frame.place(x=765, y=820, width=855, height=45)

Author = ttkbst.Label(Auth_frame, text="dongsub.roh@samsung.com")
Author.place(x=685, y=10)

# %%
Setting_frame = ttkbst.Frame(Left_frame)
Setting_frame.place(x=5, y=120, width=755, height=290)

TX_Main_frame = ttkbst.Labelframe(Setting_frame, text="TX Main")
TX_Main_frame.place(x=0, y=50, width=400, height=120)


def Select_Main(v, ch_option, User_defined_path, User_defined_band):
    global Band_Select_Main_var, Band_index_Main
    Band_index_Main = []

    for widget in TX_Main_frame.winfo_children():
        widget.destroy()

    if v == 1:  # 3G
        B_list_Main = [1, 2, 4, 5, 8]
        rat = "B"
    elif v == 2:
        B_list_Main = [1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 66, 38, 39, 40, 41]
        rat = "B"
    elif v == 3:
        B_list_Main = [1, 2, 3, 5, 7, 8, 12, 13, 20, 25, 26, 28, 66, 38, 39, 40, 41, 77, 78]
        rat = "n"

    try:
        if Band_Select_Main_var:
            for count, i in enumerate(Band_Select_Main_var):
                Band_Select_Main_var[count].place_forget()
    except:
        Band_Select_Main_var = [None] * len(B_list_Main)
        Chkbox_Main = [None] * len(B_list_Main)

    for count, i in enumerate(B_list_Main):
        Band_Select_Main_var[count] = ttkbst.BooleanVar()
        Chkbox_Main[count] = ttkbst.Checkbutton(
            TX_Main_frame,
            text=f"{rat}{i}",
            width=5,
            variable=Band_Select_Main_var[count],
        )
        Band_index_Main.append(f"{rat}{i}")
        if count == 0:
            pos_x = 10
            pos_y = 5
        else:
            pos_x = 10 + 55 * (count % 7)
            pos_y = 5 + 35 * (count // 7)

        if (ch_option == 3) & (User_defined_path == "Main"):
            rat = User_defined_band[:1]
            User_Blist_Main = int(User_defined_band[1:])
            if i == User_Blist_Main:
                Band_Select_Main_var[count].set(True)
            else:
                Band_Select_Main_var[count].set(False)
        elif (ch_option == 3) & (User_defined_path == "Sub"):
            Band_Select_Main_var[count].set(False)
        else:
            if (v == 3) & (i in [39]):
                Chkbox_Main[count].config(state=tk.DISABLED)
                Band_Select_Main_var[count].set(False)
            else:
                Band_Select_Main_var[count].set(True)

        Chkbox_Main[count].place(x=pos_x, y=pos_y, width=50)


# %%
TX_Sub_frame = ttkbst.Labelframe(Setting_frame, text="TX Sub")
TX_Sub_frame.place(x=0, y=170, width=400, height=120)


def Select_Sub(v, ch_option, User_defined_path, User_defined_band):
    global Band_Select_Sub_var, Band_index_Sub
    Band_index_Sub = []

    for widget in TX_Sub_frame.winfo_children():
        widget.destroy()

    if v == 1:  # 3G
        B_list_Sub = [1, 2, 4]
        rat = "B"
    elif v == 2:
        B_list_Sub = [1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 66, 38, 39, 40, 41]
        rat = "B"
    elif v == 3:
        B_list_Sub = [1, 2, 3, 5, 7, 8, 12, 13, 20, 25, 26, 28, 66, 38, 39, 40, 41, 77, 78]
        rat = "n"

    try:
        if Band_Select_Sub_var:
            for count, i in enumerate(Band_Select_Sub_var):
                Band_Select_Sub_var[count].place_forget()
    except:
        Band_Select_Sub_var = [None] * len(B_list_Sub)
        Chkbox_Sub = [None] * len(B_list_Sub)

    for count, i in enumerate(B_list_Sub):
        Band_Select_Sub_var[count] = ttkbst.BooleanVar()
        Chkbox_Sub[count] = ttkbst.Checkbutton(
            TX_Sub_frame, text=f"{rat}{i}", width=5, variable=Band_Select_Sub_var[count]
        )
        Band_index_Sub.append(f"{rat}{i}")
        if count == 0:
            pos_x = 10
            pos_y = 5
        else:
            pos_x = 10 + 55 * (count % 7)
            pos_y = 5 + 35 * (count // 7)

        if (ch_option == 3) & (User_defined_path == "Sub"):
            rat = User_defined_band[:1]
            User_Blist_Sub = int(User_defined_band[1:])
            if i == User_Blist_Sub:
                Band_Select_Sub_var[count].set(True)
            else:
                Band_Select_Sub_var[count].set(False)
        elif (ch_option == 3) & (User_defined_path == "Main"):
            Band_Select_Sub_var[count].set(False)
        else:
            if (v == 2) & (i in [5, 8, 12, 13, 17, 18, 19, 20, 26]):
                Chkbox_Sub[count].config(state=tk.DISABLED)
                Band_Select_Sub_var[count].set(False)
            elif (v == 3) & (i in [5, 8, 12, 13, 20, 26, 39, 77, 78]):
                Chkbox_Sub[count].config(state=tk.DISABLED)
                Band_Select_Sub_var[count].set(False)
            else:
                Band_Select_Sub_var[count].set(True)

        Chkbox_Sub[count].place(x=pos_x, y=pos_y, width=50)


# %%
# 실행 프레임
Bottom_frame = ttkbst.Frame(Left_frame)
Bottom_frame.place(x=5, y=820, width=755, height=40)

# Themecombo = ttkbst.Combobox(Bottom_frame, values=themes, textvariable=theme, font=("Consolas", 8))
# Themecombo.place(x=5, y=8, width=100, height=30)

theme_options = tk.Menubutton(Bottom_frame, text="Select a theme")
menu = tk.Menu(theme_options)

for t in themes:
    menu.add_radiobutton(label=t, variable="themename", command=change_theme)

theme_options["menu"] = menu
theme_options.place(x=0, y=5, width=100, height=30)

# %%
User_defined_path = []
User_defined_band = []
User_defined_ch = []


def func_userch(Band_index_Main, Band_Select_Main_var, Band_index_Sub, Band_Select_Sub_var):
    global ChildWin_userdefine, Combo_user_define_path, User_defined_path

    try:
        ChildWin_userdefine.destroy()
    except:
        pass

    ChildWin_userdefine = ttkbst.Toplevel(title="User Defined Channel")
    ChildWin_userdefine.attributes("-topmost", True)
    ChildWin_userdefine.geometry("430x50")
    ChildWin_userdefine.resizable(False, False)

    TX_Path = ["Main", "Sub"]
    Combo_user_define_path = ttkbst.Combobox(ChildWin_userdefine, values=TX_Path, font=("Calibri", 10))
    Combo_user_define_path.place(x=10, y=10, width=60, height=30)
    Combo_user_define_path.current(0)
    Combo_user_define_path.bind("<<ComboboxSelected>>", lambda event: [User_select_band()])

    Combo_user_define_band = ttkbst.Combobox(ChildWin_userdefine, font=("Calibri", 10))
    Combo_user_define_band.place(x=80, y=10, width=60, height=30)
    Entry_user_define_ch = ttkbst.Entry(ChildWin_userdefine, justify=tk.LEFT, font=("Consolas", 10))
    Entry_user_define_ch.place(x=150, y=10, width=200, height=30)
    OK_btn = ttkbst.Button(ChildWin_userdefine, text="OK")
    OK_btn.place(x=360, y=10, width=60, height=30)
    ChildWin_userdefine.bind("<Return>", lambda event: [func_userch_ok()])
    ChildWin_userdefine.focus()


def User_select_band():
    global ChildWin_userdefine, Combo_user_define_band
    if Combo_user_define_path.get() == "Main":
        User_band = [x for c, x in enumerate(Band_index_Main) if Band_Select_Main_var[c].get() == True]
    else:
        User_band = [x for c, x in enumerate(Band_index_Sub) if Band_Select_Sub_var[c].get() == True]
    Combo_user_define_band = ttkbst.Combobox(ChildWin_userdefine, values=User_band, font=("Calibri", 10))
    Combo_user_define_band.place(x=80, y=10, width=60, height=30)
    Combo_user_define_band.current(0)
    Combo_user_define_band.bind("<<ComboboxSelected>>", lambda event: [User_input_ch()])


def User_input_ch():
    global ChildWin_userdefine, Entry_user_define_ch

    Entry_user_define_ch = ttkbst.Entry(ChildWin_userdefine, justify=tk.LEFT, font=("Consolas", 10))
    Entry_user_define_ch.place(x=150, y=10, width=200, height=30)

    OK_btn = ttkbst.Button(ChildWin_userdefine, text="OK", command=lambda: [func_userch_ok()])
    OK_btn.place(x=360, y=10, width=60, height=30)


def func_userch_ok():
    global ChildWin_userdefine, Ch_option_var
    global Combo_user_define_path, Combo_user_define_band, Entry_user_define_ch
    global User_defined_path, User_defined_band, User_defined_ch

    Ch_option_var.set(3)
    User_defined_path = Combo_user_define_path.get()
    User_defined_band = Combo_user_define_band.get()
    User_defined_ch = Entry_user_define_ch.get()
    ChildWin_userdefine.destroy()

    Select_Main(Rat_option_var.get(), 3, User_defined_path, User_defined_band)
    Select_Sub(Rat_option_var.get(), 3, User_defined_path, User_defined_band)


Run_mode_var = tk.IntVar()

Sig_Test = ttkbst.Radiobutton(
    Bottom_frame,
    text="<F1> Signaling",
    value=1,
    variable=Run_mode_var,
    command=lambda: [
        Run_mode_var.set(1),  # Signaling
        Rat_option_var.set(2),  # LTE Selected
        Rat_Option1.config(state=tk.NORMAL),  # 3G enable
        Rat_Option2.config(state=tk.NORMAL),  # LTE enable
        Rat_Option3.config(state=tk.DISABLED),  # NR Disable
    ],
)
Sig_Test.place(x=400, y=12)

Nonsig_Test = ttkbst.Radiobutton(
    Bottom_frame,
    text="<F2> Non-Signal",
    value=2,
    variable=Run_mode_var,
    command=lambda: [
        Run_mode_var.set(2),  # Non-signaling
        Rat_option_var.set(2),  # LTE Selected
        Rat_Option1.config(state=tk.NORMAL),  # 3G enable
        Rat_Option2.config(state=tk.NORMAL),  # LTE enable
        Rat_Option3.config(state=tk.NORMAL),  # NR enable
    ],
)
Nonsig_Test.place(x=515, y=12)

APT_Tune = ttkbst.Radiobutton(
    Bottom_frame,
    text="<F3> APT Tuning",
    value=3,
    variable=Run_mode_var,
    command=lambda: [
        Run_mode_var.set(3),
        Rat_option_var.set(3),
        Rat_Option1.config(state=tk.DISABLED),  # 3G disable
        Rat_Option2.config(state=tk.DISABLED),  # LTE disable
        Rat_Option3.config(state=tk.NORMAL),  # NR enable
    ],
)
APT_Tune.place(x=640, y=12)

Rat_frame = ttkbst.Labelframe(Setting_frame, text="RAT")
Rat_frame.place(x=0, y=0, width=150, height=50)

Rat_option_var = ttkbst.IntVar()
Rat_Option1 = ttkbst.Radiobutton(
    Rat_frame,
    text="3G",
    width=4,
    value=1,
    variable=Rat_option_var,
    command=lambda: [
        APT_Tune.config(state=tk.DISABLED),  # APT Tune enable
        Select_Main(Rat_option_var.get(), Ch_option_var.get(), User_defined_path, User_defined_band),
        Select_Sub(Rat_option_var.get(), Ch_option_var.get(), User_defined_path, User_defined_band),
    ],
)
Rat_Option1.place(x=10, y=6, width=40)

Rat_Option2 = ttkbst.Radiobutton(
    Rat_frame,
    text="LTE",
    width=4,
    value=2,
    variable=Rat_option_var,
    command=lambda: [
        APT_Tune.config(state=tk.DISABLED),  # APT Tune enable
        Select_Main(Rat_option_var.get(), Ch_option_var.get(), User_defined_path, User_defined_band),
        Select_Sub(Rat_option_var.get(), Ch_option_var.get(), User_defined_path, User_defined_band),
    ],
)
Rat_Option2.place(x=55, y=6, width=40)

Rat_Option3 = ttkbst.Radiobutton(
    Rat_frame,
    text="NR ",
    width=4,
    value=3,
    variable=Rat_option_var,
    command=lambda: [
        APT_Tune.config(state=tk.NORMAL),  # APT Tune enable
        Select_Main(Rat_option_var.get(), Ch_option_var.get(), User_defined_path, User_defined_band),
        Select_Sub(Rat_option_var.get(), Ch_option_var.get(), User_defined_path, User_defined_band),
    ],
)
Rat_Option3.place(x=100, y=6, width=40)

# %%
Ch_frame = ttkbst.Labelframe(Setting_frame, text="Channel")
Ch_frame.place(x=155, y=0, width=205, height=50)

Ch_option_var = ttkbst.IntVar()
Ch_Option1 = ttkbst.Radiobutton(Ch_frame, text="1CH ", value=1, variable=Ch_option_var)
Ch_Option1.place(x=10, y=6, width=45)

Ch_Option2 = ttkbst.Radiobutton(Ch_frame, text="3CH ", value=2, variable=Ch_option_var)
Ch_Option2.place(x=60, y=6, width=45)

Ch_Option3 = ttkbst.Radiobutton(Ch_frame, text="User Define", value=3, variable=Ch_option_var)
Ch_Option3.place(x=110, y=6, width=85)
Ch_Option3.config(state=tk.DISABLED)


Btn_user_defined_ch = ttkbst.Button(
    Setting_frame,
    text="User Defined CH (F8)",
    style="danger.TButton",
    command=lambda: [
        Select_Main(Rat_option_var.get(), 1, User_defined_path, User_defined_band),
        Select_Sub(Rat_option_var.get(), 1, User_defined_path, User_defined_band),
        func_userch(Band_index_Main, Band_Select_Main_var, Band_index_Sub, Band_Select_Sub_var),
    ],
)
Btn_user_defined_ch.place(x=365, y=11, width=142, height=35)
Win_GUI.bind(
    "<F8>",
    lambda event: [
        Select_Main(Rat_option_var.get(), 1, User_defined_path, User_defined_band),
        Select_Sub(Rat_option_var.get(), 1, User_defined_path, User_defined_band),
        func_userch(Band_index_Main, Band_Select_Main_var, Band_index_Sub, Band_Select_Sub_var),
    ],
)

# %%
Pw_option_var = ttkbst.IntVar()
Btn_pwsetting = ttkbst.Button(
    Setting_frame,
    text="Power Level (F10)",
    style="danger.TButton",
    command=lambda: [blist.Power_setting(Pw_option_var)],
)
Btn_pwsetting.place(x=634, y=11, width=122, height=35)

Win_GUI.bind("<F10>", lambda event: [blist.Power_setting(Pw_option_var)])

# %%
s = ttkbst.Style()
# s.configure("SelectBand.TButton", font=("Calibri", 10))

# Select all 버튼
Select_Main_frame = ttkbst.Labelframe(Setting_frame, text="Main")
Select_Main_frame.place(x=405, y=50, width=60, height=120)

Select_Mainall = ttkbst.Button(
    Select_Main_frame,
    text="All",
    # style="SelectBand.TButton",
    command=lambda: [blist.Selectall_band(Rat_option_var, "Main", Band_Select_Main_var)],
)
Select_Mainall.place(x=4, y=0, width=50, height=29)

Select_Mainfdd = ttkbst.Button(
    Select_Main_frame,
    text="FDD",
    # style="SelectBand.TButton",
    command=lambda: [blist.Selectfdd_band(Rat_option_var, "Main", Band_Select_Main_var)],
)
Select_Mainfdd.place(x=4, y=34, width=50, height=29)

Select_Maintdd = ttkbst.Button(
    Select_Main_frame,
    text="TDD",
    # style="SelectBand.TButton",
    command=lambda: [blist.Selecttdd_band(Rat_option_var, "Main", Band_Select_Main_var)],
)
Select_Maintdd.place(x=4, y=68, width=50, height=29)

# %%
# Select all 버튼
Select_Sub_frame = ttkbst.Labelframe(Setting_frame, text="Sub")
Select_Sub_frame.place(x=405, y=170, width=60, height=120)

Select_Suball = ttkbst.Button(
    Select_Sub_frame,
    text="All",
    # style="SelectBand.TButton",
    command=lambda: [blist.Selectall_band(Rat_option_var, "Sub", Band_Select_Sub_var)],
)
Select_Suball.place(x=4, y=0, width=50, height=29)

Select_Subfdd = ttkbst.Button(
    Select_Sub_frame,
    text="FDD",
    # style="SelectBand.TButton",
    command=lambda: [blist.Selectfdd_band(Rat_option_var, "Sub", Band_Select_Sub_var)],
)
Select_Subfdd.place(x=4, y=34, width=50, height=29)

Select_Subtdd = ttkbst.Button(
    Select_Sub_frame,
    text="TDD",
    # style="SelectBand.TButton",
    command=lambda: [blist.Selecttdd_band(Rat_option_var, "Sub", Band_Select_Sub_var)],
)
Select_Subtdd.place(x=4, y=68, width=50, height=29)

# %%
def Callback_CB(combo1, Rat_option_var):
    Call_Box = combo1.get()

    if Call_Box == "GPIB0::20::INSTR":
        Run_mode_var.set(2)  # Non-signaling
        Rat_Option2.invoke()
        # Rat_option_var.set(2)  # LTE Selected
        Rat_Option1.config(state=tk.NORMAL)  # 3G enable
        Rat_Option2.config(state=tk.NORMAL)  # LTE enable
        Rat_Option3.config(state=tk.DISABLED)  # NR Disable
        Sig_Test.config(state=tk.NORMAL)  # Signaling enable
        Nonsig_Test.config(state=tk.NORMAL)  # NonSignaling enable
        APT_Tune.config(state=tk.DISABLED)  # APT Tune Disable
        Win_GUI.bind(
            "<F1>",
            lambda event: [
                Run_mode_var.set(1),  # Signaling
                Rat_Option2.invoke(),
                # Rat_option_var.set(2),  # LTE Selected
                Rat_Option1.config(state=tk.NORMAL),  # 3G enable
                Rat_Option2.config(state=tk.NORMAL),  # LTE enable
                Rat_Option3.config(state=tk.DISABLED),  # NR Disable
            ],
        )
        Win_GUI.unbind("<F3>")

    elif Call_Box == "TCPIP0::127.0.0.1":
        Run_mode_var.set(2)  # Non-signaling
        Rat_Option2.invoke()
        # Rat_option_var.set(2)  # LTE Selected
        Rat_Option1.config(state=tk.NORMAL)  # 3G enable
        Rat_Option2.config(state=tk.NORMAL)  # LTE enable
        Rat_Option3.config(state=tk.NORMAL)  # NR enable
        Sig_Test.config(state=tk.DISABLED)  # Signaling Disable
        Nonsig_Test.config(state=tk.NORMAL)  # NonSignaling Disable
        APT_Tune.config(state=tk.NORMAL)  # APT Tune enable
        Win_GUI.unbind("<F1>")
        Win_GUI.bind(
            "<F3>",
            lambda event: [
                Run_mode_var.set(3),
                Rat_Option3.invoke(),
                # Rat_option_var.set(3),  # NR Main Selected
                Rat_Option1.config(state=tk.DISABLED),  # 3G disable
                Rat_Option2.config(state=tk.DISABLED),  # LTE disable
                Rat_Option3.config(state=tk.NORMAL),  # NR enable
            ],
        )
    else:
        msgbox.showwarning("Warning", "Select Call_Box")


# %%
toolbar_frame = ttkbst.Frame(Left_frame)
toolbar_frame.place(x=5, y=80, width=755, height=40)

Label1 = ttkbst.Label(toolbar_frame, text="Call Box")
Label1.place(x=0, y=10, width=50)
combo1 = ttkbst.Combobox(toolbar_frame, values=CB_list, font=("Calibri", 10))
combo1.place(x=55, y=5, width=105)
combo1.bind("<<ComboboxSelected>>", lambda event: [Callback_CB(combo1, Rat_option_var)])

Label2 = ttkbst.Label(toolbar_frame, text="System Power")
Label2.place(x=170, y=10, width=80)
combo2 = ttkbst.Combobox(toolbar_frame, values=PS_list1, font=("Calibri", 10))
combo2.place(x=255, y=5, width=100)
combo2.bind("<<ComboboxSelected>>", lambda event: [func.Callback_Sys_P(combo2)])

Label3 = ttkbst.Label(toolbar_frame, text="PA VCC")
Label3.place(x=365, y=10, width=50)
combo3 = ttkbst.Combobox(toolbar_frame, values=PS_list2, font=("Calibri", 10))
combo3.place(x=420, y=5, width=100)
combo3.bind("<<ComboboxSelected>>", lambda event: [func.Callback_PA_Vcc(combo3)])

Label4 = ttkbst.Label(toolbar_frame, text="COM Port")
Label4.place(x=530, y=10, width=60)
combo4 = ttkbst.Combobox(toolbar_frame, values=CP_list, font=("Calibri", 10))
combo4.place(x=595, y=5, width=60)
combo4.bind("<<ComboboxSelected>>", lambda event: [func.Callback_Comport(combo4)])

Equip_scan_btn = ttkbst.Button(toolbar_frame, text="Equip. Scan", command=lambda: [func.Equipment_scan()])
Equip_scan_btn.place(x=665, y=5, width=90)

# %%
MIPI_frame = ttkbst.Labelframe(Setting_frame, text="MIPI")
MIPI_frame.place(x=470, y=50, width=285, height=240)

Mipi_data = {
    "LB_PA": [2, 13, 2, 0],
    "LB_SM": [2, 5, 2, 0],
    "OMH_PA": [0, 14, 2, 0],
    "OMH_SM": [0, 5, 2, 0],
    "NR_PA": [4, 15, 2, 0],
    "NR_SM": [4, 5, 2, 0],
}
Mipi_Label = [None] * len(Mipi_data)

Mipi_posx = [60, 95, 130, 165, 200, 235]
Mipi_posy = {
    "LB_PA": [32, 32, 32, 32],
    "LB_SM": [62, 62, 62, 62],
    "OMH_PA": [92, 92, 92, 92],
    "OMH_SM": [122, 122, 122, 122],
    "NR_PA": [152, 152, 152, 152],
    "NR_SM": [182, 182, 182, 182],
}

for count, i in enumerate(Mipi_data):
    Mipi_Label[count] = ttkbst.Label(MIPI_frame, text=f"{i}", font=("Consolas", 8), anchor="e")
    for c, j in enumerate(Mipi_data[i]):
        Mipi_data[i][c] = ttkbst.Entry(MIPI_frame, justify=RIGHT, font=("Consolas", 8))
        Mipi_data[i][c].insert(0, j)
        Mipi_data[i][c].place(x=Mipi_posx[c], y=Mipi_posy[i][c], width=30, height=26)
        Mipi_Label[count].place(x=0, y=Mipi_posy[i][c], width=50, height=26)

# %%
Mipi_label_ch = ttkbst.Label(MIPI_frame, text="Ch", font=("Consolas", 8), anchor="center")
Mipi_label_ch.place(x=60, y=5, width=30, height=26)
Mipi_label_usid = ttkbst.Label(MIPI_frame, text="USID", font=("Consolas", 8), anchor="center")
Mipi_label_usid.place(x=95, y=5, width=30, height=26)
Mipi_label_addr = ttkbst.Label(MIPI_frame, text="Addr.", font=("Consolas", 8), anchor="center")
Mipi_label_addr.place(x=130, y=5, width=30, height=26)
Mipi_label_data = ttkbst.Label(MIPI_frame, text="Data", font=("Consolas", 8), anchor="center")
Mipi_label_data.place(x=165, y=5, width=30, height=26)

# %%
s.configure("MIPI.TButton", font=("Calibri", 8, "bold"))

Btn_LB_PAW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_W(text_area, "LTE", Mipi_data["LB_PA"], combo4)],
)
Btn_LB_PAW.place(x=200, y=32, width=35, height=26)

Btn_LB_PAR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_R(text_area, "LTE", Mipi_data["LB_PA"], combo4)],
)
Btn_LB_PAR.place(x=240, y=32, width=35, height=26)

# %%
Btn_LB_SMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_W(text_area, "LTE", Mipi_data["LB_SM"], combo4)],
)
Btn_LB_SMW.place(x=200, y=62, width=35, height=26)

Btn_LB_SMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_R(text_area, "LTE", Mipi_data["LB_SM"], combo4)],
)
Btn_LB_SMR.place(x=240, y=62, width=35, height=26)

# %%
Btn_OMH_PAW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_W(text_area, "LTE", Mipi_data["OMH_PA"], combo4)],
)
Btn_OMH_PAW.place(x=200, y=92, width=35, height=26)

Btn_OMH_PAR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_R(text_area, "LTE", Mipi_data["OMH_PA"], combo4)],
)
Btn_OMH_PAR.place(x=240, y=92, width=35, height=26)

# %%
Btn_OMH_SMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_W(text_area, "LTE", Mipi_data["OMH_SM"], combo4)],
)
Btn_OMH_SMW.place(x=200, y=122, width=35, height=26)

Btn_OMH_SMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_R(text_area, "LTE", Mipi_data["OMH_SM"], combo4)],
)
Btn_OMH_SMR.place(x=240, y=122, width=35, height=26)

# %%
Btn_NRPAW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_W(text_area, "NR", Mipi_data["NR_PA"], combo4)],
)
Btn_NRPAW.place(x=200, y=152, width=35, height=26)

Btn_NRPAR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_R(text_area, "NR", Mipi_data["NR_PA"], combo4)],
)
Btn_NRPAR.place(x=240, y=152, width=35, height=26)

# %%
Btn_NRSMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_W(text_area, "NR", Mipi_data["NR_SM"], combo4)],
)
Btn_NRSMW.place(x=200, y=182, width=35, height=26)

Btn_NRSMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="MIPI.TButton",
    command=lambda: [func.Check_mipi_R(text_area, "NR", Mipi_data["NR_SM"], combo4)],
)
Btn_NRSMR.place(x=240, y=182, width=35, height=26)

# %%
# Cal log 파일 선택
path_frame = ttkbst.Frame(Left_frame)
path_frame.place(x=5, y=5, width=755, height=70)

Add_main_loss = ttkbst.Button(
    path_frame,
    text="Main Loss (F11)",
    command=lambda: [func.add_file(Main_loss_path)],
)
Add_main_loss.place(x=0, y=0, width=110, height=30)

Main_loss_path = ttkbst.Entry(path_frame, width=60)
Main_loss_path.insert(
    0,
    "C:\DIST\CONFIG\DASEUL\CABLE_LOSS\MeasuredCableLoss_DUT01_BtoB.dec",
)
Main_loss_path.place(x=115, y=0, width=515, height=30)

Add_sub_loss = ttkbst.Button(
    path_frame,
    text="Sub Loss (F12)",
    command=lambda: [func.add_file(Sub_loss_path)],
)
Add_sub_loss.place(x=0, y=35, width=110, height=30)

Sub_loss_path = ttkbst.Entry(path_frame, width=60)
Sub_loss_path.insert(
    0,
    "C:\DIST\CONFIG\DASEUL\CABLE_LOSS\MeasuredCableLoss_DUT01.dec",
)
Sub_loss_path.place(x=115, y=35, width=515, height=30)

Win_GUI.bind("<F11>", lambda event: [func.add_file(Main_loss_path)])
Win_GUI.bind("<F12>", lambda event: [func.add_file(Sub_loss_path)])

Btn_power = ttkbst.Button(
    path_frame,
    text="Power ON (F4)",
    command=lambda: [threading.Thread(target=func.Power_on, args=(combo2, combo3, combo4, text_area)).start()],
)
Btn_power.place(x=635, y=0, width=120, height=30)
Win_GUI.bind(
    "<F4>",
    lambda event: [threading.Thread(target=func.Power_on, args=(combo2, combo3, combo4, text_area)).start()],
)

# %%
combo_list = [combo1, combo2, combo3, combo4]
for i in combo_list:
    try:
        if i == combo3:
            i.current(1)
        else:
            i.current(0)
    except:
        pass

Rat_Option2.invoke()
Ch_option_var.set(1)  # 1로 세팅만 한다.
Pw_option_var.set(1)
Run_mode_var.set(2)
APT_Tune.config(state=tk.DISABLED)  # APT Tune Disable

# %%
BW_list = blist.Init_BW_Setting(Rat_option_var.get())

Btn_bwsetting = ttkbst.Button(
    Setting_frame,
    text="Define BW (F9)",
    style="danger.TButton",
    command=lambda: [
        BW_list.update(
            blist.BW_setting(
                Rat_option_var.get(),
                Band_index_Main,
                Band_Select_Main_var,
                Band_index_Sub,
                Band_Select_Sub_var,
                BW_list,
            )
        )
    ],
)

Btn_bwsetting.place(x=512, y=11, width=117, height=35)

Win_GUI.bind(
    "<F9>",
    lambda event: [
        BW_list.update(
            blist.BW_setting(
                Rat_option_var.get(),
                Band_index_Main,
                Band_Select_Main_var,
                Band_index_Sub,
                Band_Select_Sub_var,
                BW_list,
            )
        )
    ],
)

# %%
Btn_strt = ttkbst.Button(
    path_frame,
    text="TEST Start (F5)",
    command=lambda: [
        threading.Thread(
            target=func.Start,
            args=(
                Main_loss_path,
                Sub_loss_path,
                combo1,
                combo2,
                combo3,
                combo4,
                Run_mode_var,
                Rat_option_var,
                Ch_option_var,
                User_defined_path,
                User_defined_band,
                User_defined_ch,
                Band_Select_Main_var,
                Band_Select_Sub_var,
                BW_list,
                Pw_option_var,
                Mipi_data,
                canvas,
                fig,
                ax1,
                ax2,
                ax3,
                text_area,
            ),
        ).start()
    ],
)
Btn_strt.place(x=635, y=35, width=120, height=30)

Win_GUI.bind(
    "<F5>",
    lambda event: [
        threading.Thread(
            target=func.Start,
            args=(
                Main_loss_path,
                Sub_loss_path,
                combo1,
                combo2,
                combo3,
                combo4,
                Run_mode_var,
                Rat_option_var,
                Ch_option_var,
                User_defined_path,
                User_defined_band,
                User_defined_ch,
                Band_Select_Main_var,
                Band_Select_Sub_var,
                BW_list,
                Pw_option_var,
                Mipi_data,
                canvas,
                fig,
                ax1,
                ax2,
                ax3,
                text_area,
            ),
        ).start()
    ],
)

# %%
Win_GUI.bind(
    "<F1>",
    lambda event: [
        Run_mode_var.set(1),  # Signaling
        Rat_Option2.invoke(),
        # Rat_option_var.set(2),  # LTE Selected
        Rat_Option1.config(state=tk.NORMAL),  # 3G enable
        Rat_Option2.config(state=tk.NORMAL),  # LTE enable
        Rat_Option3.config(state=tk.DISABLED),  # NR Disable
    ],
)
Win_GUI.bind("<F2>", lambda event: [Callback_CB(combo1, Rat_option_var)])
Win_GUI.bind(
    "<F3>",
    lambda event: [
        Run_mode_var.set(3),  # APT Tuning
        Rat_Option3.invoke(),
        # Rat_option_var.set(3),  # NR Selected
        Rat_Option1.config(state=tk.DISABLED),  # 3G disable
        Rat_Option2.config(state=tk.DISABLED),  # LTE disable
        Rat_Option3.config(state=tk.NORMAL),  # NR enable
    ],
)

# %%
Win_GUI.resizable(False, False)
Win_GUI.mainloop()