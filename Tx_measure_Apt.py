import tkinter as tk
from datetime import datetime

import pandas as pd

import Function as func
from Band_list import NR_channel_converter, Num_RB

pd.options.display.float_format = "{:.5f}".format


def Tune_bias():
    pass


def Tune_voltage():
    pass


def Dsp_off_tx_measure(
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
    Mipi_data,
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
    text_area.insert(tk.END, "*" * 44)
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

    # DSP off
    response = dut.at_write(f"AT+NTXAPTTUNESET=1")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")

    text_area.insert(tk.END, "-" * 115)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)
    delta = "\u0394"
    text_area.insert(
        tk.END,
        f"   TARGET  |  POWER  | POWERΔ |  E-UTRA-  |  E-UTRA+  | PA_MIPI | SM_MIPI | RFIC G1 | RFIC G2 |  P.AMP  |  SYSTEM  \n",
    )
    text_area.see(tk.END)
    text_area.insert(tk.END, "-" * 115)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)

    columns = [
        "TX POWER",
        "POWER Diff.",
        "EUTRA ACLR-",
        "EUTRA ACLR+",
        "PA_MIPI",
        "SM_MIPI",
        "PA",
        "SYSTEM",
    ]
    one_channel_tx_result = pd.DataFrame("", index=pwr_levels, columns=columns)
    one_channel_tx_result.columns.name = "Target"

    for pwr in pwr_levels:
        if pwr > 23:  # 23dBm 12RB Setting
            continue
        elif pwr == 23:
            if Testband in [38, 40, 41, 77, 78]:  # SCS 30
                response = dut.at_write(f"AT+NTXSENDREQ={path_number},{txfreq},1,1,{PRB},{infull_offset},2,0,{pwr}")
            else:  # SCS 15
                response = dut.at_write(f"AT+NTXSENDREQ={path_number},{txfreq},1,0,{PRB},{infull_offset},2,0,{pwr}")

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

        TX_power, Pwr_diff, Leutra, Reutra, PA_mipi_read, SM_mipi_read, Pa_current, Sy_current = Apt_tune(
            dut, Callbox, E3632a_1, E3632a_2, Testband, pwr, Mipi_data, text_area
        )

        # plot Start
        list_Power.append(TX_power)
        list_ACLR_L.append(0 - Leutra)
        list_ACLR_R.append(0 - Reutra)
        list_ACLR_max = max(list_ACLR_L, list_ACLR_R)
        Power_delta.append(Pwr_diff)

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
            Pwr_diff,
            Leutra,
            Reutra,
            PA_mipi_read,
            SM_mipi_read,
            Pa_current,
            Sy_current,
        ]
    str_time = datetime.now().strftime("%y%m%d_%H%M%S_")
    fig.savefig(save_dir + str_time + f"NonSig_NRS_n{Testband}_{path}_{channel}CH {bandwidth}MHz" + ".png", dpi=300)

    return one_channel_tx_result


def Set_expected_pwr(Callbox, pwr):
    Callbox.write(f"CONF:NRS:MEAS:RFS:UMAR 10.000000")
    Callbox.write(f"CONF:NRS:MEAS:RFS:ENP {pwr+5:5.2f}")
    func.Check_OPC(Callbox)


def Apt_tune(dut, Callbox, E3632a_1, E3632a_2, Testband, pwr, Mipi_data, text_area):
    if Testband in [1, 2, 3, 4, 7, 25, 66, 38, 39, 40, 41]:
        PA_mipi = Mipi_data["OMH_PA"]
        SM_mipi = Mipi_data["OMH_SM"]
    elif Testband in [77, 78]:
        PA_mipi = Mipi_data["NR_PA"]
        SM_mipi = Mipi_data["NR_SM"]
    else:
        PA_mipi = Mipi_data["LB_PA"]
        SM_mipi = Mipi_data["LB_SM"]

    PA_mipi_addr = PA_mipi[2].get()
    SM_mipi_addr = SM_mipi[2].get()
    PA_mipi_read = int(func.Read_mipi(dut, "NR", PA_mipi, PA_mipi_addr, text_area).split(":")[1], base=16)
    SM_mipi_read = int(func.Read_mipi(dut, "NR", SM_mipi, SM_mipi_addr, text_area).split(":")[1], base=16)
    # Hmipi_read = func.Hmipi_read(dut, PA_mipi, "1", text_area)

    rfic1 = dut.at_write("AT+NSPIREAD=157")[2].split(":")[1]  # RFIC Gain1
    rfic2 = dut.at_write("AT+NSPIREAD=197")[2].split(":")[1]  # RFIC Gain2

    TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
        pwr, PA_mipi_read, SM_mipi_read, rfic1, rfic2, Callbox, E3632a_1, E3632a_2, text_area
    )
    Aclr_min = min(Leutra, Reutra)

    while Aclr_min > 40:
        PA_mipi_read -= 4
        at_resp = func.Write_mipi(dut, "NR", PA_mipi, PA_mipi_addr, PA_mipi_read, text_area)
        PA_mipi_read = int(func.Read_mipi(dut, "NR", PA_mipi, PA_mipi_addr, text_area).split(":")[1], base=16)
        SM_mipi_read = int(func.Read_mipi(dut, "NR", SM_mipi, SM_mipi_addr, text_area).split(":")[1], base=16)

        rfic1 = dut.at_write("AT+NSPIREAD=157")[2].split(":")[1]  # RFIC Gain1
        rfic2 = dut.at_write("AT+NSPIREAD=197")[2].split(":")[1]  # RFIC Gain2

        TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
            pwr, PA_mipi_read, SM_mipi_read, rfic1, rfic2, Callbox, E3632a_1, E3632a_2, text_area
        )
        Aclr_min = min(Leutra, Reutra)
        if Aclr_min < 38:
            break
        # Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)
        # text_area.see(tk.END)

    if Pwr_diff >= 1:
        response = dut.at_write("AT+NTXAPTTUNESET=2")  # Gain up
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n\n")
        text_area.see(tk.END)

        rfic1 = dut.at_write("AT+NSPIREAD=157")[2].split(":")[1]  # RFIC Gain1
        rfic2 = dut.at_write("AT+NSPIREAD=197")[2].split(":")[1]  # RFIC Gain2

        while True:
            Set_expected_pwr(Callbox, pwr)
            TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
                pwr, PA_mipi_read, SM_mipi_read, rfic1, rfic2, Callbox, E3632a_1, E3632a_2, text_area
            )
            at_resp = func.Write_mipi(dut, "NR", PA_mipi, PA_mipi_addr, PA_mipi_read - 4, text_area)
            if Pwr_diff < 1:
                break

    elif Pwr_diff < -1:
        response = dut.at_write("AT+NTXAPTTUNESET=3")  # Gain down
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n\n")
        text_area.see(tk.END)

        rfic1 = dut.at_write("AT+NSPIREAD=157")[2].split(":")[1]  # RFIC Gain1
        rfic2 = dut.at_write("AT+NSPIREAD=197")[2].split(":")[1]  # RFIC Gain2

        while True:
            Set_expected_pwr(Callbox, pwr)
            TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
                pwr, PA_mipi_read, SM_mipi_read, rfic1, rfic2, Callbox, E3632a_1, E3632a_2, text_area
            )
            at_resp = func.Write_mipi(dut, "NR", PA_mipi, PA_mipi_addr, PA_mipi_read - 4, text_area)
            if Pwr_diff > -1:
                break
    else:
        Set_expected_pwr(Callbox, pwr)

        rfic1 = dut.at_write("AT+NSPIREAD=157")[2].split(":")[1]  # RFIC Gain1
        rfic2 = dut.at_write("AT+NSPIREAD=197")[2].split(":")[1]  # RFIC Gain2

        TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
            pwr, PA_mipi_read, SM_mipi_read, rfic1, rfic2, Callbox, E3632a_1, E3632a_2, text_area
        )

    return TX_power, Pwr_diff, Leutra, Reutra, PA_mipi_read, SM_mipi_read, Pa_current, Sy_current


def Dispaly_TX_log(pwr, PA_mipi_read, SM_mipi_read, rfic1, rfic2, Callbox, E3632a_1, E3632a_2, text_area):
    TX_power, Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2 = func.Query_aclr("NR", Callbox)
    Pwr_diff = pwr - TX_power
    Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)
    List_aclr = [Leutra, Reutra]

    text_area.tag_config("red_bold", foreground="red", font=("Consolas", 9, "bold"))
    text_area.insert(tk.END, f"     {pwr:>2}    |  {TX_power:>5.2f}  |  {Pwr_diff:^4.1f}  |   ")
    for aclr in List_aclr:
        if aclr < 38.0:
            text_area.insert(tk.END, f"{aclr:^5.2f}", "red_bold")
            text_area.insert(tk.END, f"   |   ")
        else:
            text_area.insert(tk.END, f"{aclr:^5.2f}")
            text_area.insert(tk.END, f"   |   ")
    text_area.insert(
        tk.END,
        f"{PA_mipi_read:^3}   |   {SM_mipi_read:^3}   |  {rfic1:^5}  |  {rfic2:^5}  |   {Pa_current:>3d}   |    {Sy_current:>3d}   \n",
    )
    text_area.see(tk.END)

    return TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current
