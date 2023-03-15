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
            20: [5, 10, 15, 20],
            25: [5, 10, 15, 20, 25, 30, 35, 40, 45],
            26: [5, 10, 15, 20],
            28: [5, 10, 15, 20, 25, 30],
            66: [5, 10, 15, 20, 25, 30, 35, 40, 45],
            38: [5, 10, 15, 20, 25, 30, 35, 40],
            39: [5, 10, 15, 20, 25, 30, 35, 40],
            40: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80],
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
        fdd_1ch_list = {
            1: {5: [300], 10: [300], 15: [300], 20: [300]},
            2: {5: [900], 10: [900], 15: [900], 20: [900]},
            3: {5: [1575], 10: [1575], 15: [1575], 20: [1575]},
            4: {5: [2175], 10: [2175], 15: [2175], 20: [2175]},
            5: {5: [2525], 10: [2525], 15: [2525], 20: [2525]},
            7: {5: [3100], 10: [3100], 15: [3100], 20: [3100]},
            8: {5: [3625], 10: [3625], 15: [3625], 20: [3625]},
            12: {5: [5095], 10: [5095], 15: [5095], 20: [5095]},
            13: {5: [5230], 10: [5230], 15: [5230], 20: [5230]},
            17: {5: [5790], 10: [5790], 15: [5790], 20: [5790]},
            18: {5: [5925], 10: [5925], 15: [5925], 20: [5925]},
            19: {5: [6075], 10: [6075], 15: [6075], 20: [6075]},
            20: {5: [6300], 10: [6300], 15: [6300], 20: [6300]},
            25: {5: [8365], 10: [8365], 15: [8365], 20: [8365]},
            26: {5: [8865], 10: [8865], 15: [8865], 20: [8865]},
            28: {5: [9385], 10: [9410], 15: [9435], 20: [9460]},
            66: {5: [66786], 10: [66786], 15: [66786], 20: [66786]},
        }
        tdd_1ch_list = {
            38: {5: [38000], 10: [38000], 15: [38000], 20: [38000]},
            39: {5: [38450], 10: [38450], 15: [38450], 20: [38450]},
            40: {5: [39150], 10: [39150], 15: [39150], 20: [39150]},
            41: {5: [40620], 10: [40620], 15: [40620], 20: [40620]},
        }
        fdd_3ch_list = {
            1: {5: [25, 300, 575], 10: [50, 300, 550], 15: [75, 300, 525], 20: [100, 300, 500]},
            2: {5: [625, 900, 1175], 10: [650, 900, 1150], 15: [675, 900, 1125], 20: [700, 900, 1100]},
            3: {5: [1225, 1575, 1925], 10: [1250, 1575, 1900], 15: [1275, 1575, 1875], 20: [1300, 1575, 1850]},
            4: {5: [1975, 2175, 2375], 10: [2000, 2175, 2300], 15: [2025, 2175, 2325], 20: [2050, 2175, 2300]},
            5: {5: [2425, 2525, 2625], 10: [2450, 2525, 2600]},
            7: {5: [2775, 3100, 3425], 10: [2800, 3100, 3350], 15: [2825, 3100, 3375], 20: [2850, 3100, 3350]},
            8: {5: [3475, 3625, 3775], 10: [3500, 3625, 3750]},
            12: {5: [5035, 5095, 5155], 10: [5060, 5095, 5130]},
            13: {5: [5205, 5230, 5255], 10: [5230]},
            17: {5: [5755, 5790, 5825], 10: [5780, 5790, 5800]},
            18: {5: [5875, 5925, 5975], 10: [5900, 5925, 5950], 15: [5925]},
            19: {5: [6025, 6075, 6125], 10: [6050, 6075, 6100], 15: [6075]},
            20: {5: [6175, 6300, 6425], 10: [6200, 6300, 6400], 15: [6225, 6300, 6375], 20: [6250, 6300, 6350]},
            25: {5: [8065, 8365, 8665], 10: [8065, 8365, 8640], 15: [8115, 8365, 8615], 20: [8140, 8365, 8590]},
            26: {5: [8715, 8865, 9015], 10: [8750, 8865, 8990], 15: [8775, 8865, 8965]},
            28: {
                5: [9235, 9385, 9360, 9485, 9510, 9635],
                10: [9260, 9360, 9410, 9460, 9485, 9510, 9610],
                15: [9285, 9435, 9585],
                20: [9310, 9460, 9560],
            },
            66: {
                5: [66461, 66786, 67111],
                10: [66486, 66786, 67086],
                15: [66511, 66786, 67061],
                20: [66536, 66786, 67036],
            },
        }
        tdd_3ch_list = {
            38: {
                5: [37775, 38000, 38225],
                10: [37800, 38000, 38200],
                15: [37825, 38000, 38175],
                20: [37850, 38000, 38150],
            },
            39: {
                5: [38275, 38450, 38625],
                10: [38300, 38450, 38600],
                15: [38325, 38450, 38575],
                20: [38350, 38450, 38550],
            },
            40: {
                5: [38675, 39150, 39625],
                10: [38700, 39150, 39600],
                15: [38725, 39150, 39575],
                20: [38750, 39150, 39550],
            },
            41: {
                5: [39675, 40620, 41565],
                10: [39700, 40620, 41540],
                15: [39725, 40620, 41515],
                20: [39750, 40620, 41490],
            },
        }
        fdd_User = {
            1: {
                5: [x for x in range(25, 576, 1)],
                10: [x for x in range(50, 551, 1)],
                15: [x for x in range(75, 526, 1)],
                20: [x for x in range(100, 501, 1)],
            },
            2: {
                5: [x for x in range(625, 1176, 1)],
                10: [x for x in range(650, 1151, 1)],
                15: [x for x in range(675, 1126, 1)],
                20: [x for x in range(700, 1101, 1)],
            },
            3: {
                5: [x for x in range(1225, 1926, 1)],
                10: [x for x in range(1250, 1901, 1)],
                15: [x for x in range(1275, 1876, 1)],
                20: [x for x in range(1300, 1851, 1)],
            },
            4: {
                5: [x for x in range(1975, 2371, 1)],
                10: [x for x in range(2000, 2351, 1)],
                15: [x for x in range(2025, 2326, 1)],
                20: [x for x in range(2050, 2301, 1)],
            },
            5: {
                5: [x for x in range(2425, 2626, 1)],
                10: [x for x in range(2450, 2601, 1)],
            },
            7: {
                5: [x for x in range(2775, 3426, 1)],
                10: [x for x in range(2800, 3401, 1)],
                15: [x for x in range(2825, 3376, 1)],
                20: [x for x in range(2850, 3351, 1)],
            },
            8: {
                5: [x for x in range(3475, 3776, 1)],
                10: [x for x in range(3500, 3751, 1)],
            },
            12: {
                5: [x for x in range(5035, 5156, 1)],
                10: [x for x in range(5060, 5131, 1)],
            },
            13: {
                5: [x for x in range(5205, 5256, 1)],
                10: [x for x in range(5230, 5231, 1)],
            },
            17: {
                5: [x for x in range(5755, 5826, 1)],
                10: [x for x in range(5780, 5801, 1)],
            },
            18: {
                5: [x for x in range(5875, 5976, 1)],
                10: [x for x in range(5900, 5951, 1)],
                15: [x for x in range(5925, 5926, 1)],
            },
            19: {
                5: [x for x in range(6025, 6126, 1)],
                10: [x for x in range(6050, 6101, 1)],
                15: [x for x in range(6075, 6076, 1)],
            },
            20: {
                5: [x for x in range(6175, 6426, 1)],
                10: [x for x in range(6200, 6401, 1)],
                15: [x for x in range(6225, 6376, 1)],
                20: [x for x in range(6300, 6351, 1)],
            },
            25: {
                5: [x for x in range(8065, 8666, 1)],
                10: [x for x in range(8090, 8641, 1)],
                15: [x for x in range(8115, 8616, 1)],
                20: [x for x in range(8140, 8591, 1)],
            },
            26: {
                5: [x for x in range(8715, 9016, 1)],
                10: [x for x in range(8740, 8991, 1)],
                15: [x for x in range(8765, 8966, 1)],
            },
            28: {
                5: [x for x in range(9235, 9636, 1)],
                10: [x for x in range(9260, 9611, 1)],
                15: [x for x in range(9285, 9586, 1)],
                20: [x for x in range(9310, 9561, 1)],
            },
            66: {
                5: [x for x in range(66461, 67312, 1)],
                10: [x for x in range(66486, 67287, 1)],
                15: [x for x in range(66511, 67262, 1)],
                20: [x for x in range(66536, 67237, 1)],
            },
        }
        tdd_User = {
            38: {
                5: [x for x in range(37775, 38226, 1)],
                10: [x for x in range(37800, 38201, 1)],
                15: [x for x in range(37825, 38176, 1)],
                20: [x for x in range(37850, 38151, 1)],
            },
            39: {
                5: [x for x in range(38275, 38626, 1)],
                10: [x for x in range(38300, 38601, 1)],
                15: [x for x in range(38325, 38576, 1)],
                20: [x for x in range(38350, 38551, 1)],
            },
            40: {
                5: [x for x in range(38675, 39626, 1)],
                10: [x for x in range(38700, 39601, 1)],
                15: [x for x in range(38725, 39576, 1)],
                20: [x for x in range(38750, 39551, 1)],
            },
            41: {
                5: [x for x in range(39675, 41566, 1)],
                10: [x for x in range(39700, 41541, 1)],
                15: [x for x in range(39725, 41516, 1)],
                20: [x for x in range(39750, 41491, 1)],
            },
        }

        if N_of_Channel == 1:  # 1 CH
            Temp1 = [i for c, i in enumerate(B_list[0]) if Band_Select_Main_var[c].get() != True]
            B_list[0] = [x for x in B_list[0] if x not in Temp1]
            Temp2 = [i for c, i in enumerate(B_list[1]) if Band_Select_Sub_var[c].get() != True]
            B_list[1] = [x for x in B_list[1] if x not in Temp2]

            val = merge_dic(fdd_1ch_list, tdd_1ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in B_list[0] if k in val},
                1: {k: val[k] for k in B_list[1] if k in val},
            }
        elif N_of_Channel == 2:  # 3 CH
            Temp1 = [i for c, i in enumerate(B_list[0]) if Band_Select_Main_var[c].get() != True]
            B_list[0] = [x for x in B_list[0] if x not in Temp1]
            Temp2 = [i for c, i in enumerate(B_list[1]) if Band_Select_Sub_var[c].get() != True]
            B_list[1] = [x for x in B_list[1] if x not in Temp2]

            val = merge_dic(fdd_3ch_list, tdd_3ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in B_list[0] if k in val},
                1: {k: val[k] for k in B_list[1] if k in val},
            }
        elif N_of_Channel == 3:  # User Define
            Temp1 = int(User_defined_band[1:])
            channel = [int(x) for x in User_defined_ch.split(",")]

            if User_defined_path == "Main":
                path = 0
            elif User_defined_path == "Sub":
                path = 1

            val = merge_dic(fdd_User, tdd_User)
            matches = {k: v for k, v in val.items() if k == Temp1}
            if matches:
                (matched_key, matched_values) = list(matches.items())[0]
                Test_band_ch_list = {
                    path: {matched_key: {k: [i for i in channel if i in v] for k, v in matched_values.items()}}
                }

    elif Rat_option_var.get() == 3:  # NR
        Test_band_ch_list = {}
        fdd_1ch_list = {
            1: {
                5: [428000],
                10: [428000],
                15: [428000],
                20: [428000],
                25: [428000],
                30: [428000],
                40: [428000],
                45: [428000],
                50: [428000],
            },
            2: {
                5: [392000],
                10: [392000],
                15: [392000],
                20: [392000],
                25: [392000],
                30: [392000],
                40: [392000],
            },
            3: {
                5: [368500],
                10: [368500],
                15: [368500],
                20: [368500],
                25: [368500],
                30: [368500],
                40: [368500],
                45: [368500],
                50: [368500],
            },
            5: {5: [176300], 10: [176300], 15: [176300], 20: [176300], 25: [176300]},
            7: {
                5: [531000],
                10: [531000],
                15: [531000],
                20: [531000],
                25: [531000],
                50: [531000],
            },
            8: {5: [188500], 10: [188500], 15: [188500], 20: [188500], 35: [188500]},
            12: {5: [147500], 10: [147500], 15: [147500]},
            13: {5: [150200], 10: [150200]},
            20: {5: [161200], 10: [161200], 15: [161200], 20: [161200]},
            25: {
                5: [392500],
                10: [392500],
                15: [392500],
                20: [392500],
                25: [392500],
                30: [392500],
                40: [392500],
                45: [392500],
            },
            26: {5: [175300], 10: [175300], 15: [175300], 20: [175300]},
            28: {5: [156100], 10: [156100], 15: [156100], 20: [156100], 30: [156100]},
            66: {
                5: [429000],
                10: [429000],
                15: [429000],
                20: [429000],
                25: [429000],
                30: [429000],
                40: [429000],
                45: [429000],
            },
        }
        tdd_1ch_list = {
            38: {10: [519000], 15: [519000], 20: [519000], 25: [519000], 30: [519000], 40: [519000]},
            39: {
                10: [380000],
                15: [380000],
                20: [380000],
                25: [380000],
                30: [380000],
                40: [380000],
            },
            40: {
                10: [470000],
                15: [470000],
                20: [470000],
                25: [470000],
                30: [470000],
                40: [470000],
                50: [470000],
                60: [470000],
                80: [470000],
            },
            41: {
                10: [518598],
                15: [518598],
                20: [518598],
                30: [518598],
                40: [518598],
                50: [518598],
                60: [518598],
                70: [518598],
                80: [518598],
                90: [518598],
                100: [518598],
            },
            77: {
                10: [650000],
                15: [650000],
                20: [650000],
                25: [650000],
                30: [650000],
                40: [650000],
                50: [650000],
                60: [650000],
                70: [650000],
                80: [650000],
                90: [650000],
                100: [650000],
            },
            78: {
                10: [636666],
                15: [636666],
                20: [636666],
                25: [636666],
                30: [636666],
                40: [636666],
                50: [636666],
                60: [636666],
                70: [636666],
                80: [636666],
                90: [636666],
                100: [636666],
            },
        }
        fdd_3ch_list = {
            1: {
                5: [422500, 428000, 433500],
                10: [423000, 428000, 433000],
                15: [423500, 428000, 432500],
                20: [424000, 428000, 432000],
                25: [424500, 428000, 431500],
                30: [425000, 428000, 431000],
                40: [426000, 428000, 430000],
                45: [426500, 428000, 429500],
                50: [427000, 428000, 429000],
            },
            2: {
                5: [386500, 392000, 397500],
                10: [387000, 392000, 397000],
                15: [387500, 392000, 396500],
                20: [388000, 392000, 396000],
                25: [388500, 392000, 395500],
                30: [389000, 392000, 395000],
                40: [390000, 392000, 394000],
            },
            3: {
                5: [361500, 368500, 375500],
                10: [362000, 368500, 375000],
                15: [362500, 368500, 374500],
                20: [363000, 368500, 374000],
                25: [363500, 368500, 373500],
                30: [364000, 368500, 373000],
                35: [364500, 368500, 372500],
                40: [365000, 368500, 372000],
                45: [365500, 368500, 371500],
                50: [366000, 368500, 371000],
            },
            5: {
                5: [174300, 176300, 178300],
                10: [174800, 176300, 177800],
                15: [175300, 176300, 177300],
                20: [175800, 176300, 176800],
                25: [176300],
            },
            7: {
                5: [524500, 531000, 537500],
                10: [525000, 531000, 537000],
                15: [525500, 531000, 536500],
                20: [526000, 531000, 536000],
                25: [526500, 531000, 535500],
                50: [529000, 531000, 533000],
            },
            8: {
                5: [185500, 188500, 191500],
                10: [186000, 188500, 191000],
                15: [186500, 188500, 190500],
                20: [187000, 188500, 190000],
                35: [188500, 188500, 188500],
            },
            12: {
                5: [146300, 147500, 148700],
                10: [146800, 147500, 148200],
                15: [147300, 147500, 147700],
            },
            13: {
                5: [148800, 150200, 151600],
                10: [149300, 150200, 151100],
            },
            20: {
                5: [158700, 161200, 163700],
                10: [159200, 161200, 163200],
                15: [159700, 161200, 162700],
                20: [160200, 161200, 162200],
            },
            25: {
                5: [386500, 392500, 398500],
                10: [387000, 392500, 398000],
                15: [387500, 392500, 397500],
                20: [388000, 392500, 397000],
                25: [388500, 392500, 396500],
                30: [389000, 392500, 396000],
                40: [390000, 392500, 395000],
                45: [390500, 392500, 394500],
            },
            26: {
                5: [172300, 175300, 178300],
                10: [171900, 175300, 178700],
                15: [173300, 175300, 177300],
                20: [173800, 175300, 176800],
            },
            28: {
                5: [152100, 156100, 160100],
                10: [152600, 156100, 159600],
                15: [153100, 156100, 159100],
                20: [153600, 156600, 158600],
                30: [154600, 157600],
            },
            66: {
                5: [422500, 429000, 435500],
                10: [423000, 429000, 435000],
                15: [423500, 429000, 434500],
                20: [424000, 429000, 434000],
                25: [424500, 429000, 433500],
                30: [425000, 429000, 433000],
                40: [426000, 429000, 432000],
                45: [426500, 429000, 431500],
            },
        }
        tdd_3ch_list = {
            38: {
                10: [515000, 519000, 523000],
                15: [515500, 519000, 522500],
                20: [516000, 519000, 522000],
                25: [516500, 519000, 521500],
                30: [517000, 519000, 521000],
                40: [518000, 519000, 520000],
            },
            39: {
                10: [377000, 380000, 383000],
                15: [377500, 380000, 382500],
                20: [378000, 380000, 382000],
                25: [378500, 380000, 381500],
                30: [379000, 380000, 381000],
                40: [380000],
            },
            40: {
                10: [461000, 470000, 479000],
                15: [461500, 470000, 478500],
                20: [462000, 470000, 478000],
                25: [462500, 470000, 477500],
                30: [463000, 470000, 477000],
                40: [464000, 470000, 476000],
                50: [465000, 470000, 475000],
                60: [466000, 470000, 474000],
                80: [468000, 470000, 472000],
            },
            41: {
                10: [500202, 518598, 537000],
                15: [500700, 518598, 536496],
                20: [501204, 518598, 535998],
                30: [502200, 518598, 534996],
                40: [503202, 518598, 534000],
                50: [504204, 518598, 532998],
                60: [505200, 518598, 531996],
                70: [506202, 518598, 531000],
                80: [507204, 518598, 529998],
                90: [508200, 518598, 528996],
                100: [509202, 518598, 528000],
            },
            77: {
                10: [620334, 650000, 679666],
                15: [620500, 650000, 679500],
                20: [620668, 650000, 679332],
                25: [620834, 650000, 679166],
                30: [621000, 650000, 679000],
                40: [621334, 650000, 678666],
                50: [621668, 650000, 678332],
                60: [622000, 650000, 678000],
                70: [622334, 650000, 677666],
                80: [622668, 650000, 677332],
                90: [623000, 650000, 677000],
                100: [623334, 650000, 676666],
            },
            78: {
                10: [620334, 636666, 653000],
                15: [620500, 636666, 652832],
                20: [620668, 636666, 652666],
                25: [620834, 636666, 652500],
                30: [621000, 636666, 652332],
                40: [621334, 636666, 652000],
                50: [621668, 636666, 651666],
                60: [622000, 636666, 651332],
                70: [622334, 636666, 651000],
                80: [622668, 636666, 650666],
                90: [623000, 636666, 650332],
                100: [623334, 636666, 650000],
            },
        }
        fdd_User = {
            1: {
                5: [x for x in range(422500, 433501, 1)],
                10: [x for x in range(423000, 433001, 1)],
                15: [x for x in range(423500, 432501, 1)],
                20: [x for x in range(424000, 432001, 1)],
                25: [x for x in range(424500, 431501, 1)],
                30: [x for x in range(425000, 431001, 1)],
                40: [x for x in range(426000, 430001, 1)],
                45: [x for x in range(426500, 429501, 1)],
                50: [x for x in range(427000, 429001, 1)],
            },
            2: {
                5: [x for x in range(386500, 397501, 1)],
                10: [x for x in range(387000, 397001, 1)],
                15: [x for x in range(387500, 396501, 1)],
                20: [x for x in range(388000, 396001, 1)],
                25: [x for x in range(388500, 395501, 1)],
                30: [x for x in range(389000, 395001, 1)],
                40: [x for x in range(390000, 394001, 1)],
            },
            3: {
                5: [x for x in range(361500, 375501, 1)],
                10: [x for x in range(362000, 375001, 1)],
                15: [x for x in range(362500, 374501, 1)],
                20: [x for x in range(363000, 374001, 1)],
                25: [x for x in range(363500, 373501, 1)],
                30: [x for x in range(364000, 373001, 1)],
                35: [x for x in range(364500, 372501, 1)],
                40: [x for x in range(365000, 372001, 1)],
                45: [x for x in range(365500, 371501, 1)],
                50: [x for x in range(366000, 371001, 1)],
            },
            5: {
                5: [x for x in range(174300, 178301, 1)],
                10: [x for x in range(174800, 177801, 1)],
                15: [x for x in range(175300, 177301, 1)],
                20: [x for x in range(175800, 176801, 1)],
                25: [176300],
            },
            7: {
                5: [x for x in range(524500, 537500, 1)],
                10: [x for x in range(525000, 537001, 1)],
                15: [x for x in range(525500, 536501, 1)],
                20: [x for x in range(526000, 536001, 1)],
                25: [x for x in range(526500, 535501, 1)],
                50: [x for x in range(529000, 533001, 1)],
            },
            8: {
                5: [x for x in range(185500, 191501, 1)],
                10: [x for x in range(186000, 191001, 1)],
                15: [x for x in range(186500, 190501, 1)],
                20: [x for x in range(187000, 190001, 1)],
                35: [x for x in range(188500, 188501, 1)],
            },
            12: {
                5: [x for x in range(146300, 148701, 1)],
                10: [x for x in range(146800, 148201, 1)],
                15: [x for x in range(147300, 147701, 1)],
            },
            13: {
                5: [x for x in range(148800, 151601, 1)],
                10: [x for x in range(149300, 151101, 1)],
            },
            20: {
                5: [x for x in range(158700, 163701, 1)],
                10: [x for x in range(159200, 163201, 1)],
                15: [x for x in range(159700, 162701, 1)],
                20: [x for x in range(160200, 162201, 1)],
            },
            25: {
                5: [x for x in range(386500, 398501, 1)],
                10: [x for x in range(387000, 398001, 1)],
                15: [x for x in range(387500, 397501, 1)],
                20: [x for x in range(388000, 397001, 1)],
                25: [x for x in range(388500, 396501, 1)],
                30: [x for x in range(389000, 396001, 1)],
                40: [x for x in range(390000, 395001, 1)],
                45: [x for x in range(390500, 394501, 1)],
            },
            26: {
                5: [x for x in range(172300, 178301, 1)],
                10: [x for x in range(171900, 178701, 1)],
                15: [x for x in range(173300, 177301, 1)],
                20: [x for x in range(173800, 176801, 1)],
            },
            28: {
                5: [x for x in range(152100, 160101, 1)],
                10: [x for x in range(152600, 159601, 1)],
                15: [x for x in range(153100, 159101, 1)],
                20: [x for x in range(153600, 158601, 1)],
                30: [x for x in range(154600, 157601, 1)],
            },
            66: {
                5: [x for x in range(422500, 435501, 1)],
                10: [x for x in range(423000, 435001, 1)],
                15: [x for x in range(423500, 434501, 1)],
                20: [x for x in range(424000, 434001, 1)],
                25: [x for x in range(424500, 433501, 1)],
                30: [x for x in range(425000, 433001, 1)],
                40: [x for x in range(426000, 432001, 1)],
                45: [x for x in range(426500, 431501, 1)],
            },
        }
        tdd_User = {
            38: {
                10: [x for x in range(515000, 523001, 1)],
                15: [x for x in range(515500, 522501, 1)],
                20: [x for x in range(516000, 522001, 1)],
                25: [x for x in range(516500, 521501, 1)],
                30: [x for x in range(517000, 521001, 1)],
                40: [x for x in range(518000, 520001, 1)],
            },
            39: {
                10: [x for x in range(377000, 383001, 1)],
                15: [x for x in range(377500, 382501, 1)],
                20: [x for x in range(378000, 382001, 1)],
                25: [x for x in range(378500, 381501, 1)],
                30: [x for x in range(379000, 381001, 1)],
                40: [380000],
            },
            40: {
                10: [x for x in range(461000, 479001, 1)],
                15: [x for x in range(461500, 478501, 1)],
                20: [x for x in range(462000, 478001, 1)],
                25: [x for x in range(462500, 477501, 1)],
                30: [x for x in range(463000, 477001, 1)],
                40: [x for x in range(464000, 476001, 1)],
                50: [x for x in range(465000, 475001, 1)],
                60: [x for x in range(466000, 474001, 1)],
                80: [x for x in range(468000, 472001, 1)],
            },
            41: {
                10: [x for x in range(500202, 537001, 1)],
                15: [x for x in range(500700, 536497, 1)],
                20: [x for x in range(501204, 535999, 1)],
                30: [x for x in range(502200, 534997, 1)],
                40: [x for x in range(503202, 534001, 1)],
                50: [x for x in range(504204, 532999, 1)],
                60: [x for x in range(505200, 531997, 1)],
                70: [x for x in range(506202, 531001, 1)],
                80: [x for x in range(507204, 529999, 1)],
                90: [x for x in range(508200, 528997, 1)],
                100: [x for x in range(499200, 537998, 1)],
            },
            77: {
                10: [x for x in range(620334, 679667, 1)],
                15: [x for x in range(620500, 679501, 1)],
                20: [x for x in range(620668, 679333, 1)],
                25: [x for x in range(620834, 679167, 1)],
                30: [x for x in range(621000, 679001, 1)],
                40: [x for x in range(621334, 678667, 1)],
                50: [x for x in range(621668, 678333, 1)],
                60: [x for x in range(622000, 678001, 1)],
                70: [x for x in range(622334, 677667, 1)],
                80: [x for x in range(622668, 677333, 1)],
                90: [x for x in range(623000, 677001, 1)],
                100: [x for x in range(623334, 676667, 1)],
            },
            78: {
                10: [x for x in range(620334, 653000, 1)],
                15: [x for x in range(620500, 652832, 1)],
                20: [x for x in range(620668, 652666, 1)],
                25: [x for x in range(620834, 652500, 1)],
                30: [x for x in range(621000, 652332, 1)],
                40: [x for x in range(621334, 652000, 1)],
                50: [x for x in range(621668, 651666, 1)],
                60: [x for x in range(622000, 651332, 1)],
                70: [x for x in range(622334, 651000, 1)],
                80: [x for x in range(622668, 650666, 1)],
                90: [x for x in range(623000, 650332, 1)],
                100: [x for x in range(623334, 650001, 1)],
            },
        }
        N_of_Channel = Ch_option_var.get()

        if N_of_Channel == 1:  # 1 CH
            Temp1 = [i for c, i in enumerate(N_list[0]) if Band_Select_Main_var[c].get() != True]
            N_list[0] = [x for x in N_list[0] if x not in Temp1]

            Temp2 = [i for c, i in enumerate(N_list[1]) if Band_Select_Sub_var[c].get() != True]
            N_list[1] = [x for x in N_list[1] if x not in Temp2]

            val = merge_dic(fdd_1ch_list, tdd_1ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in N_list[0] if k in val},
                1: {k: val[k] for k in N_list[1] if k in val},
            }
        elif N_of_Channel == 2:  # 3 CH
            Temp1 = [i for c, i in enumerate(N_list[0]) if Band_Select_Main_var[c].get() != True]
            N_list[0] = [x for x in N_list[0] if x not in Temp1]

            Temp2 = [i for c, i in enumerate(N_list[1]) if Band_Select_Sub_var[c].get() != True]
            N_list[1] = [x for x in N_list[1] if x not in Temp2]

            val = merge_dic(fdd_3ch_list, tdd_3ch_list)
            Test_band_ch_list = {
                0: {k: val[k] for k in N_list[0] if k in val},
                1: {k: val[k] for k in N_list[1] if k in val},
            }
        elif N_of_Channel == 3:  # User Define
            Temp1 = int(User_defined_band[1:])
            User_defined_ch = [int(x) for x in User_defined_ch.split(",")]

            if User_defined_path == "Main":
                path = 0
            elif User_defined_path == "Sub":
                path = 1

            val = merge_dic(fdd_User, tdd_User)
            matches = {k: v for k, v in val.items() if k == Temp1}
            if matches:
                (matched_key, matched_values) = list(matches.items())[0]
                Test_band_ch_list = {
                    path: {matched_key: {k: [i for i in channel if i in v] for k, v in matched_values.items()}}
                }
    return Test_band_ch_list

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