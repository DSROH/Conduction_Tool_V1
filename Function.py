import os
import time
from datetime import datetime

import serial
import pyvisa as visa
from io import StringIO

import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import filedialog

import img2pdf

from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.styles.numbers import builtin_format_code

import pandas as pd
import numpy as np

import threading

from Band_list import *
import Tx_measure_Apt as Apt
import Tx_measure_Nonsig as Nonsig
import Tx_measure_Signaling as Sig

font_style = Font(
    name="Calibri",
    size=10,
    bold=False,
    italic=False,
    vertAlign=None,  # 첨자
    underline="none",  # 밑줄
    strike=False,  # 취소선
    color="00000000",  # 블랙, # 00FF0000 Red, # 000000FF Blue
)


class Open_Dut:
    def __init__(self, Comport):
        self.ser = serial.Serial(
            port=Comport,
            baudrate=115200,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=0.3,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        )

    def serial_open(self):
        self.ser.o()

    def serial_close(self):
        self.ser.c()

    def con_check(self):
        if self.ser.is_open == 0:
            return 0
        else:
            return 1

    def at_write(self, cmd):
        self.cmd_add = cmd + "\r\n"
        self.ser.reset_input_buffer()
        self.ser.write(self.cmd_add.encode())
        self.raw_responses = self.ser.readlines()
        self.ser.reset_output_buffer()

        self.responses = []
        for line_response in self.raw_responses:
            self.responses.append(line_response.strip().decode())
        # print(self.responses)
        return self.responses  # , self.read

    def check_bcm(self, text_area):
        while True:
            response = self.ser.readlines()
            for line_response in response:
                # 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte : decode() -> decode('latin1') 으로 변경
                line = line_response.strip().decode("latin1")
                text_area.insert(tk.END, f"{line}\n")
                text_area.see(tk.END)
                if line == "BOOTING COMPLETED":
                    return line


def return_print(*prt_str):  # print 출력값을 변수로 리턴
    io = StringIO()
    print(*prt_str, file=io, sep=",", end="")
    return io.getvalue()


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("\tError: Failed to create directory.")


def add_file(log_path):
    default_path = os.path.join(
        os.path.expanduser("~"), "C:\\DIST\\CONFIG\\DASEUL\\CABLE_LOSS\\"
    )
    log_path.delete(0, tk.END)
    files = filedialog.askopenfilename(
        title="loss 파일을 선택하세요",
        filetypes=(("dec 파일", "*.dec"), ("txt 파일", "*.txt"), ("모든 파일", "*.*")),
        initialdir=default_path,
    )
    # 사용자가 선택한 파일 목록
    log_path.insert(tk.END, files)
    Selected_path = log_path.get()

    if Selected_path == "":
        msgbox.showwarning("경고", "Loss 파일을 선택하세요")
        return


def resut_to_excel(result, file_name, name_of_sheet):
    if not os.path.exists(file_name):  # 파일이 없으면 쓰기모드
        with pd.ExcelWriter(file_name, mode="w", engine="openpyxl") as writer:
            result.to_excel(writer, sheet_name=name_of_sheet)

    else:  # 파일이 있으면 어펜드 모드
        with pd.ExcelWriter(file_name, mode="a", engine="openpyxl") as writer:
            result.to_excel(writer, sheet_name=name_of_sheet)


def WB_Format(filename, i, j, k):
    wb = load_workbook(filename)
    ws = wb.sheetnames
    for sheet in ws:
        col_max = wb[sheet].max_column
        row_max = wb[sheet].max_row
        for row_c in range(i, row_max + 1, 1):
            for col_c in range(j, col_max + 1, 1):
                wb[sheet].cell(row=row_c, column=col_c).font = font_style
                wb[sheet].cell(row=row_c, column=col_c).alignment = Alignment(
                    horizontal="center"
                )
                # wb[sheet].cell(row=row_c, column=col_c).number_format = "#,##0.0"
                wb[sheet].cell(
                    row=row_c, column=col_c
                ).number_format = builtin_format_code(k)
    wb.save(filename)


def Check_mipi_R(text_area, rat, mipi_data, combo4):
    text_area.delete("1.0", tk.END)
    Comport = combo4.get()
    ch = mipi_data[0].get()
    usid = mipi_data[1].get()
    addr = mipi_data[2].get()

    dut = Open_Dut(Comport)
    at_resp = dut.at_write("AT+MODECHAN=0,0")
    at_resp = dut.at_write("AT+HNSSTOP")
    if rat == "LTE":
        at_resp = dut.at_write("AT+LRFFINALSTART=1,1")
    elif rat == "NR":
        # AT+NRFFINALSTART=Band, SA
        # SA : 0, NSA : 1
        at_resp = dut.at_write("AT+NRFFINALSTART=1,0")
    text_area.insert(tk.END, f"{at_resp[0]:<25}\t|\t{at_resp[2:3:2]}\n")
    at_resp = dut.at_write(f"AT+MIPIREAD = {ch},{usid},{addr}")
    text_area.insert(tk.END, f"{at_resp[0]:<25}\t|\t{at_resp[2:3:2]}\n")
    at_resp = dut.at_write("AT+MODECHAN=0,2")
    text_area.see(tk.END)


def Check_mipi_W(text_area, rat, mipi_data, combo4):
    text_area.delete("1.0", tk.END)
    Comport = combo4.get()
    ch = mipi_data[0].get()
    usid = mipi_data[1].get()
    addr = mipi_data[2].get()
    data = mipi_data[3].get()

    dut = Open_Dut(Comport)
    at_resp = dut.at_write("AT+MODECHAN=0,0")
    at_resp = dut.at_write("AT+HNSSTOP")
    if rat == "LTE":
        at_resp = dut.at_write("AT+LRFFINALSTART=1,1")
    elif rat == "NR":
        # AT+NRFFINALSTART=Band, SA
        # SA : 0, NSA : 1
        at_resp = dut.at_write("AT+NRFFINALSTART=1,0")
    text_area.insert(tk.END, f"{at_resp[0]:<25}\t|\t{at_resp[2:3:2]}\n")
    at_resp = dut.at_write(f"AT+MIPIWRITE = {ch},{usid},{addr},{data}")
    text_area.insert(tk.END, f"{at_resp[0]:<25}\t|\t{at_resp[2:3:2]}\n")
    at_resp = dut.at_write("AT+MODECHAN=0,2")
    text_area.see(tk.END)


def Read_mipi(dut, rat, mipi_data, addr, text_area):
    ch = mipi_data[0].get()
    if rat == "LTE":
        usid = mipi_data[1].get()
        at_resp = dut.at_write(f"AT+MIPIREAD = {ch},{usid},{addr}")
    elif rat == "NR":
        usid = hex(int(mipi_data[1].get())).strip("0x")
        at_resp = dut.at_write(f"AT+NMIPIREAD = {ch},{usid},{addr}")

    return at_resp[2]


def Write_mipi(dut, rat, mipi_data, addr, data, text_area):
    ch = mipi_data[0].get()
    if rat == "LTE":
        usid = mipi_data[1].get()
        at_resp = dut.at_write(f"AT+MIPIWRITE = {ch},{usid},{addr}")
    elif rat == "NR":
        usid = hex(int(mipi_data[1].get())).strip("0x")
        at_resp = dut.at_write(f"AT+NMIPIWRITE = {ch},{usid},{addr}")
    print(f"Write Bias = {data}, {at_resp[2:]}")
    return at_resp[2]


def Hmipi_read(dut, mipi_data, addr, text_area):
    ch = mipi_data[0].get()
    usid = hex(int(mipi_data[1].get())).strip("0x")
    at_resp = dut.at_write(f"AT+HREADMIPI = {ch},{usid},{addr}")

    return at_resp


def Power_on(combo2, combo3, combo4, text_area):
    text_area.delete("1.0", tk.END)
    Sys_power = combo2.get()
    Pa_power = combo3.get()
    Comport = combo4.get()

    if Sys_power == "":
        msgbox.showwarning("Warning", "Check System Power")
        return
    elif Pa_power == "":
        msgbox.showwarning("Warning", "Check PA VCC")
        return

    rm = visa.ResourceManager()
    E3632a_1 = rm.open_resource(Sys_power)  # SYS전류측정 Power supply
    if Pa_power == "NO Supply for PA":
        E3632a_2 = "NO Supply for PA"
    else:
        E3632a_2 = rm.open_resource(Pa_power)  # PA전류측정 Power supply

    text_area.insert(tk.END, f"Start threading\n")
    text_area.insert(tk.END, f"Thread count = {threading.active_count()}\n")

    for thread in threading.enumerate():
        text_area.insert(
            tk.END,
            f"Thread ID = {threading.get_ident()}, Thread name = {thread.name}\n",
        )
    text_area.see(tk.END)

    text_area.insert(tk.END, f"\nSystem Power = {Sys_power}\t|\tPA VCC = {Pa_power}\n")
    text_area.see(tk.END)

    # OCP Check 후 Sys_Power Off -> On
    recycle = OCP_Check(E3632a_1, E3632a_2, text_area)
    Psupply_vcc_on_off(E3632a_1, 4.5)

    dut = Open_Dut(Comport)
    response = dut.check_bcm(text_area)

    if response == "BOOTING COMPLETED":
        msgbox.showinfo("Info", "BOOTING COMPLETED")


def Start(
    Main_loss_path,
    Sub_loss_path,
    combo1,
    combo2,
    combo3,
    combo4,
    Run_mode_var,
    Rat_option_var,
    Ch_option_var,
    User_defined_path,
    User_defined_band,
    User_defined_ch,
    Band_Select_Main_var,
    Band_Select_Sub_var,
    BW_list,
    Pw_option_var,
    Mipi_data,
    canvas,
    fig,
    ax1,
    ax2,
    ax3,
    text_area,
):
    try:
        Main_loss = Main_loss_path.get()
        Sub_loss = Sub_loss_path.get()
        text_area.delete("1.0", tk.END)
        Run_mode = Run_mode_var.get()
        Equip = combo1.get()
        Sys_power = combo2.get()
        Pa_power = combo3.get()
        Comport = combo4.get()

        if Equip == "TCPIP::127.0.0.1::INSTR":
            C_Box = "CMW100"
        elif Equip == "GPIB0::20::INSTR":
            C_Box = "CMW500"

        text_area.insert(tk.END, f"Start threading\n")
        text_area.insert(tk.END, f"Thread count = {threading.active_count()}\n")

        for thread in threading.enumerate():
            text_area.insert(
                tk.END,
                f"Thread ID = {threading.get_ident()}, Thread name = {thread.name}\n",
            )
        text_area.see(tk.END)

        if Equip == "":
            msgbox.showwarning("Warning", "Check Call Box")
            return
        elif Sys_power == "":
            msgbox.showwarning("Warning", "Check System Power")
            return
        elif Pa_power == "":
            msgbox.showwarning("Warning", "Check PA VCC")
            return
        elif Comport == "":
            msgbox.showwarning("Warning", "Check Comport")
            return
        elif (C_Box == "CMW500") & (Rat_option_var.get() == 3):
            msgbox.showwarning("Warning", "Choose CMW100")
            return

        rm = visa.ResourceManager()
        Callbox = rm.open_resource(Equip)
        Callbox.timeout = 20000
        E3632a_1 = rm.open_resource(Sys_power)  # SYS전류측정 Power supply
        if Pa_power == "NO Supply for PA":
            E3632a_2 = "NO Supply for PA"
        else:
            E3632a_2 = rm.open_resource(Pa_power)  # PA전류측정 Power supply

        text_area.insert(
            tk.END,
            f"\nCallBox = {Equip}\t|\tSystem Power = {Sys_power}\t|\tPA VCC = {Pa_power}\n",
        )
        text_area.see(tk.END)
        # Callbox reset 시 losstable setting 진행
        Sig.Callbox_reset(Main_loss, Equip, Callbox, text_area)

        Test_band_ch_list = Check_testband(
            Rat_option_var,
            Ch_option_var,
            User_defined_path,
            User_defined_band,
            User_defined_ch,
            Band_Select_Main_var,
            Band_Select_Sub_var,
        )
        pwr_levels = Check_pwr_lvs(Rat_option_var.get(), Pw_option_var.get())
        today = datetime.today().strftime("%Y_%m_%d")
        start_T = datetime.today().strftime("%Y%m%d_%H%M")
        save_dir = os.getcwd() + "\\Measurement_Result\\" + today + "\\"
        createDirectory(save_dir)

        dut = Open_Dut(Comport)
        recycle = OCP_Check(E3632a_1, E3632a_2, text_area)

        if recycle:
            bcm_check = dut.check_bcm(text_area)

        if not Test_band_ch_list:
            msgbox.showwarning("Warning", "Select Test Band")
            return

        # Singaling test
        elif Run_mode == 1:
            if Rat_option_var.get() == 1:  # 3G
                msgbox.showwarning("Warning", "Not supported yet")
                return

            elif Rat_option_var.get() == 2:  # LTE
                filename = save_dir + f"LTE_Current_{C_Box}_{start_T}.xlsx"
                Sig.LTE_Signaling_test(
                    dut,
                    Equip,
                    Callbox,
                    E3632a_1,
                    E3632a_2,
                    Main_loss,
                    Sub_loss,
                    "LTE",
                    Test_band_ch_list,
                    BW_list,
                    pwr_levels,
                    canvas,
                    fig,
                    ax1,
                    ax2,
                    ax3,
                    save_dir,
                    filename,
                    text_area,
                )

        # Non-Singaling test
        elif Run_mode == 2:
            if Rat_option_var.get() == 1:  # 3G
                msgbox.showwarning("Warning", "Not supported yet")
                return

            elif Rat_option_var.get() == 2:  # LTE
                filename = save_dir + f"LTE_NonSig_{C_Box}_{start_T}.xlsx"
                Callbox.write("SYST:DISP:UPD ON")
                Nonsig.Set_factolog(dut, text_area)

                for key in Test_band_ch_list:
                    if key == 0:
                        path = "Main"
                        loss_table(Main_loss, "Loss_table_Main", Equip, Callbox)
                    elif key == 1:
                        path = "Sub"
                        loss_table(Sub_loss, "Loss_table_Sub", Equip, Callbox)

                    for Testband in Test_band_ch_list[key]:
                        channel_list = Test_band_ch_list[key][Testband]
                        bandwidth_list = BW_list[key][Testband]
                        band_tx_result = []
                        bandwidth_tx_result = []
                        for bandwidth in bandwidth_list:
                            ch_tx_result = []
                            for channel in channel_list[bandwidth]:
                                tx_result = Nonsig.LTE_tx_measure(
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
                                )
                                Nonsig.End_testmode(dut, text_area)
                                ch_tx_result.append(tx_result)

                            bandwidth_tx_result = pd.concat(
                                ch_tx_result,
                                axis=1,
                                keys=[
                                    f"CH {i}"
                                    for i in range(1, len(channel_list[bandwidth]) + 1)
                                ],
                                # names=[f"LTE {path} B{Testband} {bandwidth}MHz"],
                            )
                            band_tx_result.append(bandwidth_tx_result)
                        Total_tx_result = pd.concat(
                            band_tx_result,
                            axis=0,
                            keys=[str(bw) + " MHz" for bw in bandwidth_list],
                            names=[f"LTE {path} B{Testband}"],
                        )
                        resut_to_excel(
                            Total_tx_result, filename, f"LTE {path} B{Testband}"
                        )
                        WB_Format(filename, 1, 1, 0)

                images2PdfFile(save_dir, filename)

            elif Rat_option_var.get() == 3:
                filename = save_dir + f"NR_NonSig_{C_Box}_{start_T}.xlsx"
                Callbox.write("SYST:DISP:UPD ON")
                Nonsig.Set_factolog(dut, text_area)

                for key in Test_band_ch_list:
                    if key == 0:
                        path = "Main"
                        loss_table(Main_loss, "Loss_table_Main", Equip, Callbox)
                    elif key == 1:
                        path = "Sub"
                        loss_table(Sub_loss, "Loss_table_Sub", Equip, Callbox)

                    for Testband in Test_band_ch_list[key]:
                        channel_list = Test_band_ch_list[key][Testband]
                        bandwidth_list = BW_list[key][Testband]
                        band_tx_result = []
                        bandwidth_tx_result = []
                        for bandwidth in bandwidth_list:
                            ch_tx_result = []
                            for channel in channel_list[bandwidth]:
                                tx_result = Nonsig.NR_tx_measure(
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
                                )
                                Nonsig.End_testmode(dut, text_area)
                                ch_tx_result.append(tx_result)

                            bandwidth_tx_result = pd.concat(
                                ch_tx_result,
                                axis=1,
                                keys=[
                                    f"CH {i}"
                                    for i in range(1, len(channel_list[bandwidth]) + 1)
                                ],
                                # names=[f"NR {path} n{Testband} {bandwidth}MHz"],
                            )
                            band_tx_result.append(bandwidth_tx_result)

                        Total_tx_result = pd.concat(
                            band_tx_result,
                            axis=0,
                            keys=[str(bw) + " MHz" for bw in bandwidth_list],
                            names=[f"NR {path} n{Testband}"],
                        )
                        resut_to_excel(
                            Total_tx_result, filename, f"NR {path} n{Testband}"
                        )
                        WB_Format(filename, 1, 1, 0)

                images2PdfFile(save_dir, filename)

        # APT Tuning
        elif Run_mode == 3:
            loss_table(Main_loss, "Loss_table_Main", Equip, Callbox)
            filename = save_dir + f"NR_APT_Tuning_{C_Box}_{start_T}.xlsx"
            Callbox.write("SYST:DISP:UPD ON")

            Nonsig.Set_factolog(dut, text_area)

            for key in Test_band_ch_list:
                if key == 0:
                    path = "Main"
                    loss_table(Main_loss, "Loss_table_Main", Equip, Callbox)
                elif key == 1:
                    path = "Sub"
                    loss_table(Sub_loss, "Loss_table_Sub", Equip, Callbox)
                for Testband in Test_band_ch_list[key]:
                    channel_list = Test_band_ch_list[key][Testband]
                    bandwidth_list = BW_list[key][Testband]
                    band_tx_result = []
                    bandwidth_tx_result = []
                    for bandwidth in bandwidth_list:
                        ch_tx_result = []
                        for channel in channel_list[bandwidth]:
                            tx_result = Apt.Dsp_off_tx_measure(
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
                            )
                            Nonsig.End_testmode(dut, text_area)
                            ch_tx_result.append(tx_result)

                        bandwidth_tx_result = pd.concat(
                            ch_tx_result,
                            axis=0,
                            keys=[
                                f"CH {i}"
                                for i in range(1, len(channel_list[bandwidth]) + 1)
                            ],
                            # names=[f"NR n{Testband} {channel}CH"],
                        )
                        band_tx_result.append(bandwidth_tx_result)
                    Total_tx_result = pd.concat(
                        band_tx_result,
                        axis=0,
                        keys=[str(bw) + " MHz" for bw in bandwidth_list],
                        names=[f"NR {path} n{Testband}"],
                    )
                    resut_to_excel(Total_tx_result, filename, f"NR {path} n{Testband}")
                    WB_Format(filename, 4, 2, 0)

            images2PdfFile(save_dir, filename)

        else:
            msgbox.showwarning("Warning", "Not supported")
            return

        text_area.see(tk.END)
        text_area.insert(tk.END, f"\n\n")
        response = dut.at_write("AT+MODECHAN=0,2")
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
        response = dut.at_write("AT+DISPTEST=0,3")
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
        text_area.see(tk.END)

        Psupply_off(E3632a_1, E3632a_2)
        msgbox.showinfo("Message", "***** 작업완료 *****")
        # rm.close()

    except ValueError as e:
        if str(e) == "Unable to process empty list":
            raise ValueError("Unable to process empty list")
        else:
            raise e
    except Exception as e:
        msgbox.showwarning("Warning", e)


def loss_table(Selected_path, table_name, Equip, Callbox):
    with open(Selected_path, "r", encoding="utf-8") as loss_file:
        fname, ext = os.path.splitext(Selected_path)
        if ext == ".txt":
            # 0번~4번 행 값 스킵하고, 각 컬럼명을 index와 value로 지정
            df = pd.read_csv(
                loss_file, sep="=", names=["index", "value"], skiprows=[0, 1, 2, 3, 4]
            )
        else:
            df = pd.read_csv(
                loss_file,
                sep="=",
                names=["index", "value"],
                # skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            )
    loss_file.close()
    Start_index = df.index[df["index"].str.contains("Measured_CableLoss_01")].tolist()
    df = df.loc[Start_index[0] + 2 :].reset_index()
    df = df[["index", "value"]]
    df = df[["value"]].assign(g=df.index % 2)

    Equipment = Callbox.query("*IDN?").split(",")[1]

    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        df_freq = df.loc[df["g"] == 0, "value"].astype(int) * 1000000.00
        df_loss = df.loc[df["g"] == 1, "value"].astype(float).abs()  # loss value
        df["value"] = df_freq.combine_first(df_loss)  # 2개 Series freq 기준으로 병합
        loss_list = list(df["value"])  # value 값 loss_list에 list로 저장
        loss = return_print(*loss_list)

        Callbox.write(f"CONF:FDC:DEAC:ALL")
        Callbox.write(f"CONF:BASE:FDC:CTAB:DEL:ALL")
        Callbox.write(f"CONF:BASE:FDC:CTAB:CRE '{table_name}', {loss}")
        Callbox.write(
            f"CONF:CMWS:FDC:ACT:TX R118,"
            f" '{table_name}','{table_name}','{table_name}','{table_name}','{table_name}','{table_name}','{table_name}','{table_name}'"
        )
        Callbox.write(
            f"CONF:CMWS:FDC:ACT:RX R118,"
            f" '{table_name}','{table_name}','{table_name}','{table_name}','{table_name}','{table_name}','{table_name}','{table_name}'"
        )

    else:
        df_freq = (
            df.loc[df["g"] == 0, "value"].astype(int).astype(str) + "e6"
        )  # Frequency 정수로 변환 후 문자열로 변환 & e6 추가
        df_loss = df.loc[df["g"] == 1, "value"].astype(float).abs()  # loss value
        df["value"] = df_freq.combine_first(df_loss)  # 2개 Series freq 기준으로 병합
        loss_list = list(df["value"])  # value 값 loss_list에 list로 저장
        loss = return_print(*loss_list)

        Callbox.write(f"CONF:FDC:DEAC RF1C")
        Callbox.write(f"CONF:BASE:FDC:CTAB:CRE '{table_name}',{loss}")
        Callbox.write(f"CONF:FDC:ACT RF1C, '{table_name}', RXTX")


def Callback_Sys_P(combo2):
    Sys_vcc = combo2.get()
    if Sys_vcc:
        print(f"System Power = {Sys_vcc}")


def Callback_PA_Vcc(combo3):
    Pa_vcc = combo3.get()
    if Pa_vcc:
        print(f"PA VCC = {Pa_vcc}")


def Callback_Comport(combo4):
    Comport = combo4.get()
    if Comport:
        print(f"Comport = {Comport}")


def OCP_Check(Sys_vcc, Pa_vcc, text_area):
    P_recycle = False
    E3632a = [Sys_vcc, Pa_vcc]

    for Psupply in E3632a:
        if Psupply != "NO Supply for PA":
            OCP_stat = Psupply.query("CURR:PROT:TRIP?")
            OVP_stat = Psupply.query("VOLT:PROT:TRIP?")

            if Psupply == Sys_vcc:
                Volt = 4.3
            elif Psupply == Pa_vcc:
                Volt = 4.0

            if (OCP_stat == "1\n") or (
                OVP_stat == "1\n"
            ):  # 리턴은 0 or 1이 아니고 \n 까지 붙어서 옴
                text_area.insert(tk.END, f"{Psupply} OCP/OVP TRIPPED")
                Psupply_init(Psupply)
                Psupply_vcc_on_off(Psupply, Volt)
                if Psupply == Sys_vcc:  # System 전원을 off 했을때만 P_recycle True 설정
                    P_recycle = True

            Outp_stat = Psupply.query("OUTP:STAT?").strip("\n")
            # print(f"{Psupply} Outp_stat ={Outp_stat}")
            if (Outp_stat == "0") or (
                int(float(Psupply.query("MEAS:CURR?")) * 1000) <= 5
            ):
                Psupply_vcc_on_off(Psupply, Volt)
                if Psupply == Sys_vcc:  # System 전원을 off 했을때만 P_recycle True 설정
                    P_recycle = True

    text_area.see(tk.END)

    return P_recycle


def Psupply_init(Psupply):
    Psupply.write("OUTP OFF")
    Psupply.write("CURR:PROT:CLE")
    time.sleep(0.5)
    Psupply.write("VOLT:PROT:CLE")
    time.sleep(0.5)


def Psupply_vcc_on_off(Psupply, vcc):
    Psupply.write(f"OUTP OFF")
    time.sleep(0.5)
    Psupply.write(f"VOLT {vcc}")
    Psupply.write(f"VOLT:PROT 15")
    Psupply.write(f"VOLT:PROT:STAT ON")
    Psupply.write(f"CURR:PROT 7.5")
    Psupply.write(f"CURR:PROT:STAT ON")
    Psupply.write(f"OUTP ON")
    # Psupply.control_ren(0)


def Psupply_off(Sys_vcc, Pa_vcc):
    time.sleep(0.5)
    Pa_vcc.write("OUTP OFF")
    # Pa_vcc.control_ren(0)
    time.sleep(0.5)
    Sys_vcc.write("OUTP OFF")
    # Sys_vcc.control_ren(0)


def Equipment_scan():
    # visa.log_to_screen()        # 장비로그 On
    rm = visa.ResourceManager()  # Resource Manager 생성
    Resource = rm.list_resources()  # Visa resource list
    CB_list = []
    PS_list1 = []
    PS_list2 = []
    CP_list = []

    for r in Resource:
        if r.startswith("ASRL"):
            com = r.replace("ASRL", "COM")
            com = com.split("::")[0]
            CP_list.append(com)

        if r.startswith("GPIB"):
            instrument = rm.open_resource(r, timeout=500)
            Equipment = instrument.query("*IDN?").split(",")
            # Power Supply list
            if Equipment[1] == "E3632A":
                PS_list1.append(r)
                PS_list2.append(r)
            elif Equipment[1] == "CMW":
                CB_list.append(r)

    rm = visa.ResourceManager("@py")  # pyvisa-py로 검색해야 TCPIP 잘 찾음
    Resource = rm.list_resources()  # Visa resource list
    # instr_list = ["TCPIP::127.0.0.1::5025::SOCKET"]
    cwm100 = "TCPIP::127.0.0.1::INSTR"

    for r in Resource:
        # Callbox list
        if r == cwm100:
            instrument = rm.open_resource(r, timeout=2000)
            Equipment = instrument.query("*IDN?").split(",")
            if Equipment[1] == "CMW":
                CB_list.append(r)

    PS_list2.append("NO Supply for PA")

    return CB_list, PS_list1, PS_list2, CP_list


def PA_Current_Measure(E3632a_1, E3632a_2):
    Sy_current = int(float(E3632a_1.query("MEAS:CURR?")) * 1000)

    if E3632a_2 == "NO Supply for PA":
        Pa_current = 0
    else:
        Pa_current = int(float(E3632a_2.query("MEAS:CURR?")) * 1000)

    return Sy_current, Pa_current


def Ask_query(Callbox, text_area, word_string, query_string):
    response = Callbox.query(f"{query_string}")
    text_area.insert(tk.END, f"{word_string:<40}\t|\t{response}")
    text_area.see(tk.END)


def Check_OPC(Callbox):
    response = Callbox.query("*OPC?")


def update_plot(
    canvas,
    fig,
    ax1,
    ax2,
    ax3,
    rat,
    path,
    Testband,
    channel,
    bandwidth,
    list_Power,
    Power_delta,
    list_Pa_current,
    list_ACLR_max,
):
    if rat == "LTE":
        band_ind = "B"
    elif rat == "NR":
        band_ind = "n"

    ax1.clear()
    x_min, x_max = axis_min_max(list_Power)
    ax1.axis(xmin=x_min, xmax=x_max)
    ax1.set_title(
        f"{rat} {band_ind}{Testband} {path} {channel}CH {bandwidth}MHz PA Current",
        fontsize=8,
    )
    ax1.set_xlabel("Measured Power (dBm)", fontsize=8)
    ax1.set_ylabel("PA Current (mA)", fontsize=8)
    ax1.grid(True, color="black", alpha=0.3, linestyle="--")
    ax1.plot(
        list_Power,
        list_Pa_current,
        marker="o",
        markersize=3,
        color="red",
        linewidth=0.7,
    )
    fig.tight_layout()

    ax2.clear()
    x_min, x_max = axis_min_max(list_Power)
    ax2.axis(xmin=x_min, xmax=x_max)
    ax2.axis(ymin=-1, ymax=2)
    ax2.set_title(f"Power Diff. ( Measured - Target )", fontsize=8)
    ax2.set_xlabel("Measured Power (dBm)", fontsize=8)
    # ax2.set_ylabel("Power Diff (dB)", fontsize=8)
    ax2.grid(True, color="black", alpha=0.3, linestyle="--")
    ax2.plot(list_Power, Power_delta, marker="o", markersize=3, linewidth=0.7)
    fig.tight_layout()

    ax3.clear()
    x_min, x_max = axis_min_max(list_Power)
    ax3.axis(xmin=x_min, xmax=x_max)
    ax3.set_title(f"ACLR (dBc)", fontsize=8)
    ax3.set_xlabel("Measured Power (dBm)", fontsize=8)
    # ax3.set_ylabel("ACLR (dBc)", fontsize=8)
    ax3.grid(True, color="black", alpha=0.3, linestyle="--")
    ax3.plot(list_Power, list_ACLR_max, marker="o", markersize=3, linewidth=0.7)
    ax3.axhline(
        y=-38, linestyle="dashdot", color="red", label="Target"
    )  # Spec 기준선 Drwaing
    fig.tight_layout()

    if len(list_Power) > 5:
        np_PW = np.array(list_Power)
        np_PA = np.array(list_Pa_current)

        z = np.polyfit(np_PW, np_PA, 5)  # (X,Y,차원) 정의
        p = np.poly1d(z)  # 1차원 다항식에 대한 연산을 캡슐화

        ax1.plot(np_PW, p(np_PW), "--", label=f"Trend-line {channel}CH", linewidth=1)
        ax1.legend(fontsize=8, frameon=False, loc="lower right", ncol=6)

    fig.tight_layout()

    canvas.draw()


def axis_min_max(x_list):
    if len(x_list) == 1:
        x_min = 0
        x_max = 25
    else:
        x_min = min(x_list) - 1
        x_max = max(x_list) + 1

    return x_min, x_max
