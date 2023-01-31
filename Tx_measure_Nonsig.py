import time
from datetime import datetime
import tkinter as tk
import pandas as pd
from Band_list import channel_converter, NR_channel_converter
import Function as func

pd.options.display.float_format = "{:.5f}".format


def Set_factolog(dut, text_area):
    response = dut.at_write("AT+MODECHAN=0,2")
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
    band,
    channel,
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

    text_area.insert(tk.END, "\n")
    text_area.insert(tk.END, "*" * 50)
    text_area.insert(tk.END, f" BAND{band:<2} {channel:>5} CH ")
    text_area.insert(tk.END, "*" * 49)
    text_area.insert(tk.END, "\n")
    response = dut.at_write("AT+HNSSTOP")
    response = dut.at_write(f"AT+LRFFINALSTART=1,{band}")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)
    response = dut.at_write("AT+LMODETEST")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)

    func.Nonsig_lte_tx_measure_setting(dut, Callbox, Equip, band, rxfreq, txfreq, text_area)

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
            Callbox.write("CONFigure:LTE:MEAS:MEValuation:RBALlocation:AUTO OFF")
            response = dut.at_write(f"AT+LTXSENDREQ=0,3,{txfreq},12,0,0,2,1,{pwr}")
            # response = dut.at_write(f"AT+LTXPWRLVLSET={pwr}")
            # response = dut.at_write("AT+LTXCHNSDREQ")
        else:
            response = dut.at_write(f"AT+LTXSENDREQ=0,3,{txfreq},50,0,0,2,1,{pwr}")
            # response = dut.at_write(f"AT+LTXPWRLVLSET={pwr}")
            # response = dut.at_write("AT+LTXCHNSDREQ")
            Callbox.write("CONFigure:LTE:MEAS:MEValuation:RBALlocation:AUTO OFF")
            Callbox.write("CONF:LTE:MEAS:MEV:RBAL:NRB 50")
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

        text_area.insert(
            tk.END,
            f"    {pwr:>3}    |  {TX_power:>6.2f}   |   {Lutra2:^5.2f}   |   {Lutra1:^5.2f}   |  "
            f" {Leutra:^5.2f}   |   {Reutra:^5.2f}   |   {Rutra1:^5.2f}   |   {Rutra2:^5.2f}   | "
            f" {Pa_current:>5d}  |   {Sy_current:>5d}  \n",
        )
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
            canvas, fig, ax1, ax2, ax3, "LTE", band, channel, list_Power, Power_delta, list_Pa_current, list_ACLR_max
        )
        Callbox.write("STOP:LTE:MEAS:MEV")
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
    fig.savefig(save_dir + str_time + f"NonSig_LTE_B{band}_{channel}CH" + ".png", dpi=300)

    return one_channel_tx_result


def NR_tx_measure(
    dut,
    Equip,
    Callbox,
    E3632a_1,
    E3632a_2,
    band,
    channel,
    pwr_levels,
    canvas,
    fig,
    ax1,
    ax2,
    ax3,
    save_dir,
    text_area,
):

    rxfreq, txfreq = NR_channel_converter(band, channel)

    list_Power = []
    Power_delta = []
    list_Pa_current = []
    list_ACLR_L = []
    list_ACLR_R = []

    text_area.insert(tk.END, "\n")
    text_area.insert(tk.END, "*" * 50)
    text_area.insert(tk.END, f" n{band:<2} {channel:>5} CH ")
    text_area.insert(tk.END, "*" * 49)
    text_area.insert(tk.END, "\n")
    response = dut.at_write(f"AT+NRFFINALSTART={band},0")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)

    func.Nonsig_nr_tx_measure_setting(dut, Callbox, Equip, band, rxfreq, txfreq, text_area)

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
            if band in [38, 40, 41, 77, 78]:  # SCS 30
                response = dut.at_write(f"AT+NTXSENDREQ=0,{txfreq},1,1,12,6,2,0,23")
            else:  # SCS 15
                response = dut.at_write(f"AT+NTXSENDREQ=0,{txfreq},1,0,25,12,2,0,23")

            Callbox.write(f"CONF:NRS:MEAS:RFS:UMAR 10.000000")
            Callbox.write(f"CONF:NRS:MEAS:RFS:ENP {pwr+5:5.2f}")
            func.Check_OPC(Callbox)
        else:
            if band in [38, 40, 41, 77, 78]:  # SCS 30
                response = dut.at_write(f"AT+NTXSENDREQ=0,{txfreq},1,1,24,0,2,0,{pwr}")
            else:  # SCS 15
                response = dut.at_write(f"AT+NTXSENDREQ=0,{txfreq},1,0,50,0,2,0,{pwr}")

            Callbox.write("CONF:NRS:MEAS:MEV:RBAL:NRB 50")
            Callbox.write("CONF:NRS:MEAS:MEV:RBAL:ORB 0")
            Callbox.write(f"CONF:NRS:MEAS:RFS:UMAR 10.000000")
            Callbox.write(f"CONF:NRS:MEAS:RFS:ENP {pwr+5:5.2f}")
            func.Check_OPC(Callbox)

        func.Check_nr_status(Callbox)
        TX_power, Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2 = func.Query_aclr("NR", Callbox)
        Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)

        text_area.insert(
            tk.END,
            f"    {pwr:>3}    |  {TX_power:>6.2f}   |   {Lutra2:^5.2f}   |   {Lutra1:^5.2f}   |  "
            f" {Leutra:^5.2f}   |   {Reutra:^5.2f}   |   {Rutra1:^5.2f}   |   {Rutra2:^5.2f}   | "
            f" {Pa_current:>5d}  |   {Sy_current:>5d}  \n",
        )
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
            canvas, fig, ax1, ax2, ax3, "NR", band, channel, list_Power, Power_delta, list_Pa_current, list_ACLR_max
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
    fig.savefig(save_dir + str_time + f"NonSig_NRS_B{band}_{channel}CH" + ".png", dpi=300)

    return one_channel_tx_result
