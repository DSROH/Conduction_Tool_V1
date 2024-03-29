import time
import tkinter as tk
from datetime import datetime

import pandas as pd

import Function as func
from Band_list import NR_channel_converter, Num_RB, channel_converter

pd.options.display.float_format = "{:.5f}".format


def Set_factolog(dut, text_area):
    response = dut.at_write("AT+MODECHAN=0,2")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    response = dut.at_write("AT+DISPTEST=0,3")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    response = dut.at_write("AT+FACTOLOG=0,2,1,2")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    response = dut.at_write("AT+AIRPMODE=0,0,0,1")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    time.sleep(1)
    response = dut.at_write("AT+AIRPMODE=0,0,0,0")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    # response = dut.at_write("AT+NFCMTEST=0,0")
    # text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    # text_area.see(tk.END)
    # response = dut.at_write("AT+FACMTEST=0,0,1,86400_10")
    # text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    # text_area.see(tk.END)
    # response = dut.at_write("AT+FACMTEST=0,0,2,86400_10")
    # text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    # text_area.see(tk.END)
    response = dut.at_write("AT+DISPTEST=0,4")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    response = dut.at_write("AT+MODECHAN=0,0")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n\n")
    text_area.see(tk.END)


def End_testmode(dut, text_area):
    response = dut.at_write("AT+LRFFINALFINISH")
    # text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    # text_area.see(tk.END)


def LTE_tx_measure(
    dut,
    Equip,
    Callbox,
    E3632a_1,
    E3632a_2,
    path,
    band,
    channel,
    bandwidth,
    pwr_levels,
    canvas,
    fig,
    ax1,
    ax2,
    ax3,
    save_dir,
    text_area,
):

    rxfreq, txfreq = channel_converter(band, channel)
    list_Power = []
    Power_delta = []
    list_Pa_current = []
    list_ACLR_L = []
    list_ACLR_R = []

    if path == "Main":
        path_number = 0
    elif path == "Sub":
        path_number = 1

    text_area.insert(tk.END, "\n")
    text_area.insert(tk.END, "*" * 45)
    text_area.insert(tk.END, f" LTE B{band:<2} {path} {channel:>5}CH {bandwidth}MHz ")
    text_area.insert(tk.END, "*" * 44)
    text_area.insert(tk.END, "\n")
    response = dut.at_write("AT+HNSSTOP")
    response = dut.at_write(f"AT+LRFFINALSTART=1,{band}")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    response = dut.at_write("AT+LMODETEST")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    NRB, outfull_offset, PRB, infull_offsets = Num_RB("LTE", band, bandwidth)
    BW_number = func.define_BW_number("LTE", bandwidth)
    func.Nonsig_lte_tx_measure_setting(
        dut, Callbox, Equip, path_number, band, bandwidth, BW_number, NRB, PRB, rxfreq, txfreq, text_area
    )

    text_area.insert(tk.END, "-" * 116)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)
    text_area.insert(
        tk.END,
        f"   TARGET  |   POWER   |   UTRA2   |   UTRA1   |  E-UTRA1  |  E-UTRA1  |   UTRA1   |   UTRA2   |"
        f"   P.AMP  |  SYSTEM  \n",
    )
    text_area.see(tk.END)
    text_area.insert(tk.END, "-" * 116)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)

    columns = [
        "TX POWER",
        "UTRA ACLR2-",
        "UTRA ACLR1-",
        "EUTRA ACLR-",
        "EUTRA ACLR+",
        "UTRA ACLR1+",
        "UTRA ACLR2+",
        "PA",
        "SYSTEM",
    ]
    tx_result = pd.DataFrame("", index=pwr_levels, columns=columns)
    tx_result.columns.name = "Target"

    for pwr in pwr_levels:
        if pwr == 23:  # 23dBm 12RB Setting
            Callbox.write("CONFigure:LTE:MEAS:MEValuation:RBALlocation:AUTO OFF")
            response = dut.at_write(f"AT+LTXSENDREQ={path_number},{BW_number},{txfreq},{PRB},0,0,2,1,{pwr}")
            # response = dut.at_write(f"AT+LTXPWRLVLSET={pwr}")
            # response = dut.at_write("AT+LTXCHNSDREQ")
        else:
            response = dut.at_write(f"AT+LTXSENDREQ={path_number},{BW_number},{txfreq},{NRB},0,0,2,1,{pwr}")
            # response = dut.at_write(f"AT+LTXPWRLVLSET={pwr}")
            # response = dut.at_write("AT+LTXCHNSDREQ")
            Callbox.write("CONFigure:LTE:MEAS:MEValuation:RBALlocation:AUTO OFF")
            Callbox.write(f"CONF:LTE:MEAS:MEV:RBAL:NRB {NRB}")
            Callbox.write("CONF:LTE:MEAS:MEV:RBAL:ORB 0")

        Callbox.write(f"CONF:LTE:MEAS:RFS:UMAR 10.000000")
        Callbox.write(f"CONF:LTE:MEAS:RFS:ENP {pwr+5:5.2f}")
        Callbox.write("INIT:LTE:MEAS:MEV")
        # initiate check
        func.Check_OPC(Callbox)
        # Meas rdy check
        word = "FETC:LTE:MEAS:MEV:STAT?"
        while True:
            response = Callbox.query(f"{word}")
            time.sleep(0.1)
            if response == "RDY\n":
                break

        TX_power, Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2 = func.Query_aclr("LTE", Callbox)
        Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)

        List_aclr = [Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2]
        text_area.tag_config("red_bold", foreground="red", font=("Consolas", 9, "bold"))
        text_area.insert(tk.END, f"    {pwr:>3}    |  {TX_power:>6.2f}   |   ")
        for aclr in List_aclr:
            if aclr < 38.0:
                text_area.insert(tk.END, f"{aclr:^5.2f}", "red_bold")
                text_area.insert(tk.END, f"   |   ")
            else:
                text_area.insert(tk.END, f"{aclr:^5.2f}")
                text_area.insert(tk.END, f"   |   ")
        text_area.insert(tk.END, f"{Pa_current:>4d}   |  {Sy_current:>4d}   \n")
        text_area.see(tk.END)
        # word = "FETC:LTE:MEAS:MEV:SEM:MARG?" # SEM 마진 생략
        # Ask_query(Callbox, text_area, word, word)
        # word = "FETC:LTE:MEAS:MEV:SEM:AVER?"
        # Ask_query(Callbox, text_area, word, word)
        # plot Start
        list_Power.append(TX_power)
        list_ACLR_L.append(0 - Leutra)
        list_ACLR_R.append(0 - Reutra)
        list_ACLR_max = max(list_ACLR_L, list_ACLR_R)
        Power_delta.append(TX_power - pwr)

        if Pa_current <= 0:
            list_Pa_current.append(Sy_current)
        else:
            list_Pa_current.append(Pa_current)

        func.update_plot(
            canvas,
            fig,
            ax1,
            ax2,
            ax3,
            "LTE",
            path,
            band,
            channel,
            bandwidth,
            list_Power,
            Power_delta,
            list_Pa_current,
            list_ACLR_max,
        )
        Callbox.write("STOP:LTE:MEAS:MEV")
        func.Check_OPC(Callbox)

        tx_result.loc[pwr, :] = [
            TX_power,
            Lutra2,
            Lutra1,
            Leutra,
            Reutra,
            Rutra1,
            Rutra2,
            Pa_current,
            Sy_current,
        ]
    str_time = datetime.now().strftime("%y%m%d_%H%M%S_")
    fig.savefig(save_dir + str_time + f"NonSig_LTE_B{band}_{path}_{channel}CH_BW{bandwidth}M" + ".png", dpi=300)

    return tx_result


def NR_tx_measure(
    dut,
    Equip,
    Callbox,
    E3632a_1,
    E3632a_2,
    path,
    Testband,
    channel,
    bandwidth,
    pwr_levels,
    canvas,
    fig,
    ax1,
    ax2,
    ax3,
    save_dir,
    text_area,
):

    rxfreq, txfreq = NR_channel_converter(Testband, channel)

    list_Power = []
    Power_delta = []
    list_Pa_current = []
    list_ACLR_L = []
    list_ACLR_R = []

    if path == "Main":
        path_number = 0
    elif path == "Sub":
        path_number = 1

    text_area.insert(tk.END, "\n")
    text_area.insert(tk.END, "*" * 45)
    text_area.insert(tk.END, f" NR n{Testband:<2} {path} {channel:>5}CH {bandwidth}MHz ")
    text_area.insert(tk.END, "*" * 44)
    text_area.insert(tk.END, "\n")
    response = dut.at_write(f"AT+NRFFINALSTART={Testband},0")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)

    NRB, outfull_offset, PRB, infull_offset = Num_RB("NR", Testband, bandwidth)
    BW_number = func.define_BW_number("NR", bandwidth)
    func.Nonsig_nr_tx_measure_setting(
        dut,
        Callbox,
        Equip,
        path_number,
        Testband,
        bandwidth,
        BW_number,
        PRB,
        infull_offset,
        rxfreq,
        txfreq,
        text_area,
    )

    text_area.insert(tk.END, "-" * 116)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)
    text_area.insert(
        tk.END,
        f"   TARGET  |   POWER   |   UTRA2   |   UTRA1   |  E-UTRA1  |  E-UTRA1  |   UTRA1   |   UTRA2  "
        f" |  P.AMP  |  SYSTEM  \n",
    )
    text_area.see(tk.END)
    text_area.insert(tk.END, "-" * 116)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)

    columns = [
        "TX POWER",
        "UTRA ACLR2-",
        "UTRA ACLR1-",
        "EUTRA ACLR-",
        "EUTRA ACLR+",
        "UTRA ACLR1+",
        "UTRA ACLR2+",
        "PA",
        "SYSTEM",
    ]
    one_channel_tx_result = pd.DataFrame("", index=pwr_levels, columns=columns)
    one_channel_tx_result.columns.name = "Target"

    for pwr in pwr_levels:
        if pwr == 23:  # 23dBm 12RB Setting
            if Testband in [38, 40, 41, 77, 78]:  # SCS 30
                response = dut.at_write(f"AT+NTXSENDREQ={path_number},{txfreq},1,1,{PRB},{infull_offset},2,0,23")
            else:  # SCS 15
                response = dut.at_write(f"AT+NTXSENDREQ={path_number},{txfreq},1,0,{PRB},{infull_offset},2,0,23")

            Callbox.write(f"CONF:NRS:MEAS:RFS:UMAR 10.000000")
            Callbox.write(f"CONF:NRS:MEAS:RFS:ENP {pwr+5:5.2f}")
            func.Check_OPC(Callbox)
        else:
            if Testband in [38, 40, 41, 77, 78]:  # SCS 30
                response = dut.at_write(f"AT+NTXSENDREQ={path_number},{txfreq},1,1,{NRB},{outfull_offset},2,0,{pwr}")
            else:  # SCS 15
                response = dut.at_write(f"AT+NTXSENDREQ={path_number},{txfreq},1,0,{NRB},{outfull_offset},2,0,{pwr}")

            Callbox.write(f"CONF:NRS:MEAS:MEV:RBAL:NRB {NRB}")
            Callbox.write(f"CONF:NRS:MEAS:MEV:RBAL:ORB {outfull_offset}")
            Callbox.write(f"CONF:NRS:MEAS:RFS:UMAR 10.000000")
            Callbox.write(f"CONF:NRS:MEAS:RFS:ENP {pwr+5:5.2f}")
            func.Check_OPC(Callbox)

        func.Check_nr_status(Callbox)
        TX_power, Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2 = func.Query_aclr("NR", Callbox)
        Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)

        List_aclr = [Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2]
        text_area.tag_config("red_bold", foreground="red", font=("Consolas", 9, "bold"))
        text_area.insert(tk.END, f"    {pwr:>3}    |  {TX_power:>6.2f}   |   ")
        for aclr in List_aclr:
            if aclr < 38.0:
                text_area.insert(tk.END, f"{aclr:^5.2f}", "red_bold")
                text_area.insert(tk.END, f"   |   ")
            else:
                text_area.insert(tk.END, f"{aclr:^5.2f}")
                text_area.insert(tk.END, f"   |   ")
        text_area.insert(tk.END, f"{Pa_current:>4d}   |  {Sy_current:>4d}   \n")
        text_area.see(tk.END)

        # plot Start
        list_Power.append(TX_power)
        list_ACLR_L.append(0 - Leutra)
        list_ACLR_R.append(0 - Reutra)
        list_ACLR_max = max(list_ACLR_L, list_ACLR_R)
        Power_delta.append(TX_power - pwr)

        if Pa_current <= 0:
            list_Pa_current.append(Sy_current)
        else:
            list_Pa_current.append(Pa_current)

        func.update_plot(
            canvas,
            fig,
            ax1,
            ax2,
            ax3,
            "NR",
            path,
            Testband,
            channel,
            bandwidth,
            list_Power,
            Power_delta,
            list_Pa_current,
            list_ACLR_max,
        )
        Callbox.write("STOP:NRS:MEAS:MEV")
        func.Check_OPC(Callbox)

        one_channel_tx_result.loc[pwr, :] = [
            TX_power,
            Lutra2,
            Lutra1,
            Leutra,
            Reutra,
            Rutra1,
            Rutra2,
            Pa_current,
            Sy_current,
        ]
    str_time = datetime.now().strftime("%y%m%d_%H%M%S_")
    fig.savefig(save_dir + str_time + f"NonSig_NRS_n{Testband}_{path}_{channel}CH {bandwidth}MHz" + ".jpg", dpi=300)

    return one_channel_tx_result
