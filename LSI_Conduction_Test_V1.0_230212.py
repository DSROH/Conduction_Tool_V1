# %%
import tkinter as tk
import ttkbootstrap as ttkbst
import tkinter.font as font
from ttkbootstrap.constants import *
import tkinter.scrolledtext as st
import tkinter.messagebox as msgbox

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
Win_GUI.geometry("1625x805")


def change_theme():
    themename = Win_GUI.getvar("themename")
    Win_GUI.style.theme_use(themename)


themes = Win_GUI.style.theme_names()

# %%
Left_frame = ttkbst.Frame(Win_GUI)
Left_frame.place(x=0, y=0, width=765, height=805)

# %%
canvas_frame = ttkbst.Labelframe(Left_frame, text="Canvas")  # Frame의 크기 따로 지정하지 않고, figsize로 결정됨
canvas_frame.place(x=5, y=350, width=755, height=405)

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

# ax4 = plt.subplot(2, 2, 3)
# ax4.remove()

canvas.draw
canvas.get_tk_widget().grid(row=0, column=0, sticky=NSEW)
plt.tight_layout()

plt.close()

# %%
Scrolled_txt_frame = ttkbst.Frame(Win_GUI)
Scrolled_txt_frame.place(x=765, y=5, width=855, height=755)

text_area = st.ScrolledText(Scrolled_txt_frame, font=("Consolas", 9))
text_area.place(x=0, y=0, width=855, height=750)

Auth_frame = ttkbst.Frame(Win_GUI)
Auth_frame.place(x=765, y=760, width=855, height=40)

Author = ttkbst.Label(Auth_frame, text="dongsub.roh@samsung.com")
Author.place(x=685, y=10)

# %%
Setting_frame = ttkbst.Frame(Left_frame)
Setting_frame.place(x=5, y=100, width=755, height=250)

TX_Main_frame = ttkbst.Labelframe(Setting_frame, text="TX Main")
TX_Main_frame.place(x=0, y=50, width=400, height=120)


def Select_Main(v):

    global Band_Select_Main_var
    global Band_index_Main
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
            TX_Main_frame, text=f"{rat}{i}", width=5, variable=Band_Select_Main_var[count]
        )
        Band_index_Main.append(f"{rat}{i}")
        if count == 0:
            pos_x = 10
            pos_y = 5
        else:
            pos_x = 10 + 55 * (count % 7)
            pos_y = 5 + 35 * (count // 7)
        Chkbox_Main[count].place(x=pos_x, y=pos_y, width=50)
        Band_Select_Main_var[count].set(True)

# %%
TX_Sub_frame = ttkbst.Labelframe(Setting_frame, text="TX Sub")
TX_Sub_frame.place(x=0, y=170, width=400, height=80)


def Select_Sub(v):

    global Band_Select_Sub_var
    global Band_index_Sub
    Band_index_Sub = []

    for widget in TX_Sub_frame.winfo_children():
        widget.destroy()

    if v == 1:  # 3G
        B_list_Sub = [1, 2, 4]
        rat = "B"
    elif v == 2:
        B_list_Sub = [1, 2, 3, 4, 7, 25, 28, 66, 38, 39, 40, 41]
        rat = "B"
    elif v == 3:
        B_list_Sub = [1, 2, 3, 7, 25, 28, 66, 38, 39, 40, 41, 77, 78]
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
        Chkbox_Sub[count].place(x=pos_x, y=pos_y, width=50)
        Band_Select_Sub_var[count].set(True)

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
    command=lambda: [Select_Main(Rat_option_var.get()), Select_Sub(Rat_option_var.get())],
)
Rat_Option1.place(x=10, y=6, width=35)

Rat_Option2 = ttkbst.Radiobutton(
    Rat_frame,
    text="LTE",
    width=4,
    value=2,
    variable=Rat_option_var,
    command=lambda: [Select_Main(Rat_option_var.get()), Select_Sub(Rat_option_var.get())],
)
Rat_Option2.place(x=50, y=6, width=40)

Rat_Option3 = ttkbst.Radiobutton(
    Rat_frame,
    text="NR ",
    width=4,
    value=3,
    variable=Rat_option_var,
    command=lambda: [Select_Main(Rat_option_var.get()), Select_Sub(Rat_option_var.get())],
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
    global Band_index_Main
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

    Band = [x for x in Band_index_Main]
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
Btn_user_defined_ch = ttkbst.Button(Setting_frame, text="User Defined CH (F9)", style="danger.TButton", command=func_userch)
Btn_user_defined_ch.place(x=260, y=15, width=140, height=30)
Win_GUI.bind("<F9>", lambda event: [func_userch()])

# %%
Pw_option_var = ttkbst.IntVar()
Btn_pwsetting = ttkbst.Button(Setting_frame, text="Power Level (F11)", style="danger.TButton", command=func_userch)
Btn_pwsetting.place(x=525, y=15, width=120, height=30)

Win_GUI.bind("<F11>", lambda event: [func_userch()])

# %%
# Select all 버튼
Select_Main_frame = ttkbst.Labelframe(Setting_frame, text="Main")
Select_Main_frame.place(x=405, y=50, width=60, height=120)

Select_Mainall = ttkbst.Button(
    Select_Main_frame, text="All", command=lambda: [blist.Selectall_band(Band_Select_Main_var)]
)
Select_Mainall.place(x=4, y=0, width=50, height=29)

Select_Mainfdd = ttkbst.Button(
    Select_Main_frame, text="FDD", command=lambda: [blist.Selectfdd_band(Rat_option_var, Band_Select_Main_var)]
)
Select_Mainfdd.place(x=4, y=34, width=50, height=29)

Select_Maintdd = ttkbst.Button(
    Select_Main_frame, text="TDD", command=lambda: [blist.Selecttdd_band(Rat_option_var, Band_Select_Main_var)]
)
Select_Maintdd.place(x=4, y=68, width=50, height=29)

# %%
# Select all 버튼
Select_Sub_frame = ttkbst.Labelframe(Setting_frame, text="Sub")
Select_Sub_frame.place(x=405, y=170, width=60, height=80)

Select_Subfdd = ttkbst.Button(
    Select_Sub_frame, text="FDD", command=lambda: [blist.Selectfdd_band(Rat_option_var, Band_Select_Sub_var)]
)
Select_Subfdd.place(x=4, y=0, width=50, height=27)

Select_Subtdd = ttkbst.Button(
    Select_Sub_frame, text="TDD", command=lambda: [blist.Selecttdd_band(Rat_option_var, Band_Select_Sub_var)]
)
Select_Subtdd.place(x=4, y=31, width=50, height=27)

# %%
# 실행 프레임
Bottom_frame = ttkbst.Frame(Left_frame)
Bottom_frame.place(x=5, y=760, width=755, height=40)

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
                Rat_option_var.set(3), # NR Main Selected
                Rat_Option1.config(state=tk.DISABLED),  # 3G disable
                Rat_Option2.config(state=tk.DISABLED),  # LTE disable
                Rat_Option3.config(state=tk.NORMAL),  # NR enable
            ],
        )
    else:
        msgbox.showwarning("Warning", "Select Call_Box")

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
MIPI_frame.place(x=470, y=50, width=285, height=200)

Mipi_data = {
    "LB_PA": [2, 13, 29, 0],
    "LB_SM": [2, 5, 29, 0],
    "OMH_PA": [0, 14, 29, 0],
    "OMH_SM": [0, 5, 29, 0],
    "NR PA": [0, 0, 0, 0],
    "NR SM": [0, 0, 0, 0],
}
Mipi_Label = [None] * len(Mipi_data)

LB_posx = [60, 95, 130, 165, 200, 235]
LB_posy = {
    "LB_PA": [2, 2, 2, 2],
    "LB_SM": [32, 32, 32, 32],
    "OMH_PA": [62, 62, 62, 62],
    "OMH_SM": [92, 92, 92, 92],
    "NR PA": [122, 122, 122, 122],
    "NR SM": [152, 152, 152, 152],
}

for count, i in enumerate(Mipi_data):
    Mipi_Label[count] = ttkbst.Label(MIPI_frame, text=f"{i}", font=("Consolas", 8), anchor="e")
    for c, j in enumerate(Mipi_data[i]):
        Mipi_data[i][c] = ttkbst.Entry(MIPI_frame, justify=RIGHT, font=("Consolas", 8))
        Mipi_data[i][c].insert(0, j)
        Mipi_data[i][c].place(x=LB_posx[c], y=LB_posy[i][c], width=30, height=26)
        Mipi_Label[count].place(x=0, y=LB_posy[i][c], width=50, height=26)

# %%
s = ttkbst.Style()
s.configure("my.TButton", font=("Calibri", 8, "bold"))

Btn_LB_PAW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["LB_PA"], combo4)],
)
Btn_LB_PAW.place(x=200, y=2, width=35, height=26)

Btn_LB_PAR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["LB_PA"], combo4)],
)
Btn_LB_PAR.place(x=240, y=2, width=35, height=26)

# %%
Btn_LB_SMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["LB_SM"], combo4)],
)
Btn_LB_SMW.place(x=200, y=32, width=35, height=26)

Btn_LB_SMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["LB_SM"], combo4)],
)
Btn_LB_SMR.place(x=240, y=32, width=35, height=26)

# %%
Btn_OMHW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["OMH_PA"], combo4)],
)
Btn_OMHW.place(x=200, y=62, width=35, height=26)

Btn_OMHR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["OMH_PA"], combo4)],
)
Btn_OMHR.place(x=240, y=62, width=35, height=26)

# %%
Btn_OMH_SMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["OMH_SM"], combo4)],
)
Btn_OMH_SMW.place(x=200, y=92, width=35, height=26)

Btn_OMH_SMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["OMH_SM"], combo4)],
)
Btn_OMH_SMR.place(x=240, y=92, width=35, height=26)

# %%
Btn_NRPAW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["NR_PA"], combo4)],
)
Btn_NRPAW.place(x=200, y=122, width=35, height=26)

Btn_NRPAR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["NR_PA"], combo4)],
)
Btn_NRPAR.place(x=240, y=122, width=35, height=26)

# %%
Btn_NRSMW = ttkbst.Button(
    MIPI_frame,
    text="W",
    style="my.TButton",
    command=lambda: [func.Check_mipi_W(text_area, Mipi_data["NR_SM"], combo4)],
)
Btn_NRSMW.place(x=200, y=152, width=35, height=26)

Btn_NRSMR = ttkbst.Button(
    MIPI_frame,
    text="R",
    style="my.TButton",
    command=lambda: [func.Check_mipi_R(text_area, Mipi_data["NR_SM"], combo4)],
)
Btn_NRSMR.place(x=240, y=152, width=35, height=26)

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
# combo1.current(0)
# combo2.current(0)
# combo3.current(1)
# combo4.current(0)

Rat_Option2.invoke()
Ch_option_var.set(1)  # 1로 세팅만 한다.
Pw_option_var.set(1)
Run_mode_var.set(2)

# %%
BW_list = blist.Init_BW_Setting(Rat_option_var.get(), Band_index_Main, Band_Select_Main_var)

Btn_bwsetting = ttkbst.Button(
    Setting_frame,
    text="Define BW (F10)",
    style="danger.TButton",
    command=lambda: [
        BW_list.update(blist.BW_setting(Rat_option_var.get(), Band_index_Main, Band_Select_Main_var, BW_list))
    ],
)
Btn_bwsetting.place(x=405, y=15, width=115, height=30)

Win_GUI.bind(
    "<F10>",
    lambda event: [
        BW_list.update(blist.BW_setting(Rat_option_var.get(), Band_index_Main, Band_Select_Main_var, BW_list))
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
                Band_Select_Main_var,
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
                Band_Select_Main_var,
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


