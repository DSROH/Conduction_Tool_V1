import ttkbootstrap as ttkbst
import tkinter as tk


def merge_dic(x, y):
    z = x
    z.update(y)
    return z


def Check_bandlist(Rat_option_var, Ch_option_var, User_defined_band, User_defined_ch, Chbox_var, BWbox_var):
    W_list = [1, 2, 4, 5, 8]
    B_list = [1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 66, 38, 39, 40, 41]
    N_list = [1, 2, 3, 5, 7, 8, 12, 13, 20, 25, 26, 28, 66, 38, 39, 40, 41, 77, 78]

    if Rat_option_var.get() == 1:  # 3G
        Wlist = []
        band_list = {}

        for c, i in enumerate(W_list):
            if Chbox_var[c].get() == True:
                Wlist.append(i)
        key = dict.fromkeys(Wlist)

        fdd_1ch_list = {
            1: [10700],
            2: [9800],
            4: [1638],
            5: [4408],
            8: [3013],
        }

        fdd_3ch_list = {
            1: [10562, 10700, 10838],
            2: [9662, 9800, 9938],
            4: [1537, 1638, 1738],
            5: [4357, 4408, 4458],
            8: [2937, 3013, 3088],
        }

        N_of_Channel = Ch_option_var.get()

        if N_of_Channel == 1:  # 1 CH
            val = merge_dic(fdd_1ch_list, tdd_1ch_list)
        elif N_of_Channel == 2:  # 3 CH
            val = merge_dic(fdd_3ch_list, tdd_3ch_list)
        elif N_of_Channel == 3:  # User Define
            new_char = [int(x.strip()) for x in User_defined_ch.split(",")]
            key = [int(s) for s in key]
            val = dict.fromkeys(key, new_char)

        for k in key:
            if k in val.keys():
                band_list[k] = val[k]

    elif Rat_option_var.get() == 2:  # LTE
        Blist = []
        band_list = {}
        N_of_Channel = Ch_option_var.get()

        if N_of_Channel == 3:
            key = User_defined_band[1:]
        else:
            for c, i in enumerate(B_list):
                if Chbox_var[c].get() == True:
                    Blist.append(i)
            key = dict.fromkeys(Blist)

        fdd_1ch_list = {
            1: [300],
            2: [900],
            3: [1575],
            4: [2175],
            5: [2525],
            7: [3100],
            8: [3625],
            12: [5095],
            13: [5230],
            17: [5790],
            18: [5925],
            19: [6075],
            20: [6300],
            25: [8365],
            26: [8865],
            28: [9610],
            66: [66886],
        }
        tdd_1ch_list = {38: [38000], 39: [38450], 40: [39150], 41: [40620]}

        fdd_3ch_list = {
            1: [50, 300, 550],
            2: [650, 900, 1150],
            3: [1250, 1575, 1900],
            4: [2000, 2175, 2300],
            5: [2450, 2525, 2600],
            7: [2800, 3100, 3350],
            8: [3500, 3625, 3750],
            12: [5060, 5095, 5130],
            13: [5230],
            17: [5780, 5790, 5800],
            18: [5900, 5925, 5950],
            19: [6050, 6075, 6100],
            20: [6200, 6300, 6400],
            25: [8065, 8365, 8665],
            26: [8750, 8865, 8990],
            28: [9410, 9510, 9610, 9260, 9360, 9460],
            66: [66486, 66786, 67085],
        }
        tdd_3ch_list = {
            38: [37800, 38000, 38200],
            39: [38300, 38450, 38600],
            40: [38700, 39150, 39600],
            41: [39700, 40620, 41540],
        }

        if N_of_Channel == 1:  # 1 CH
            val = merge_dic(fdd_1ch_list, tdd_1ch_list)
        elif N_of_Channel == 2:  # 3 CH
            val = merge_dic(fdd_3ch_list, tdd_3ch_list)
        elif N_of_Channel == 3:  # User Define
            new_char = [int(x.strip()) for x in User_defined_ch.split(",")]
            key = [int(s) for s in key]
            val = dict.fromkeys(key, new_char)

        for k in key:
            if k in val.keys():
                band_list[k] = val[k]

    elif Rat_option_var.get() == 3:  # NR
        Nlist = []
        band_list = {}

        for c, i in enumerate(N_list):
            if BWbox_var[c].get() == True:
                Nlist.append(i)
        key = dict.fromkeys(Nlist)

        fdd_1ch_list = {
            1: [428000],
            2: [392000],
            3: [368500],
            5: [176300],
            7: [531000],
            8: [188500],
            12: [147500],
            13: [150200],
            20: [161200],
            25: [392500],
            26: [175300],
            28: [156100],
            66: [429000],
        }
        tdd_1ch_list = {
            38: [519000],
            39: [380000],
            40: [470000],
            41: [518598],
            77: [650000],
            78: [636667],
        }

        fdd_3ch_list = {
            1: [423000, 428000, 433000],
            2: [387000, 392000, 397000],
            3: [362000, 368500, 375000],
            5: [174800, 176300, 177800],
            7: [525000, 531000, 537000],
            8: [186000, 188500, 191000],
            12: [146800, 147500, 148200],
            13: [149300, 150200, 151100],
            20: [159200, 161200, 163200],
            25: [387000, 392500, 398000],
            26: [171900, 175300, 178700],
            28: [152600, 156100, 159600],
            66: [423000, 429000, 435000],
        }
        tdd_3ch_list = {
            38: [515000, 519000, 523000],
            39: [377000, 380000, 383000],
            40: [461000, 470000, 479000],
            41: [500202, 518598, 537000],
            77: [620334, 650000, 679666],
            78: [620334, 636667, 653000],
        }

        N_of_Channel = Ch_option_var.get()

        if N_of_Channel == 1:  # 1 CH
            val = merge_dic(fdd_1ch_list, tdd_1ch_list)
        elif N_of_Channel == 2:  # 3 CH
            val = merge_dic(fdd_3ch_list, tdd_3ch_list)
        elif N_of_Channel == 3:  # User Define
            new_char = [int(x.strip()) for x in User_defined_ch.split(",")]
            key = [int(s) for s in key]
            val = dict.fromkeys(key, new_char)

        for k in key:
            if k in val.keys():
                band_list[k] = val[k]

    return band_list


def Selectall_band(BWbox_var):
    chk = []
    for c, i in enumerate(BWbox_var):
        chk.append(BWbox_var[c].get())

    if all(chk):
        # 한개라도 체크되있다면, 전체 체크 해제
        for count, j in enumerate(BWbox_var):
            BWbox_var[count].set(False)
    else:
        for count, j in enumerate(BWbox_var):
            BWbox_var[count].set(True)


def Selectfdd_band(Rat_option_var, BWbox_var):
    if Rat_option_var.get() == 2:  # LTE
        Select_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        for c, i in enumerate(BWbox_var):
            # BWbox_var[c].set(not BWbox_var[c].get())
            if c in Select_list:
                BWbox_var[c].set(True)
            else:
                BWbox_var[c].set(False)
    elif Rat_option_var.get() == 3:  # NR
        Select_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for c, i in enumerate(BWbox_var):
            # BWbox_var[c].set(not BWbox_var[c].get())
            if c in Select_list:
                BWbox_var[c].set(True)
            else:
                BWbox_var[c].set(False)


def Selecttdd_band(Rat_option_var, BWbox_var):
    if Rat_option_var.get() == 2:  # LTE
        Select_list = [17, 18, 19, 20]
        for c, i in enumerate(BWbox_var):
            if c in Select_list:
                BWbox_var[c].set(True)
            else:
                BWbox_var[c].set(False)
    elif Rat_option_var.get() == 3:  # NR
        Select_list = [13, 14, 15, 16, 17, 18]
        for c, i in enumerate(BWbox_var):
            if c in Select_list:
                BWbox_var[c].set(True)
            else:
                BWbox_var[c].set(False)


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


def Check_pwr_lvs(Pw_option_var):

    pwr_levels = []

    if Pw_option_var.get() == 1:
        pwr_levels = [23, 20, 15, 10, 5, 0]

    elif Pw_option_var.get() == 2:

        for i in range(23, -1, -1):
            pwr_levels.append(i)

    elif Pw_option_var.get() == 3:

        for i in range(23, -11, -1):
            pwr_levels.append(i)

    return pwr_levels


def BW_setting(v):

    global ChildWin_bw
    global Band_list_var
    global BW_list_var
    global BW_Label

    if v == 1:  # 3G
        Band_list = {
            1: [5],
            2: [5],
            4: [5],
            5: [5],
            8: [5],
        }
        rat = "B"

    elif v == 2:  # LTE
        Band_list = {
            1: [5, 10, 15, 20],
            2: [5, 10, 15, 20],
            3: [5, 10, 15, 20],
            4: [5, 10, 15, 20],
            5: [5, 10, 15, 20],
            7: [5, 10, 15, 20],
            8: [5, 10, 15, 20],
            12: [5, 10, 15, 20],
            13: [5, 10, 15, 20],
            17: [5, 10, 15, 20],
            18: [5, 10, 15, 20],
            19: [5, 10, 15, 20],
            20: [5, 10, 15, 20],
            25: [5, 10, 15, 20],
            26: [5, 10, 15, 20],
            28: [5, 10, 15, 20],
            66: [5, 10, 15, 20],
            38: [5, 10, 15, 20],
            39: [5, 10, 15, 20],
            40: [5, 10, 15, 20],
            41: [5, 10, 15, 20],
        }
        rat = "B"

    elif v == 3:  # NR
        Band_list = {
            1: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            2: [5, 10, 15, 20, 25, 30, 35, 40],
            3: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            5: [5, 10, 15, 20, 25],
            7: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            8: [5, 10, 15, 20, 25, 30, 35],
            12: [5, 10, 15],
            13: [5, 10],
            18: [5, 10, 15],
            20: [5, 10, 15, 20],
            25: [5, 10, 15, 20, 25, 30, 35, 40, 45],
            26: [5, 10, 15, 20, 25, 30],
            28: [5, 10, 15, 20, 25, 30],
            66: [5, 10, 15, 20, 25, 30, 35, 40, 45],
            38: [5, 10, 15, 20, 25, 30, 35, 40],
            39: [5, 10, 15, 20, 25, 30, 35, 40],
            40: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
            41: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
            77: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
            78: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
        }
        rat = "n"

    try:
        ChildWin_bw.destroy()
    except:
        pass

    ChildWin_bw = ttkbst.Toplevel(title="Bandwidth Setting")
    ChildWin_bw.attributes("-topmost", True)

    Band_list_var = [None] * len(Band_list)
    BW_list_var = [None] * len(Band_list)
    BW_Label = [None] * len(Band_list)

    geom_max_x = []
    geom_max_y = []
    for count, i in enumerate(Band_list):
        pos_x1 = 10
        pos_y1 = 5 + 35 * count
        Band_list_var[count] = ttkbst.Label(ChildWin_bw, text=f"{rat}{i}")
        Band_list_var[count].place(x=pos_x1, y=pos_y1, width=50, height=30)

        BW_list_var[count] = [None] * len(Band_list.get(i))
        BW_Label[count] = [None] * len(Band_list.get(i))
        # print(f"Band_list.get(i) = {Band_list.get(i)}, count = {len(Band_list.get(i))}")

        for c, k in enumerate(Band_list.get(i)):
            BW_list_var[count][c] = ttkbst.BooleanVar()
            pos_x2 = 50 + 50 * c
            BW_Label[count][c] = ttkbst.Checkbutton(ChildWin_bw, text=f"{k}", variable=BW_list_var[count][c])
            BW_Label[count][c].place(x=pos_x2, y=pos_y1, width=50, height=30)
            BW_list_var[count][c].set(True)
            geom_max_x.append(pos_x2)
            geom_max_y.append(pos_y1)

            if v == 3:
                if (i in [38, 39, 40, 41]) & (k == 5):
                    BW_Label[count][c].config(state=tk.DISABLED)
                    BW_list_var[count][c].set(False)
                elif (i in [7, 40]) & (k == 45):
                    BW_Label[count][c].config(state=tk.DISABLED)
                    BW_list_var[count][c].set(False)
                elif (i in [8]) & (k in [25, 30]):
                    BW_Label[count][c].config(state=tk.DISABLED)
                    BW_list_var[count][c].set(False)
                elif (i in [1, 66, 38, 39, 40]) & (k == 35):
                    BW_Label[count][c].config(state=tk.DISABLED)
                    BW_list_var[count][c].set(False)
                elif (i in [77, 78]) & (k in [5, 35, 45]):
                    BW_Label[count][c].config(state=tk.DISABLED)
                    BW_list_var[count][c].set(False)

    ChildWin_bw.geometry(f"{max(geom_max_x)+50}x{max(geom_max_y)+110}")

    if v == 2:
        Btn_BW = [None, None, None, None]
        bw_var = ttkbst.IntVar()
        for counter, i in enumerate(range(5, 21, 5)):
            Btn_BW[counter] = ttkbst.Radiobutton(
                ChildWin_bw,
                text=i,
                value=i,
                variable=bw_var,
                command=lambda: BW_check(bw_var.get(), Band_list, BW_Label, BW_list_var),
            )
            ps_x = pos_x2 - 50 * (3 - counter)
            ps_y = pos_y1 + 35
            Btn_BW[counter].place(x=ps_x, y=ps_y, width=50, height=30)

    Btn_all = ttkbst.Button(ChildWin_bw, text="All", bootstyle="info")
    Btn_all.place(x=max(geom_max_x) - 50, y=max(geom_max_y) + 70, width=40, height=30)
    Btn_all.config(command=lambda: BW_check(0, Band_list, BW_Label, BW_list_var))

    Btn_ok = ttkbst.Button(ChildWin_bw, text="OK", bootstyle="info")
    Btn_ok.place(x=max(geom_max_x), y=max(geom_max_y) + 70, width=40, height=30)
    Btn_ok.config(command=lambda: BW_setting_ok(Band_list, BW_list_var))


def BW_check(bw_var, Band_list, BW_Label, BW_list_var):
    chk = []
    state = [None] * len(Band_list)
    for i, j in enumerate(Band_list):
        state[i] = [None] * len(Band_list.get(j))

        for k, l in enumerate(Band_list.get(j)):
            state[i][k] = str(BW_Label[i][k].cget("state")).strip()  # normal or disabled
            if state[i][k] == "disabled":
                chk.append(True)
            else:
                chk.append(BW_list_var[i][k].get())  # True or False
    # DISABLED 이면 Skip 하도록 구현
    for m, n in enumerate(Band_list):
        for o, p in enumerate(Band_list.get(n)):
            match bw_var:
                case 0:  # all button
                    if state[m][o] == "disabled":
                        pass
                    else:
                        if all(chk):  # all() : None in list -> False, None in 2D list -> True
                            BW_list_var[m][o].set(False)
                        else:
                            BW_list_var[m][o].set(True)
                case 5:
                    BW_list_var[m][o].set(False)
                    BW_list_var[m][0].set(True)
                case 10:
                    BW_list_var[m][o].set(False)
                    BW_list_var[m][1].set(True)
                case 15:
                    BW_list_var[m][o].set(False)
                    BW_list_var[m][2].set(True)
                case 20:
                    BW_list_var[m][o].set(False)
                    BW_list_var[m][3].set(True)


def BW_setting_ok(Band_list, BW_list_var):
    bwlist = [None] * len(BW_list_var)
    for count, band in enumerate(BW_list_var):
        bwlist[count] = []
        for bw in band:
            if bw == None:
                bwlist[count].append(False)
            else:
                bwlist[count].append(bw.get())
    BW_list = {
        key: [value[i] for i in range(len(value)) if bwlist[counter][i]]
        for counter, (key, value) in enumerate(Band_list.items())
    }
    ChildWin_bw.destroy()

    return BW_list