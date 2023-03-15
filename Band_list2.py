def Selectall_band(Rat_option_var, TX_path, Band_Select_var):
    chk = []

    for c, i in enumerate(Band_Select_var):
        if (Rat_option_var.get() == 2) & (TX_path == "Sub") & (c in [4, 6, 7, 8, 9, 10, 11, 12, 14]):
            pass
        elif (Rat_option_var.get() == 3) & (TX_path == "Main") & (c in [14]):
            pass
        elif (Rat_option_var.get() == 3) & (TX_path == "Sub") & (c in [3, 5, 6, 7, 8, 10, 14, 17, 18]):
            pass
        else:
            chk.append(Band_Select_var[c].get())

    if all(chk):
        # 한개라도 체크되있다면, 전체 체크 해제
        for count, j in enumerate(Band_Select_var):
            Band_Select_var[count].set(False)
    else:
        for count, j in enumerate(Band_Select_var):
            if (Rat_option_var.get() == 2) & (TX_path == "Sub") & (count in [4, 6, 7, 8, 9, 10, 11, 12, 14]):
                pass
            elif (Rat_option_var.get() == 3) & (TX_path == "Main") & (count in [14]):
                pass
            elif (Rat_option_var.get() == 3) & (TX_path == "Sub") & (count in [3, 5, 6, 7, 8, 10, 14, 17, 18]):
                pass
            else:
                Band_Select_var[count].set(True)


def Selectfdd_band(Rat_option_var, TX_path, Band_Select_var):
    if Rat_option_var.get() == 2:  # LTE Main
        if TX_path == "Main":
            Select_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        elif TX_path == "Sub":
            Select_list = [0, 1, 2, 3, 5, 13, 15, 16]

        for c, i in enumerate(Band_Select_var):
            # Band_Select_var[c].set(not Band_Select_var[c].get())
            if TX_path == "Main":
                if c in Select_list:
                    Band_Select_var[c].set(True)
                else:
                    Band_Select_var[c].set(False)
            elif TX_path == "Sub":
                if c in Select_list:
                    Band_Select_var[c].set(True)
                else:
                    Band_Select_var[c].set(False)

    elif Rat_option_var.get() == 3:  # NR Main
        if TX_path == "Main":
            Select_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        elif TX_path == "Sub":
            Select_list = [0, 1, 2, 4, 9, 11, 12]

        for c, i in enumerate(Band_Select_var):
            # Band_Select_var[c].set(not Band_Select_var[c].get())
            if TX_path == "Main":
                if c in Select_list:
                    Band_Select_var[c].set(True)
                else:
                    Band_Select_var[c].set(False)
            elif TX_path == "Sub":
                if c in Select_list:
                    Band_Select_var[c].set(True)
                else:
                    Band_Select_var[c].set(False)


def Selecttdd_band(Rat_option_var, TX_path, Band_Select_var):
    if Rat_option_var.get() == 2:  # LTE Main
        if TX_path == "Main":
            Select_list = [17, 18, 19, 20]
        elif TX_path == "Sub":
            Select_list = [17, 18, 19, 20]

        for c, i in enumerate(Band_Select_var):
            if c in Select_list:
                Band_Select_var[c].set(True)
            else:
                Band_Select_var[c].set(False)

    elif Rat_option_var.get() == 3:  # NR Main
        if TX_path == "Main":
            Select_list = [13, 15, 16, 17, 18]
        elif TX_path == "Sub":
            Select_list = [13, 15, 16]

        for c, i in enumerate(Band_Select_var):
            if c in Select_list:
                Band_Select_var[c].set(True)
            else:
                Band_Select_var[c].set(False)


def Num_RB(rat, band, BW):
    if rat == "LTE":
        RB = {
            5: [25, 0, 8, 0],  # NRB, outfull_offset, PRB, infull_offset
            10: [50, 0, 12, 0],
            15: [75, 0, 16, 0],
            20: [100, 0, 18, 0],
        }
    elif rat == "NR":
        if band in [38, 39, 40, 41, 77, 78]:
            RB = {
                5: [25, 0, 5, 2],  # NRB, outfull_offset, PRB, infull_offset
                10: [24, 0, 12, 6],
                15: [36, 0, 18, 9],
                20: [50, 0, 25, 12],
                25: [64, 0, 32, 16],
                30: [75, 0, 36, 18],
                40: [100, 0, 50, 25],
                50: [128, 0, 64, 32],
                60: [162, 0, 81, 40],
                70: [180, 0, 90, 45],
                80: [216, 0, 108, 54],
                90: [243, 0, 120, 60],
                100: [270, 0, 135, 67],
            }
        else:
            RB = {
                5: [25, 0, 12, 6],  # NRB, outfull_offset, PRB, infull_offset
                10: [50, 0, 25, 12],
                15: [75, 0, 36, 18],
                20: [100, 0, 50, 25],
                25: [128, 0, 64, 32],
                30: [160, 0, 80, 40],
                40: [216, 0, 108, 54],
                50: [270, 0, 135, 67],
            }

    return RB[BW][0], RB[BW][1], RB[BW][2], RB[BW][3]


def channel_converter(band, channel):

    Info_freq_calc = {
        # fdl_low, ndl_offset, ful_low, nul_offset
        1: [2110, 0, 1920, 18000],
        2: [1930, 600, 1850, 18600],
        3: [1805, 1200, 1710, 19200],
        4: [2110, 1950, 1710, 19950],
        5: [869, 2400, 824, 20400],
        7: [2620, 2750, 2500, 20750],
        8: [925, 3450, 880, 21450],
        12: [729, 5010, 699, 23010],
        13: [746, 5180, 777, 23180],
        17: [734, 5730, 704, 23730],
        18: [860, 5850, 815, 23850],
        19: [875, 6000, 830, 24000],
        20: [791, 6150, 832, 24150],
        25: [1930, 8040, 1850, 26040],
        26: [859, 8690, 814, 26690],
        28: [758, 9210, 703, 27210],
        66: [2110, 66436, 1710, 131972],
        38: [2570, 37750, 2570, 37750],
        39: [1880, 38250, 1880, 38250],
        40: [2300, 38650, 2300, 38650],
        41: [2496, 39650, 2496, 39650],
    }

    freq_separation = {
        1: [190],
        2: [80],
        3: [95],
        4: [400],
        5: [45],
        7: [120],
        8: [45],
        12: [30],
        13: [-31],
        17: [30],
        18: [45],
        19: [45],
        20: [-41],
        25: [80],
        26: [45],
        28: [55],
        66: [400],
        38: [0],
        39: [0],
        40: [0],
        41: [0],
    }

    # rxfreq = fdl_low, + 0.1*(ndl - ndl_offset)
    # txfreq = ful_low, + 0.1*(nul - nul_offset)
    rx = int((Info_freq_calc[band][0] + 0.1 * (channel - Info_freq_calc[band][1])) * 1000)
    tx = int((rx / 1000 - freq_separation[band][0]) * 1000)

    # tx = rx - np.float_(freq_separation[band][0])
    # tx = Info_freq_calc[band][2] + 0.1 * (channel - Info_freq_calc[band][3])

    return rx, tx


def NR_channel_converter(band, channel):

    Info_freq_calc = {
        # fdl_low, nref_offset, ful_low, delta_f, freq_offset
        1: [2110, 0, 1920, 5, 0],
        2: [1930, 0, 1850, 5, 0],
        3: [1805, 0, 1710, 5, 0],
        5: [869, 0, 824, 5, 0],
        7: [2620, 0, 2500, 5, 0],
        8: [925, 0, 880, 5, 0],
        12: [729, 0, 699, 5, 0],
        13: [746, 0, 777, 5, 0],
        18: [860, 0, 815, 5, 0],
        20: [791, 0, 832, 5, 0],
        25: [1930, 0, 1850, 5, 0],
        26: [859, 0, 814, 5, 0],
        28: [758, 0, 703, 5, 0],
        66: [2110, 0, 1710, 5, 0],
        38: [2570, 0, 2570, 5, 0],
        39: [1880, 0, 1880, 5, 0],
        40: [2300, 0, 2300, 5, 0],
        41: [2496, 0, 2496, 5, 0],
        77: [3300, 600000, 3300, 15, 3000],
        78: [3300, 600000, 3300, 15, 3000],
    }

    freq_separation = {
        1: [190],
        2: [80],
        3: [95],
        5: [45],
        7: [120],
        8: [45],
        12: [30],
        13: [-31],
        18: [45],
        20: [-41],
        25: [80],
        26: [45],
        28: [55],
        66: [400],
        38: [0],
        39: [0],
        40: [0],
        41: [0],
        77: [0],
        78: [0],
    }

    # rxfreq = fref_offset + delta_f * (nref - nref_offset)
    # txfreq = ful_low, + 0.1*(nul - nul_offset)
    delta_f = Info_freq_calc[band][3] * 1000
    freq_offset = Info_freq_calc[band][4] * 1000000
    rx = int((freq_offset + (delta_f * (channel - Info_freq_calc[band][1]))) / 1000)
    tx = int((rx / 1000 - freq_separation[band][0]) * 1000)

    return rx, tx


def Check_pwr_lvs(rat, variable):
    pwr_levels = []
    if rat == 2:  # LTE
        if variable == 1:
            pwr_levels = [24, 23, 20, 15, 10, 5, 0]
        elif variable == 2:
            for i in range(24, -1, -3):
                pwr_levels.append(i)
        elif variable == 3:
            for i in range(24, -1, -1):
                pwr_levels.append(i)
        elif variable == 4:
            for i in range(24, -11, -1):
                pwr_levels.append(i)
        elif variable == 5:
            for i in range(24, -46, -1):
                pwr_levels.append(i)
    elif rat == 3:  # NR
        if variable == 1:
            pwr_levels = [25, 23, 20, 15, 10, 5, 0]
        elif variable == 2:
            for i in range(25, -1, -3):
                pwr_levels.append(i)
        elif variable == 3:
            for i in range(25, -1, -1):
                pwr_levels.append(i)
        elif variable == 4:
            for i in range(25, -11, -1):
                pwr_levels.append(i)
        elif variable == 5:
            for i in range(25, -46, -1):
                pwr_levels.append(i)

    return pwr_levels


def Power_setting(Pw_option_var):
    global ChildWin_pw

    try:
        ChildWin_pw.destroy()
    except:
        pass
    ChildWin_pw = ttkbst.Toplevel(title="Power Levels Setting")
    ChildWin_pw.attributes("-topmost", True)
    win_width = 200
    win_height = 210
    ChildWin_pw.geometry(f"{win_width}x{win_height}")
    Range_text = ["5dB Step", "3dB Step", "Max. Power ~ 0dBm", "Max. Power ~ -10dBm", "Max. Power ~ Min. Power"]
    Range = [None] * len(Range_text)
    posx = 10

    for i in range(len(Range_text)):
        Range[i] = ttkbst.Radiobutton(
            ChildWin_pw,
            text=Range_text[i],
            value=i + 1,
            variable=Pw_option_var,
        )
        posy = 30 * i + 10
        Range[i].place(x=posx, y=posy, width=180, height=30)

    Pwr_btn_ok = ttkbst.Button(ChildWin_pw, text="OK", bootstyle="info")
    Pwr_btn_ok.place(x=145, y=170, width=45, height=30)
    Pwr_btn_ok.config(command=lambda: [Power_btn_ok()])

    scr_width = int(ChildWin_pw.winfo_screenwidth())
    scr_height = int(ChildWin_pw.winfo_screenheight())
    x = int((scr_width - win_width) / 2)
    y = int((scr_height - win_height) / 2)
    ChildWin_pw.geometry(f"{win_width}x{win_height}+{x}+{y}")
    ChildWin_pw.resizable(False, False)
    ChildWin_pw.bind("<Return>", lambda event: [Power_btn_ok()])
    ChildWin_pw.focus()

    return Pw_option_var


def Power_btn_ok():
    global ChildWin_pw
    ChildWin_pw.destroy()


def Init_BW_Setting(v):

    if v == 1:  # 3G
        BW_list = {
            0: {
                1: [5],
                2: [5],
                4: [5],
                5: [5],
                8: [5],
            },
            1: {
                1: [5],
                2: [5],
                4: [5],
            },
        }

    elif v == 2:  # LTE
        BW_list = {
            0: {
                1: [10],
                2: [10],
                3: [10],
                4: [10],
                5: [10],
                7: [10],
                8: [10],
                12: [10],
                13: [10],
                17: [10],
                18: [10],
                19: [10],
                20: [10],
                25: [10],
                26: [10],
                28: [10],
                66: [10],
                38: [10],
                39: [10],
                40: [10],
                41: [10],
            },
            1: {
                1: [10],
                2: [10],
                3: [10],
                4: [10],
                7: [10],
                25: [10],
                28: [10],
                66: [10],
                38: [10],
                39: [10],
                40: [10],
                41: [10],
            },
        }
    elif v == 3:  # NR
        BW_list = {
            0: {
                1: [10],
                2: [10],
                3: [10],
                5: [10],
                7: [10],
                8: [10],
                12: [10],
                13: [10],
                18: [10],
                20: [10],
                25: [10],
                26: [10],
                28: [10],
                66: [10],
                38: [10],
                39: [10],
                40: [10],
                41: [10],
                77: [10],
                78: [10],
            },
            1: {
                1: [10],
                2: [10],
                3: [10],
                7: [10],
                25: [10],
                28: [10],
                66: [10],
                38: [10],
                39: [10],
                40: [10],
                41: [10],
                77: [10],
                78: [10],
            },
        }

    return BW_list


def BW_setting(v, Band_index_Main, Band_Select_Main_var, Band_index_Sub, Band_Select_Sub_var, BW_list):

    global ChildWin_bw
    global Band_list_var
    global BW_list_var
    global BW_Label

    Active_band_main = []
    Active_band_sub = []
    if Band_index_Main:
        for c, i in enumerate(Band_Select_Main_var):
            if Band_Select_Main_var[c].get():
                Active_band_main.append(int(Band_index_Main[c][1:]))

    if Band_index_Sub:
        for c, i in enumerate(Band_Select_Sub_var):
            if Band_Select_Sub_var[c].get():
                Active_band_sub.append(int(Band_index_Sub[c][1:]))

    rat, dict1 = dict_compare_list(v, Active_band_main)
    rat, dict2 = dict_compare_list(v, Active_band_sub)

    Band_list = {0: dict1, 1: dict2}

    try:
        ChildWin_bw.destroy()
    except:
        pass
    BW_frame = {0: [], 1: []}
    Band_list_var = {0: [], 1: []}
    BW_list_var = {0: [], 1: []}
    BW_Label = {0: [], 1: []}
    ChildWin_bw = ttkbst.Toplevel(title="Bandwidth Setting")
    ChildWin_bw.attributes("-topmost", True)
    x_max = [0, 0]
    y_max = [0, 0]
    x_start = [0, 0]

    for key in Band_list:
        if Band_list[key]:
            if key == 0:
                BW_frame[key] = ttkbst.Labelframe(ChildWin_bw, text="Main")
            elif key == 1:
                BW_frame[key] = ttkbst.Labelframe(ChildWin_bw, text="Sub")

            Band_list_var[key] = [None] * len(Band_list[key])
            BW_list_var[key] = [None] * len(Band_list[key])
            BW_Label[key] = [None] * len(Band_list[key])

            geom_max_x = []
            geom_max_y = []

            for count, i in enumerate(Band_list[key]):
                pos_x1 = 10
                pos_y1 = 5 + 35 * count
                Band_list_var[key][count] = ttkbst.Label(BW_frame[key], text=f"{rat}{i}")
                Band_list_var[key][count].place(x=pos_x1, y=pos_y1, width=45, height=30)

                BW_list_var[key][count] = [None] * len(Band_list[key].get(i))
                BW_Label[key][count] = [None] * len(Band_list[key].get(i))
                # print(f"Band_list[0].get(i) = {Band_list[0].get(i)}, count = {len(Band_list[0].get(i))}")

                for c, k in enumerate(Band_list[key].get(i)):
                    BW_list_var[key][count][c] = ttkbst.BooleanVar()
                    pos_x2 = 50 + 50 * c
                    BW_Label[key][count][c] = ttkbst.Checkbutton(
                        BW_frame[key], text=f"{k}", variable=BW_list_var[key][count][c]
                    )
                    BW_Label[key][count][c].place(x=pos_x2, y=pos_y1, width=45, height=30)
                    BW_list_var[key][count][c].set(True)
                    geom_max_x.append(pos_x2)
                    geom_max_y.append(pos_y1)

                    if v == 3:
                        if (i in [7]) & (k in [30, 40]):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [8]) & (k in [25, 30]):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [28, 41]) & (k in [25]):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [38, 39, 40, 41, 77, 78]) & (k == 5):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [40]) & (k in [70]):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif k in [35, 45]:
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)

            if key == 0:
                x_max[0] = max(geom_max_x) + 50
                x_start[0] = key * x_max[0] + key * 5 + 5
                y_max[0] = max(geom_max_y) + 60
                BW_frame[key].place(x=x_start[0], y=5, width=x_max[0], height=y_max[0])
            elif key == 1:
                x_max[1] = max(geom_max_x) + 50
                x_start[1] = key * x_max[0] + key * 5 + 5
                y_max[1] = max(geom_max_y) + 60
                BW_frame[key].place(x=x_start[1], y=5, width=x_max[1], height=y_max[1])
        else:
            if key == 0:
                y_max[0] = 0
            elif key == 1:
                y_max[1] = 0

    max_x = max(x_max)
    max_y = max(y_max)
    StartX = max(x_start)

    if v == 1:
        if y_max[1] == 0:
            win_width = x_max[0]
            win_height = max_y + 10
            Btn_all_x = 5
            Btn_all_y = win_height
            Btn_ok_x = 5 + x_max[0] - 45
            Btn_ok_y = win_height
            win_height = win_height + 35
            BW_frame[0].place(x=5, y=5, width=x_max[0], height=y_max[0])
            ChildWin_bw.geometry(f"{win_width}x{win_height}")
        elif y_max[0] == 0:
            win_width = x_max[1]
            win_height = max_y + 10
            Btn_all_x = 5
            Btn_all_y = win_height
            Btn_ok_x = 5 + x_max[1] - 45
            Btn_ok_y = win_height
            win_height = win_height + 35
            BW_frame[1].place(x=5, y=5, width=x_max[1], height=y_max[1])
            ChildWin_bw.geometry(f"{win_width}x{win_height}")
        else:
            win_width = StartX + max_x + 5
            win_height = max_y + 10
            if y_max[0] > y_max[1]:
                Btn_all_x = x_start[1]
                Btn_all_y = win_height - 35
                Btn_ok_x = x_start[1] + x_max[1] - 45
                Btn_ok_y = win_height - 35
            elif y_max[0] < y_max[1]:
                Btn_all_x = 5
                Btn_all_y = win_height - 35
                Btn_ok_x = 5 + x_max[0] - 45
                Btn_ok_y = win_height - 35
            elif y_max[0] == y_max[1]:
                Btn_all_x = x_start[1]
                Btn_all_y = win_height
                Btn_ok_x = x_start[1] + x_max[1] - 45
                Btn_ok_y = win_height
                win_height = win_height + 35
            ChildWin_bw.geometry(f"{win_width}x{win_height}")
    elif v == 2 or v == 3:
        for key in Band_list:
            if Band_list[key]:
                BW = longest_value(Band_list[key])

        Btn_BW = [None] * len(BW)
        bw_var = ttkbst.IntVar()

        win_width = StartX + x_max[1] + 5
        win_height = max_y + 10

        if y_max[1] == 0:
            for counter, i in enumerate(BW):
                Btn_BW[counter] = ttkbst.Radiobutton(
                    ChildWin_bw,
                    text=i,
                    value=i,
                    variable=bw_var,
                    command=lambda: BW_check(bw_var.get(), Band_list, BW_Label, BW_list_var),
                )
                ps_x = (x_start[0] + x_max[0] - 50) - (50 * (len(BW) - 1 - counter))
                ps_y = y_max[0] + 10
                Btn_BW[counter].place(x=ps_x, y=ps_y, width=50, height=30)
            Btn_ok_x = 5 + x_max[0] - 45
            Btn_all_x = Btn_ok_x - 70
            Btn_clr_x = Btn_all_x - 85
            win_width = x_max[0] + 10
            win_height = y_max[0] + 80
            BW_frame[0].place(x=5, y=5, width=x_max[0], height=y_max[0])
        elif y_max[0] == 0:
            for counter, i in enumerate(BW):
                Btn_BW[counter] = ttkbst.Radiobutton(
                    ChildWin_bw,
                    text=i,
                    value=i,
                    variable=bw_var,
                    command=lambda: BW_check(bw_var.get(), Band_list, BW_Label, BW_list_var),
                )
                ps_x = (x_start[1] + x_max[1] - 55) - (50 * (len(BW) - 1 - counter))
                ps_y = y_max[1] + 10
                Btn_BW[counter].place(x=ps_x, y=ps_y, width=50, height=30)
            Btn_ok_x = 5 + x_max[1] - 45
            Btn_all_x = Btn_ok_x - 70
            Btn_clr_x = Btn_all_x - 85
            win_width = x_max[1] + 10
            win_height = y_max[1] + 80
            BW_frame[1].place(x=5, y=5, width=x_max[1], height=y_max[1])
        else:
            if y_max[0] > y_max[1]:
                for counter, i in enumerate(BW):
                    Btn_BW[counter] = ttkbst.Radiobutton(
                        ChildWin_bw,
                        text=i,
                        value=i,
                        variable=bw_var,
                        command=lambda: BW_check(bw_var.get(), Band_list, BW_Label, BW_list_var),
                    )
                    ps_x = (StartX + max_x - 50) - (50 * (len(BW) - 1 - counter))
                    if (y_max[0] - y_max[1] < 85) & (y_max[0] - y_max[1] > 45):
                        ps_y = y_max[1] + 10
                        win_height = max_y + 10
                    elif y_max[0] - y_max[1] < 85:
                        ps_y = y_max[1] + 10
                        win_height = max_y + 50
                    else:
                        ps_y = max_y - 65
                    Btn_BW[counter].place(x=ps_x, y=ps_y, width=50, height=30)
                Btn_ok_x = StartX + max_x - 45
                Btn_all_x = Btn_ok_x - 70
                Btn_clr_x = Btn_all_x - 85
            elif y_max[0] < y_max[1]:
                for counter, i in enumerate(BW):
                    Btn_BW[counter] = ttkbst.Radiobutton(
                        ChildWin_bw,
                        text=i,
                        value=i,
                        variable=bw_var,
                        command=lambda: BW_check(bw_var.get(), Band_list, BW_Label, BW_list_var),
                    )
                    ps_x = (StartX - 55) - (50 * (len(BW) - 1 - counter))
                    if (y_max[1] - y_max[0] < 85) & (y_max[1] - y_max[0] > 45):
                        ps_y = y_max[0] + 10
                        win_height = max_y + 10
                    elif y_max[1] - y_max[0] < 85:
                        ps_y = y_max[0] + 10
                        win_height = max_y + 50
                    else:
                        ps_y = max_y - 65
                    Btn_BW[counter].place(x=ps_x, y=ps_y, width=50, height=30)
                Btn_ok_x = StartX - 50
                Btn_all_x = Btn_ok_x - 70
                Btn_clr_x = Btn_all_x - 85
            elif y_max[0] == y_max[1]:
                for counter, i in enumerate(BW):
                    Btn_BW[counter] = ttkbst.Radiobutton(
                        ChildWin_bw,
                        text=i,
                        value=i,
                        variable=bw_var,
                        command=lambda: BW_check(bw_var.get(), Band_list, BW_Label, BW_list_var),
                    )
                    ps_x = (StartX + max_x - 50) - (50 * (len(BW) - 1 - counter))
                    ps_y = max_y + 10
                    Btn_BW[counter].place(x=ps_x, y=ps_y, width=50, height=30)
                Btn_ok_x = StartX + max_x - 45
                Btn_all_x = Btn_ok_x - 70
                Btn_clr_x = Btn_all_x - 85
                win_height = max_y + 85

        Btn_ok_y = ps_y + 35
        Btn_all_y = ps_y + 35
        Btn_clr_y = ps_y + 35
        Btn_clr = ttkbst.Button(ChildWin_bw, text="Clear", bootstyle="info")
        Btn_clr.place(x=Btn_clr_x, y=Btn_clr_y, width=60, height=30)
        Btn_clr.config(command=lambda: BW_clear(Band_list, BW_list_var))

        ChildWin_bw.geometry(f"{win_width}x{win_height}")

    Btn_all = ttkbst.Button(ChildWin_bw, text="All", bootstyle="info")
    Btn_all.place(x=Btn_all_x, y=Btn_all_y, width=45, height=30)
    Btn_all.config(command=lambda: [BW_check(0, Band_list, BW_Label, BW_list_var)])

    Btn_ok = ttkbst.Button(ChildWin_bw, text="OK", bootstyle="info")
    Btn_ok.place(x=Btn_ok_x, y=Btn_ok_y, width=45, height=30)
    Btn_ok.config(command=lambda: [BW_list.clear(), BW_list.update(BW_setting_ok(Band_list, BW_list_var))])

    scr_width = int(ChildWin_bw.winfo_screenwidth())
    scr_height = int(ChildWin_bw.winfo_screenheight())
    x = int((scr_width - win_width) / 2)
    y = int((scr_height - win_height) / 2)
    ChildWin_bw.geometry(f"{win_width}x{win_height}+{x}+{y}")
    ChildWin_bw.resizable(False, False)

    ChildWin_bw.bind(
        "<Return>", lambda event: [BW_list.clear(), BW_list.update(BW_setting_ok(Band_list, BW_list_var))]
    )
    ChildWin_bw.focus()

    return BW_list


def BW_check(bw_var, Band_list, BW_Label, BW_list_var):
    for key in Band_list:
        chk = []
        state = [None] * len(Band_list[key])
        for i, j in enumerate(Band_list[key]):
            state[i] = [None] * len(Band_list[key].get(j))

            for k, l in enumerate(Band_list[key].get(j)):
                state[i][k] = str(BW_Label[key][i][k].cget("state")).strip()  # normal or disabled
                if state[i][k] == "disabled":
                    chk.append(True)
                else:
                    chk.append(BW_list_var[key][i][k].get())  # True or False
        # DISABLED 이면 Skip 하도록 구현
        match bw_var:
            case 0:  # all button
                for m, n in enumerate(Band_list[key]):
                    for o, p in enumerate(Band_list[key].get(n)):
                        if state[m][o] == "disabled":
                            pass
                        else:
                            if all(chk):  # all() : None in list -> False, None in 2D list -> True
                                BW_list_var[key][m][o].set(False)
                            else:
                                BW_list_var[key][m][o].set(True)
            case 5:
                Specific_BW_selection(Band_list[key], 0, state, chk, BW_list_var[key])
            case 10:
                Specific_BW_selection(Band_list[key], 1, state, chk, BW_list_var[key])
            case 15:
                Specific_BW_selection(Band_list[key], 2, state, chk, BW_list_var[key])
            case 20:
                Specific_BW_selection(Band_list[key], 3, state, chk, BW_list_var[key])
            case 25:
                Specific_BW_selection(Band_list[key], 4, state, chk, BW_list_var[key])
            case 30:
                Specific_BW_selection(Band_list[key], 5, state, chk, BW_list_var[key])
            case 35:
                Specific_BW_selection(Band_list[key], 6, state, chk, BW_list_var[key])
            case 40:
                Specific_BW_selection(Band_list[key], 7, state, chk, BW_list_var[key])
            case 45:
                Specific_BW_selection(Band_list[key], 8, state, chk, BW_list_var[key])
            case 50:
                Specific_BW_selection(Band_list[key], 9, state, chk, BW_list_var[key])
            case 60:
                Specific_BW_selection(Band_list[key], 10, state, chk, BW_list_var[key])
            case 70:
                Specific_BW_selection(Band_list[key], 11, state, chk, BW_list_var[key])
            case 80:
                Specific_BW_selection(Band_list[key], 12, state, chk, BW_list_var[key])
            case 90:
                Specific_BW_selection(Band_list[key], 13, state, chk, BW_list_var[key])
            case 100:
                Specific_BW_selection(Band_list[key], 14, state, chk, BW_list_var[key])


def Specific_BW_selection(Band_list, BW_number, state, chk, BW_list_var):

    if all(chk):
        for m, n in enumerate(Band_list):
            for o, p in enumerate(Band_list.get(n)):
                BW_list_var[m][o].set(False)

    for m, n in enumerate(Band_list):
        try:
            if state[m][BW_number] == "disabled":
                pass
            else:
                BW_list_var[m][BW_number].set(True)
        except:
            # print(f"m={m}, n={n} list index out of range")
            pass


def BW_clear(Band_list, BW_list_var):
    for key in Band_list:
        for m, n in enumerate(Band_list[key]):
            for o, p in enumerate(Band_list[key].get(n)):
                BW_list_var[key][m][o].set(False)


def BW_setting_ok(Band_list, BW_list_var):
    Check_list = {}
    Checked_BW_list = {}

    for key in BW_list_var:
        bwlist = [None] * len(BW_list_var[key])
        for count, band in enumerate(BW_list_var[key]):
            bwlist[count] = []
            for bw in band:
                if bw == None:
                    bwlist[count].append(False)
                else:
                    bwlist[count].append(bw.get())
        Check_list[key] = {
            key: [value[i] for i in range(len(value)) if bwlist[counter][i]]
            for counter, (key, value) in enumerate(Band_list[key].items())
        }
        Checked_BW_list[key] = dict([(k, v) for k, v in Check_list[key].items() if v != []])

    ChildWin_bw.destroy()

    return Checked_BW_list
