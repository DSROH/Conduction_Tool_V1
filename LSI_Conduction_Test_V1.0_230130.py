# %%
import tkinter as tk
import ttkbootstrap as ttkbst
from ttkbootstrap.constants import *
import tkinter.scrolledtext as st

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import matplotlib.pyplot as plt

# plt.rcParams.update({'font.size': 8})
plt.rc("xtick", labelsize=8)
plt.rc("ytick", labelsize=8)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import threading

import Function as func
import Band_list as blist

# %%
CB_list, PS_list, CP_list = func.Equipment_scan()

Win_GUI = ttkbst.Window(title="LSI Conduction Test V1.0")
Win_GUI.attributes("-topmost", True)
Win_GUI.geometry("1625x730")


def change_theme():
    themename = Win_GUI.getvar("themename")
    Win_GUI.style.theme_use(themename)


themes = Win_GUI.style.theme_names()

# %%
Left_frame = ttkbst.Frame(Win_GUI)
Left_frame.place(x=0, y=0, width=765, height=730)

# %%
canvas_frame = ttkbst.Labelframe(Left_frame, text="Canvas")  # Frame의 크기 따로 지정하지 않고, figsize로 결정됨
canvas_frame.place(x=5, y=275, width=755, height=405)

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
ax2.set_ylabel("Power Diff (dB)", fontsize=8)
ax2.grid(True, color="black", alpha=0.3, linestyle="--")

ax3 = plt.subplot(2, 2, 4)
ax3.axis(xmin=0, xmax=25)
ax3.set_xlabel("Measured Power (dBm)", fontsize=8)
ax3.set_ylabel("ACLR (dBc)", fontsize=8)
ax3.grid(True, color="black", alpha=0.3, linestyle="--")

canvas.draw
canvas.get_tk_widget().grid(row=0, column=0, sticky=NSEW)
plt.tight_layout()

plt.close()

# %%
Scrolled_txt_frame = ttkbst.Frame(Win_GUI)
Scrolled_txt_frame.place(x=770, y=5, width=850, height=675)

text_area = st.ScrolledText(Scrolled_txt_frame, font=("Consolas", 9))

text_area.place(x=0, y=0, width=850, height=675)

Auth_frame = ttkbst.Frame(Win_GUI)
Auth_frame.place(x=770, y=685, width=850, height=40)

Author = ttkbst.Label(Auth_frame, text="dongsub.roh@samsung.com")
Author.place(x=690, y=10)

# %%
Setting_frame = ttkbst.Frame(Left_frame)
Setting_frame.place(x=5, y=100, width=755, height=170)

Band_frame = ttkbst.Labelframe(Setting_frame, text="Band")
Band_frame.place(x=0, y=50, width=400, height=120)


def on_select(v):

    global Chbox_var
    global Band_index
    Band_index = []

    for widget in Band_frame.winfo_children():
        widget.destroy()

    if v == 1:  # 3G
        B_list = [1, 2, 4, 5, 8]
        rat = "B"
    elif v == 2:
        B_list = [1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 66, 38, 39, 40, 41]
        rat = "B"
    else:
        B_list = [1, 2, 3, 5, 7, 8, 12, 13, 20, 25, 26, 28, 66, 38, 39, 40, 41, 77, 78]
        rat = "n"

    try:
        if Chbox_var:
            for count, i in enumerate(Chbox_var):
                Chbox_var[count].place_forget()
    except:
        Chbox_var = [None] * len(B_list)
        Chkbox = [None] * len(B_list)

    for count, i in enumerate(B_list):
        Chbox_var[count] = ttkbst.BooleanVar()
        Chkbox[count] = ttkbst.Checkbutton(Band_frame, text=f"{rat}{i}", width=5, variable=Chbox_var[count])
        Band_index.append(f"{rat}{i}")
        if count == 0:
            pos_x = 10
            pos_y = 5
        else:
            pos_x = 10 + 55 * (count % 7)
            pos_y = 5 + 35 * (count // 7)
        Chkbox[count].place(x=pos_x, y=pos_y, width=50)
        Chbox_var[count].set(True)

# %%
Rat_frame = ttkbst.Labelframe(Setting_frame, text="RAT")
Rat_frame.place(x=0, y=0, width=140, height=50)

Rat_option_var = ttkbst.IntVar()
Rat_Option1 = ttkbst.Radiobutton(
    Rat_frame,
    text="3G",
    width=4,
    value=1,
    variable=Rat_option_var,
    command=lambda: on_select(Rat_option_var.get()),
)
Rat_Option1.place(x=10, y=6, width=35)

Rat_Option2 = ttkbst.Radiobutton(
    Rat_frame,
    text="LTE",
    width=4,
    value=2,
    variable=Rat_option_var,
    command=lambda: on_select(Rat_option_var.get()),
)
Rat_Option2.place(x=50, y=6, width=40)

Rat_Option3 = ttkbst.Radiobutton(
    Rat_frame,
    text="NR ",
    width=4,
    value=3,
    variable=Rat_option_var,
    command=lambda: on_select(Rat_option_var.get()),
)
Rat_Option3.place(x=95, y=6, width=40)

# %%
Ch_frame = ttkbst.Labelframe(Setting_frame, text="Channel")
Ch_frame.place(x=145, y=0, width=110, height=50)

Ch_option_var = ttkbst.IntVar()
Ch_Option1 = ttkbst.Radiobutton(Ch_frame, text="1CH ", value=1, variable=Ch_option_var)
Ch_Option1.place(x=5, y=6, width=50)

Ch_Option2 = ttkbst.Radiobutton(Ch_frame, text="3CH ", value=2, variable=Ch_option_var)
Ch_Option2.place(x=55, y=6, width=50)


def func_userch():
    global Band_index
    global ChildWin_userch
    global Combo_user_define_ch
    global Entry_Userdefined_ch
    global User_defined_band
    global User_defined_ch

    try:
        ChildWin_userch.destroy()
    except:
        pass

    ChildWin_userch = ttkbst.Toplevel(title="User Defined Channel")
    ChildWin_userch.attributes("-topmost", True)
    ChildWin_userch.geometry("360x50")

    Band = [x for x in Band_index]
    Combo_user_define_ch = ttkbst.Combobox(ChildWin_userch, values=Band, font=("Calibri", 10))
    Combo_user_define_ch.place(x=10, y=10, width=60, height=30)
    Combo_user_define_ch.current(0)
    Entry_Userdefined_ch = ttkbst.Entry(ChildWin_userch, justify=LEFT, font=("Consolas", 10))
    Entry_Userdefined_ch.insert(0, User_defined_ch)
    Entry_Userdefined_ch.place(x=80, y=10, width=200, height=30)
    OK_btn = ttkbst.Button(ChildWin_userch, text="OK", command=func_userch_ok)
    OK_btn.place(x=290, y=10, width=60, height=30)


def func_userch_ok():
    global Ch_option_var
    global Combo_user_define_ch
    global Entry_Userdefined_ch
    global User_defined_band
    global User_defined_ch

    Ch_option_var.set(3)
    User_defined_band = Combo_user_define_ch.get()
    User_defined_ch = Entry_Userdefined_ch.get()
    ChildWin_userch.destroy()


# User Define 없을 경우 Error 방지 목적으로 빈 리스트 생성, user define 시 값 지정됨
User_defined_band = []
User_defined_ch = []
Btn_user_defined_ch = ttkbst.Button(Setting_frame, text="Ch(F9)", style="danger.TButton", command=func_userch)
Btn_user_defined_ch.place(x=260, y=15, width=60, height=30)
Win_GUI.bind("<F9>", lambda event: [func_userch()])

# %%
global BW_list
BW_list = {}

Btn_bwsetting = ttkbst.Button(
    Setting_frame, text="BW(F10)", style="danger.TButton", command=lambda: blist.BW_setting(Rat_option_var.get())
)
Btn_bwsetting.place(x=325, y=15, width=70, height=30)

Win_GUI.bind("<F10>", lambda event: [blist.BW_setting(Rat_option_var.get())])

# %%
Pw_option_var = ttkbst.IntVar()
Btn_pwsetting = ttkbst.Button(Setting_frame, text="PW(F11)", style="danger.TButton", command=func_userch)
Btn_pwsetting.place(x=400, y=15, width=65, height=30)

Win_GUI.bind("<F11>", lambda event: [func_userch()])

# %%
# Select all 버튼
SelectBtn_frame = ttkbst.Labelframe(Setting_frame, text="Select")
SelectBtn_frame.place(x=405, y=50, width=60, height=120)

Btn_Selectall = ttkbst.Button(SelectBtn_frame, text="All", command=lambda: [blist.Selectall_band(Chbox_var)])
Btn_Selectall.place(x=4, y=0, width=50, height=29)

Btn_Selectfdd = ttkbst.Button(
    SelectBtn_frame, text="FDD", command=lambda: [blist.Selectfdd_band(Rat_option_var, Chbox_var)]
)
Btn_Selectfdd.place(x=4, y=34, width=50, height=29)

Btn_Selecttdd = ttkbst.Button(
    SelectBtn_frame, text="TDD", command=lambda: [blist.Selecttdd_band(Rat_option_var, Chbox_var)]
)
Btn_Selecttdd.place(x=4, y=68, width=50, height=29)

# %%
# 실행 프레임
Bottom_frame = ttkbst.Frame(Left_frame)
Bottom_frame.place(x=5, y=685, width=755, height=40)

# Themecombo = ttkbst.Combobox(Bottom_frame, values=themes, textvariable=theme, font=("Consolas", 8))
# Themecombo.place(x=5, y=8, width=100, height=30)

theme_options = tk.Menubutton(Bottom_frame, text="Select a theme")
menu = tk.Menu(theme_options)

for t in themes:
    menu.add_radiobutton(label=t, variable="themename", command=change_theme)

theme_options["menu"] = menu
theme_options.place(x=0, y=5, width=100, height=30)

# %%
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

# %%
def Callback_CB(combo1, Rat_option_var):
    Call_Box = combo1.get()

    if Call_Box == "GPIB0::20::INSTR":
        Run_mode_var.set(2)  # Non-signaling
        Rat_option_var.set(2)  # LTE Selected
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
                Rat_option_var.set(2),  # LTE Selected
                Rat_Option1.config(state=tk.NORMAL),  # 3G enable
                Rat_Option2.config(state=tk.NORMAL),  # LTE enable
                Rat_Option3.config(state=tk.DISABLED),  # NR Disable
            ],
        )
        Win_GUI.unbind("<F3>")

    elif Call_Box == "TCPIP0::127.0.0.1":
        Run_mode_var.set(2)  # Non-signaling
        Rat_option_var.set(2)  # LTE Selected
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
                Rat_option_var.set(3),
                Rat_Option1.config(state=tk.DISABLED),  # 3G disable
                Rat_Option2.config(state=tk.DISABLED),  # LTE disable
                Rat_Option3.config(state=tk.NORMAL),  # NR enable
            ],
        )

# %%
toolbar_frame = ttkbst.Frame(Left_frame)
toolbar_frame.place(x=5, y=55, width=755, height=40)

Label1 = ttkbst.Label(toolbar_frame, text="Call Box")
Label1.place(x=5, y=10, width=50)
combo1 = ttkbst.Combobox(toolbar_frame, values=CB_list, font=("Calibri", 10))
combo1.place(x=65, y=5, width=125)
combo1.bind("<<ComboboxSelected>>", lambda event: [Callback_CB(combo1, Rat_option_var)])

Label2 = ttkbst.Label(toolbar_frame, text="System Power")
Label2.place(x=205, y=10, width=80)
combo2 = ttkbst.Combobox(toolbar_frame, values=PS_list, font=("Calibri", 10))
combo2.place(x=295, y=5, width=115)
combo2.bind("<<ComboboxSelected>>", lambda event: [func.Callback_Sys_P(combo2)])

Label3 = ttkbst.Label(toolbar_frame, text="PA VCC")
Label3.place(x=425, y=10, width=50)
combo3 = ttkbst.Combobox(toolbar_frame, values=PS_list, font=("Calibri", 10))
combo3.place(x=485, y=5, width=115)
combo3.bind("<<ComboboxSelected>>", lambda event: [func.Callback_PA_Vcc(combo3)])

Label4 = ttkbst.Label(toolbar_frame, text="COM Port")
Label4.place(x=615, y=10, width=60)
combo4 = ttkbst.Combobox(toolbar_frame, values=CP_list, font=("Calibri", 10))
combo4.place(x=685, y=5, width=70)
combo4.bind("<<ComboboxSelected>>", lambda event: [func.Callback_Comport(combo4)])

# %%
MIPI_frame = ttkbst.Labelframe(Setting_frame, text="MIPI")
MIPI_frame.place(x=470, y=0, width=285, height=170)

Mipi_Label = [None, None, None, None]

Mipi_data = {
    "LB_PA": [2, 13, 29, 0],
    "LB_SM": [2, 5, 29, 0],
    "OMH_PA": [0, 14, 29, 0],
    "OMH_SM": [0, 5, 29, 0],
}

LB_posx = [60, 95, 130, 165]
LB_posy = {
    "LB_PA": [5, 5, 5, 5],
    "LB_SM": [40, 40, 40, 40],
    "OMH_PA": [75, 75, 75, 75],
    "OMH_SM": [110, 110, 110, 110],
}

for count, i in enumerate(Mipi_data):
    Mipi_Label[count] = ttkbst.Label(MIPI_frame, text=f"{i}", font=("Consolas", 10), anchor="e")
    for c, j in enumerate(Mipi_data[i]):
        Mipi_data[i][c] = ttkbst.Entry(MIPI_frame, justify=RIGHT, font=("Consolas", 10))
        Mipi_data[i][c].insert(0, j)
        Mipi_data[i][c].place(x=LB_posx[c], y=LB_posy[i][c], width=30, height=25)
        Mipi_Label[count].place(x=0, y=LB_posy[i][c], width=50, height=25)

# %%
Btn_LB_PAW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["LB_PA"], combo4)],
)
Btn_LB_PAW.place(x=200, y=5, width=35, height=25)

Btn_LB_PAR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["LB_PA"], combo4)],
)
Btn_LB_PAR.place(x=240, y=5, width=35, height=25)

# %%
Btn_LB_SMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["LB_SM"], combo4)],
)
Btn_LB_SMW.place(x=200, y=40, width=35, height=25)

Btn_LB_SMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["LB_SM"], combo4)],
)
Btn_LB_SMR.place(x=240, y=40, width=35, height=25)

# %%
Btn_OMHW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["OMH_PA"], combo4)],
)
Btn_OMHW.place(x=200, y=75, width=35, height=25)

Btn_OMHR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["OMH_PA"], combo4)],
)
Btn_OMHR.place(x=240, y=75, width=35, height=25)

# %%
Btn_OMH_SMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["OMH_SM"], combo4)],
)
Btn_OMH_SMW.place(x=200, y=110, width=35, height=25)

Btn_OMH_SMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["OMH_SM"], combo4)],
)
Btn_OMH_SMR.place(x=240, y=110, width=35, height=25)

# %%
# Cal log 파일 선택
path_frame = ttkbst.Frame(Left_frame)
path_frame.place(x=5, y=5, width=755, height=45)

log_path = ttkbst.Entry(path_frame, width=60)
log_path.insert(
    0,
    "C:\DIST\CONFIG\DASEUL\CABLE_LOSS\MeasuredCableLoss_DUT01_BtoB.dec",
)
log_path.place(x=120, y=7, width=385, height=30)

Btn_add_file = ttkbst.Button(
    path_frame,
    text="Loss Table (F12)",
    command=lambda: [func.add_file(log_path)],
)
Btn_add_file.place(x=5, y=7, width=110, height=30)
Win_GUI.bind("<F12>", lambda event: [func.add_file(log_path)])

# %%
Btn_power = ttkbst.Button(
    path_frame,
    text="Power ON (F4)",
    command=lambda: [threading.Thread(target=func.Power_on, args=(combo2, combo3, combo4, text_area)).start()],
)
Btn_power.place(x=510, y=7, width=120, height=30)
Win_GUI.bind(
    "<F4>",
    lambda event: [threading.Thread(target=func.Power_on, args=(combo2, combo3, combo4, text_area)).start()],
)

# %%
Btn_strt = ttkbst.Button(
    path_frame,
    text="TEST Start (F5)",
    command=lambda: [
        threading.Thread(
            target=func.Start,
            args=(
                log_path,
                combo1,
                combo2,
                combo3,
                combo4,
                Run_mode_var,
                Rat_option_var,
                Ch_option_var,
                User_defined_band,
                User_defined_ch,
                Chbox_var,
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
Btn_strt.place(x=635, y=7, width=120, height=30)

Win_GUI.bind(
    "<F5>",
    lambda event: [
        threading.Thread(
            target=func.Start,
            args=(
                log_path,
                combo1,
                combo2,
                combo3,
                combo4,
                Run_mode_var,
                Rat_option_var,
                Ch_option_var,
                User_defined_band,
                User_defined_ch,
                Chbox_var,
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
# combo1.current(0)
# combo2.current(0)
# combo3.current(1)
# combo4.current(0)

Rat_Option2.invoke()
Ch_option_var.set(1)  # 1로 세팅만 한다.
Pw_option_var.set(1)
Run_mode_var.set(1)

Win_GUI.bind(
    "<F1>",
    lambda event: [
        Run_mode_var.set(1),  # Signaling
        Rat_option_var.set(2),  # LTE Selected
        Rat_Option1.config(state=tk.NORMAL),  # 3G enable
        Rat_Option2.config(state=tk.NORMAL),  # LTE enable
        Rat_Option3.config(state=tk.DISABLED),  # NR Disable
    ],
)
Win_GUI.bind("<F2>", lambda event: [Callback_CB(combo1, Rat_option_var)])
Win_GUI.bind(
    "<F3>",
    lambda event: [
        Run_mode_var.set(3),
        Rat_option_var.set(3),
        Rat_Option1.config(state=tk.DISABLED),  # 3G disable
        Rat_Option2.config(state=tk.DISABLED),  # LTE disable
        Rat_Option3.config(state=tk.NORMAL),  # NR enable
    ],
)

# %%
Win_GUI.resizable(False, False)
Win_GUI.mainloop()


