import time
import tkinter as tk
import pandas as pd
import Function as func

pd.options.display.float_format = "{:.5f}".format


def Apt_tune(Callbox, E3632a_1, E3632a_2, pwr, band, mipi):
    pass


def Tune_bias():
    pass

def Tune_voltage():
    pass
def Dispaly_TX_log(pwr, PA_mipi_read, SM_mipi_read, Callbox, E3632a_1, E3632a_2, text_area):
    Callbox.write("INIT:NRS:MEAS:MEV")
    aclr = Callbox.query("FETC:NRS:MEAS:MEV:ACLR:AVER?").split(",")
    Leutra = round(float(aclr[3]), 2)
    TX_power = round(float(aclr[4]), 2)
    Reutra = round(float(aclr[5]), 2)
    Pwr_diff = pwr - TX_power
    Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)

    text_area.insert(
        tk.END,
        f"    {pwr:>3}    |  {TX_power:>6.2f}   |   {Pwr_diff:^5.2f}   |   {Leutra:^5.2f}   |  "
        f" {Reutra:^5.2f}   |   {PA_mipi_read:^5}   |   {SM_mipi_read:^5}   |  {Pa_current:^5d}  | "
        f" {Sy_current:^5d}  \n",
    )
    text_area.see(tk.END)

    return TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current


def Dsp_off_tx_measure(dut, Callbox, band, pwr, Mipi_data, E3632a_1, E3632a_2, text_area):

    if band in [1, 2, 3, 4, 7, 25, 66, 38, 39, 40, 41]:
        PA_mipi = Mipi_data["OMH_PA"]
        SM_mipi = Mipi_data["OMH_SM"]
        PA_mipi_addr = "2"
        SM_mipi_addr = "2"
    else:
        PA_mipi = Mipi_data["LB_PA"]
        SM_mipi = Mipi_data["LB_SM"]
        PA_mipi_addr = "1"
        SM_mipi_addr = "2"

    PA_mipi_read = int(func.Read_mipi(dut, PA_mipi, PA_mipi_addr, text_area).split(":")[1], base=16)
    SM_mipi_read = int(func.Read_mipi(dut, SM_mipi, SM_mipi_addr, text_area).split(":")[1], base=16)
    # Hmipi_read = func.Hmipi_read(dut, PA_mipi, "1", text_area)

    TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
        pwr, PA_mipi_read, SM_mipi_read, Callbox, E3632a_1, E3632a_2, text_area
    )
    Aclr_min = min(Leutra, Reutra)

    while Aclr_min > 40:
        res = func.Write_mipi(dut, PA_mipi, PA_mipi_addr, PA_mipi_read - 4, text_area)
        TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
            pwr, PA_mipi_read, SM_mipi_read, Callbox, E3632a_1, E3632a_2, text_area
        )
        Aclr_min = min(Leutra, Reutra)

        PA_mipi_read = int(func.Read_mipi(dut, PA_mipi, PA_mipi_addr, text_area).split(":")[1], base=16)
        SM_mipi_read = int(func.Read_mipi(dut, SM_mipi, SM_mipi_addr, text_area).split(":")[1], base=16)

        if Aclr_min < 38:
            break
        # Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)
        # text_area.see(tk.END)

    if Pwr_diff >= 0.5:
        response = dut.at_write("AT+NTXAPTTUNESET=2")  # Gain up
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n\n")
        text_area.see(tk.END)
        while True:
            Set_expected_pwr(Callbox, pwr)
            TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
                pwr, PA_mipi_read, SM_mipi_read, Callbox, E3632a_1, E3632a_2, text_area
            )
            res = func.Write_mipi(dut, PA_mipi, PA_mipi_addr, PA_mipi_read - 4, text_area)
            if Pwr_diff < 0.5:
                break
    elif Pwr_diff < -0.5:
        response = dut.at_write("AT+NTXAPTTUNESET=3")  # Gain down
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n\n")
        text_area.see(tk.END)
        while True:
            Set_expected_pwr(Callbox, pwr)
            TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
                pwr, PA_mipi_read, SM_mipi_read, Callbox, E3632a_1, E3632a_2, text_area
            )
            res = func.Write_mipi(dut, PA_mipi, PA_mipi_addr, PA_mipi_read - 4, text_area)
            if Pwr_diff > 0.5:
                break
    else:
        Set_expected_pwr(Callbox, pwr)
        TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current = Dispaly_TX_log(
            pwr, PA_mipi_read, SM_mipi_read, Callbox, E3632a_1, E3632a_2, text_area
        )

    return TX_power, Pwr_diff, Leutra, Reutra, Pa_current, Sy_current


def Set_expected_pwr(Callbox, pwr):
    Callbox.write(f"CONF:NRS:MEAS:RFS:UMAR 10.000000")
    Callbox.write(f"CONF:NRS:MEAS:RFS:ENP {pwr+5:5.2f}")
    func.Check_OPC(Callbox)
