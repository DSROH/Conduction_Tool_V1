import ttkbootstrap as ttkbst
import tkinter as tk


def merge_dic(x, y):
    z = x
    z.update(y)
    return z


def dict_compare_list(v, list_a):
    if v == 1:  # 3G
        Blist = {
            1: [5],
            2: [5],
            4: [5],
            5: [5],
            8: [5],
        }
        rat = "B"
    elif v == 2:  # LTE
        Blist = {
            1: [5, 10, 15, 20],
            2: [5, 10, 15, 20],
            3: [5, 10, 15, 20],
            4: [5, 10, 15, 20],
            5: [5, 10],
            7: [5, 10, 15, 20],
            8: [5, 10],
            12: [5, 10],
            13: [5, 10],
            17: [5, 10],
            18: [5, 10, 15],
            19: [5, 10, 15],
            20: [5, 10, 15, 20],
            25: [5, 10, 15, 20],
            26: [5, 10, 15],
            28: [5, 10, 15, 20],
            66: [5, 10, 15, 20],
            38: [5, 10, 15, 20],
            39: [5, 10, 15, 20],
            40: [5, 10, 15, 20],
            41: [5, 10, 15, 20],
        }
        rat = "B"
    elif v == 3:  # NR
        Blist = {
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

    keys_to_remove = [key for key in Blist.keys() if key not in list_a]
    for key in keys_to_remove:
        Blist.pop(key)

    return rat, Blist


def longest_value(dict_a):
    max_length = max(len(value) for value in dict_a.values())
    longest_values = [value for key, value in dict_a.items() if len(value) == max_length]
    if len(longest_values) == 1:
        return longest_values[0]
    else:
        values = list(dict_a.values())
        values.sort(key=len, reverse=True)
        return values[0]


def Check_testband(
    Rat_option_var,
    Ch_option_var,
    User_defined_path,
    User_defined_band,
    User_defined_ch,
    Band_Select_Main_var,
    Band_Select_Sub_var,
):
    W_list = {0: [1, 2, 4, 5, 8], 1: [1, 2, 4]}
    B_list = {
        0: [1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 66, 38, 39, 40, 41],
        1: [1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 66, 38, 39, 40, 41],
    }
    N_list = {
        0: [1, 2, 3, 5, 7, 8, 12, 13, 20, 25, 26, 28, 66, 38, 39, 40, 41, 77, 78],
        1: [1, 2, 3, 5, 7, 8, 12, 13, 20, 25, 26, 28, 66, 38, 39, 40, 41, 77, 78],
    }
    N_of_Channel = Ch_option_var.get()

    if Rat_option_var.get() == 1:  # 3G
        Test_band_ch_list = {}

        if N_of_Channel == 3:
            Temp1 = int(User_defined_band[1:])
            User_defined_ch = [int(x) for x in User_defined_ch.split(",")]

            if User_defined_path == "Main":
                path = 0
            elif User_defined_path == "Sub":
                path = 1
        else:
            Temp1 = [i for c, i in enumerate(W_list[0]) if Band_Select_Main_var[c].get() != True]
            W_list[0] = [x for x in W_list[0] if x not in Temp1]

            Temp2 = [i for c, i in enumerate(W_list[1]) if Band_Select_Sub_var[c].get() != True]
            W_list[1] = [x for x in W_list[1] if x not in Temp2]

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

        fdd_User = {
            1: [x for x in range(10562, 10839, 1)],
            2: [x for x in range(9662, 9939, 1)],
            4: [x for x in range(1537, 1739, 1)],
            5: [x for x in range(4357, 4459, 1)],
            8: [x for x in range(2937, 3089, 1)],
        }

        if N_of_Channel == 1:  # 1 CH
            Test_band_ch_list = {
                0: {k: fdd_1ch_list[k] for k in W_list[0] if k in fdd_1ch_list},
                1: {k: fdd_1ch_list[k] for k in W_list[1] if k in fdd_1ch_list},
            }
        elif N_of_Channel == 2:  # 3 CH
            Test_band_ch_list = {
                0: {k: fdd_3ch_list[k] for k in W_list[0] if k in fdd_3ch_list},
                1: {k: fdd_3ch_list[k] for k in W_list[1] if k in fdd_3ch_list},
            }
        elif N_of_Channel == 3:  # User Define
            matches = {k: v for k, v in fdd_User.items() if k == Temp1}
            if matches:
                (matched_key, matched_values) = list(matches.items())[0]
                Test_band_ch_list = {
                    path: {matched_key: [value for value in User_defined_ch if value in matched_values]},
                }

    elif Rat_option_var.get() == 2:  # LTE
        Test_band_ch_list = {}

        if N_of_Channel == 3:
            Temp1 = int(User_defined_band[1:])
            User_defined_ch = [int(x) for x in User_defined_ch.split(",")]

            if User_defined_path == "Main":
                path = 0
            elif User_defined_path == "Sub":
                path = 1
        else:
            Temp1 = [i for c, i in enumerate(B_list[0]) if Band_Select_Main_var[c].get() != True]
            B_list[0] = [x for x in B_list[0] if x not in Temp1]

            Temp2 = [i for c, i in enumerate(B_list[1]) if Band_Select_Sub_var[c].get() != True]
            B_list[1] = [x for x in B_list[1] if x not in Temp2]

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
        fdd_User = {
            1: [x for x in range(0, 600, 1)],
            2: [x for x in range(600, 1200, 1)],
            3: [x for x in range(1200, 1950, 1)],
            4: [x for x in range(1950, 2400, 1)],
            5: [x for x in range(2400, 2650, 1)],
            7: [x for x in range(2750, 3450, 1)],
            8: [x for x in range(2450, 3800, 1)],
            12: [x for x in range(5010, 5180, 1)],
            13: [x for x in range(5180, 5280, 1)],
            17: [x for x in range(5730, 5850, 1)],
            18: [x for x in range(5850, 6000, 1)],
            19: [x for x in range(6000, 6150, 1)],
            20: [x for x in range(6150, 6450, 1)],
            25: [x for x in range(8040, 8689, 1)],
            28: [x for x in range(9210, 9660, 1)],
            66: [x for x in range(66436, 67336, 1)],
        }
        tdd_User = {
            38: [x for x in range(37750, 38250, 1)],
            39: [x for x in range(38250, 38650, 1)],
            40: [x for x in range(38650, 39650, 1)],
            41: [x for x in range(39650, 41590, 1)],
        }
        if N_of_Channel == 1:  # 1 CH
            val = merge_dic(fdd_1ch_list, tdd_1ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in B_list[0] if k in val},
                1: {k: val[k] for k in B_list[1] if k in val},
            }
        elif N_of_Channel == 2:  # 3 CH
            val = merge_dic(fdd_3ch_list, tdd_3ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in B_list[0] if k in val},
                1: {k: val[k] for k in B_list[1] if k in val},
            }
        elif N_of_Channel == 3:  # User Define
            val = merge_dic(fdd_User, tdd_User)
            matches = {k: v for k, v in val.items() if k == Temp1}
            if matches:
                (matched_key, matched_values) = list(matches.items())[0]
                Test_band_ch_list = {
                    path: {matched_key: [value for value in User_defined_ch if value in matched_values]},
                }
    elif Rat_option_var.get() == 3:  # NR
        Test_band_ch_list = {}

        if N_of_Channel == 3:
            Temp1 = int(User_defined_band[1:])
            User_defined_ch = [int(x) for x in User_defined_ch.split(",")]

            if User_defined_path == "Main":
                path = 0
            elif User_defined_path == "Sub":
                path = 1
        else:
            Temp1 = [i for c, i in enumerate(N_list[0]) if Band_Select_Main_var[c].get() != True]
            N_list[0] = [x for x in N_list[0] if x not in Temp1]

            Temp2 = [i for c, i in enumerate(N_list[1]) if Band_Select_Sub_var[c].get() != True]
            N_list[1] = [x for x in N_list[1] if x not in Temp2]

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
        fdd_User = {
            1: [x for x in range(422000, 434001, 1)],
            2: [x for x in range(386000, 398001, 1)],
            3: [x for x in range(361000, 376001, 1)],
            5: [x for x in range(173800, 178801, 1)],
            7: [x for x in range(524000, 538001, 1)],
            8: [x for x in range(185000, 192001, 1)],
            12: [x for x in range(145800, 149201, 1)],
            13: [x for x in range(149200, 151201, 1)],
            18: [x for x in range(172000, 175001, 1)],
            20: [x for x in range(158200, 164201, 1)],
            25: [x for x in range(386000, 399001, 1)],
            28: [x for x in range(151600, 160601, 1)],
            66: [x for x in range(422000, 440001, 1)],
        }
        tdd_User = {
            38: [x for x in range(514000, 524001, 1)],
            39: [x for x in range(376000, 384001, 1)],
            40: [x for x in range(460000, 480001, 1)],
            41: [x for x in range(499200, 537997, 1)],
        }
        N_of_Channel = Ch_option_var.get()

        if N_of_Channel == 1:  # 1 CH
            val = merge_dic(fdd_1ch_list, tdd_1ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in N_list[0] if k in val},
                1: {k: val[k] for k in N_list[1] if k in val},
            }
            key = dict.fromkeys(Test_band_ch_list)
        elif N_of_Channel == 2:  # 3 CH
            val = merge_dic(fdd_3ch_list, tdd_3ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in N_list[0] if k in val},
                1: {k: val[k] for k in N_list[1] if k in val},
            }
            key = dict.fromkeys(Test_band_ch_list)
        elif N_of_Channel == 3:  # User Define
            val = merge_dic(fdd_User, tdd_User)
            matches = {k: v for k, v in val.items() if k == Temp1}
            if matches:
                (matched_key, matched_values) = list(matches.items())[0]
                Test_band_ch_list = {
                    path: {matched_key: [value for value in User_defined_ch if value in matched_values]},
                }

    return Test_band_ch_list


def Selectall_band(Rat_option_var, TX_path, Band_Select_var):
    chk = []

    for c, i in enumerate(Band_Select_var):
        if (Rat_option_var.get() == 2) & (TX_path == "Sub") & (c in [4, 6, 7, 8, 9, 10, 11, 12, 14]):
            pass
        elif (Rat_option_var.get() == 3) & (TX_path == "Sub") & (c in [3, 5, 6, 7, 8, 10, 14]):
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
            elif (Rat_option_var.get() == 3) & (TX_path == "Sub") & (count in [3, 5, 6, 7, 8, 10, 14]):
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
            Select_list = [13, 14, 15, 16, 17, 18]
        elif TX_path == "Sub":
            Select_list = [13, 15, 16, 17, 18]

        for c, i in enumerate(Band_Select_var):
            if c in Select_list:
                Band_Select_var[c].set(True)
            else:
                Band_Select_var[c].set(False)


def Num_RB(rat, band, BW):
    if rat == "LTE":
        match BW:
            case 5:
                NRB = 25
                outfull_offset = 0
                PRB = 8
                infull_offset = 0
            case 10:
                NRB = 50
                outfull_offset = 0
                PRB = 12
                infull_offset = 0
            case 15:
                NRB = 75
                outfull_offset = 0
                PRB = 16
                infull_offset = 0
            case 20:
                NRB = 100
                outfull_offset = 0
                PRB = 18
                infull_offset = 0

    elif rat == "NR":
        if band in [38, 39, 40, 41, 77, 78]:
            match BW:
                case 5:
                    NRB = 25
                    outfull_offset = 0
                    PRB = 5
                    infull_offset = 2
                case 10:
                    NRB = 24
                    outfull_offset = 0
                    PRB = 12
                    infull_offset = 6
                case 15:
                    NRB = 36
                    outfull_offset = 0
                    PRB = 18
                    infull_offset = 9
                case 20:
                    NRB = 50
                    outfull_offset = 0
                    PRB = 25
                    infull_offset = 12
                case 25:
                    NRB = 64
                    outfull_offset = 0
                    PRB = 32
                    infull_offset = 16
                case 30:
                    NRB = 75
                    outfull_offset = 0
                    PRB = 36
                    infull_offset = 18
                case 40:
                    NRB = 100
                    outfull_offset = 0
                    PRB = 50
                    infull_offset = 25
                case 50:
                    NRB = 128
                    outfull_offset = 0
                    PRB = 64
                    infull_offset = 32
                case 60:
                    NRB = 162
                    outfull_offset = 0
                    PRB = 81
                    infull_offset = 40
                case 70:
                    NRB = 180
                    outfull_offset = 0
                    PRB = 90
                    infull_offset = 45
                case 80:
                    NRB = 216
                    outfull_offset = 0
                    PRB = 108
                    infull_offset = 54
                case 90:
                    NRB = 243
                    outfull_offset = 0
                    PRB = 120
                    infull_offset = 60
                case 100:
                    NRB = 270
                    outfull_offset = 0
                    PRB = 135
                    infull_offset = 67
        else:
            match BW:
                case 5:
                    NRB = 25
                    outfull_offset = 0
                    PRB = 12
                    infull_offset = 6
                case 10:
                    NRB = 50
                    outfull_offset = 0
                    PRB = 25
                    infull_offset = 12
                case 15:
                    NRB = 75
                    outfull_offset = 0
                    PRB = 36
                    infull_offset = 18
                case 20:
                    NRB = 100
                    outfull_offset = 0
                    PRB = 50
                    infull_offset = 25
                case 25:
                    NRB = 128
                    outfull_offset = 0
                    PRB = 64
                    infull_offset = 32
                case 30:
                    NRB = 160
                    outfull_offset = 0
                    PRB = 80
                    infull_offset = 40
                case 40:
                    NRB = 216
                    outfull_offset = 0
                    PRB = 108
                    infull_offset = 54
                case 50:
                    NRB = 270
                    outfull_offset = 0
                    PRB = 135
                    infull_offset = 67

    return NRB, outfull_offset, PRB, infull_offset


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


def Check_pwr_lvs(variable):

    pwr_levels = []

    if variable == 1:
        pwr_levels = [23, 20, 15, 10, 5, 0]

    elif variable == 2:
        for i in range(23, -1, -3):
            pwr_levels.append(i)

    elif variable == 3:
        for i in range(23, -1, -1):
            pwr_levels.append(i)
    elif variable == 4:
        for i in range(23, -11, -1):
            pwr_levels.append(i)
    elif variable == 5:
        for i in range(23, -46, -1):
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
                        if (i in [38, 39, 40, 41]) & (k == 5):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [7, 40]) & (k == 45):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [8]) & (k in [25, 30]):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [1, 66, 38, 39, 40]) & (k == 35):
                            BW_Label[key][count][c].config(state=tk.DISABLED)
                            BW_list_var[key][count][c].set(False)
                        elif (i in [77, 78]) & (k in [5, 35, 45]):
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
