import time
from datetime import datetime
import math
import tkinter as tk
import tkinter.messagebox as msgbox
import pandas as pd

import Function as func
import Tx_measure_Nonsig as Nonsig


def Callbox_reset(Selected_path, Equip, Callbox, text_area):
    Callbox.write("SYST:RES:ALL")
    text_area.insert(tk.END, f"RESET Call Box {Equip}\n")
    text_area.see(tk.END)
    func.Check_OPC(Callbox)
    Callbox.write("SYST:PRES:ALL")
    func.Check_OPC(Callbox)
    func.loss_table(Selected_path, "Loss_table_Main", Equip, Callbox)


def Call_connection(Callbox, E3632a_1, E3632a_2, dut, text_area):
    # CALL연결
    sec = 0
    status = Callbox.query("FETC:LTE:SIGN:PSW:STAT?").strip("\n")
    count = 0
    while status != "ATT":
        if count > 3:
            recycle = func.OCP_Check(E3632a_1, E3632a_2, text_area)
            func.Psupply_vcc_on_off(E3632a_1, 4.5)
            response = dut.check_bcm(text_area)
            count = 0
        if status == "OFF":
            # Callbox.write("SOUR:LTE:SIGN:CELL:STAT OFF")
            Callbox.write("SOUR:LTE:SIGN:CELL:STAT ON")
            time.sleep(5)
            func.Check_OPC(Callbox)
        if status == "CEST":
            text_area.insert(tk.END, f"\t{status:<5}\n")
            break
        status = Callbox.query("FETC:LTE:SIGN:PSW:STAT?").strip("\n")
        time.sleep(1)
        sec += 1
        # Callbox.write("SYST:DISP:UPD ON")
        P_cursor = float(math.trunc(float(text_area.index(tk.INSERT))))  # cursor 위치 얻기 위해 소수점 버림 -> 소수점 형식으로 변경
        text_area.delete(P_cursor, tk.END)
        text_area.insert(tk.END, f"\n")
        # text_area.delete("current linestart", "current lineend") cursor 위치 기준으로 삭제되서 쓸 수 없음.
        text_area.insert(tk.END, f"{status:<4} {sec:>3} Sec.")
        text_area.see(tk.END)
        if sec == 50:
            text_area.insert(tk.END, f"\n")
            response = dut.at_write("AT+MODECHAN=0,2")
            response = dut.at_write("AT+DISPTEST=0,3")
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            text_area.see(tk.END)
            response = dut.at_write("AT+AIRPMODE=0,0,0,1")
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            text_area.see(tk.END)
            time.sleep(1)
            response = dut.at_write("AT+AIRPMODE=0,0,0,0")
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            response = dut.at_write("AT+DISPTEST=0,4")
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            text_area.see(tk.END)
            response = dut.at_write("AT+MODECHAN=0,0")
            sec = 0
            count += 1

    Callbox.write("CALL:LTE:SIGN:PSW:ACT CONN")
    time.sleep(3)
    func.Check_OPC(Callbox)
    text_area.insert(tk.END, f"\n")

    return status


def Handover(Callbox, dut, E3632a_1, E3632a_2, band, channel, text_area):
    Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:CLTPower 10")
    Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:SET CLOop")
    Callbox.write("CONFigure:LTE:SIGN:DL:RSEP:LEV -50")

    while True:
        if band in [38, 39, 40, 41]:
            Tdd_initialize(Callbox, 38, 38000, text_area)
            stat = Call_connection(Callbox, E3632a_1, E3632a_2, dut, text_area)
            Tdd_measure_setting(Callbox)
        Callbox.write(f"PREP:LTE:SIGN:HAND OB{band}, {channel}, B100, NS01")
        Callbox.write("CALL:LTE:SIGN:HAND:STAR")
        time.sleep(3)
        func.Check_OPC(Callbox)
        # Que Overflow 발생
        Callbox.write("CALL:LTE:SIGN:PSW:ACT CONN")
        func.Check_OPC(Callbox)
        Connected_CH = int(Callbox.query("CONFigure:LTE:SIGN:RFS:PCC:CHAN:DL?"))

        if channel == Connected_CH:
            break

    return Connected_CH


def Fdd_initialize(Callbox, band, channel, text_area):
    ###초기화###
    # text_area.insert(tk.END, "FDD Initialize\n")
    Callbox.write("ABORt:LTE:MEAS:MEValuation")
    Callbox.write("SOUR:LTE:SIGN:CELL:STAT OFF")
    Callbox.write("CONFigure:LTE:SIGN:RFS:EATT:INP 0;OUTP 0")
    Callbox.write("CONFigure:LTE:SIGN:CELL:MCC 1")
    Callbox.write("CONFigure:LTE:SIGN:CELL:MNC 1")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SEC:AUTH ON;NAS ON;AS ON;MIL OFF")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SEC:OPC #H00000000000000000000000000000000")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SEC:SKEY #H4147494C454E5420544543484E4F0000")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SEC:IALG S3G")
    Callbox.write("CONFigure:LTE:SIGN:DMODe FDD")
    Callbox.write(f"CONFigure:LTE:SIGN:BAND OB{band}")
    Callbox.write(f"CONFigure:LTE:SIGN:RFS:CHAN:DL {channel}")
    Callbox.write("CONFigure:LTE:SIGN:CELL:BAND:DL B100")
    Callbox.write("CONFigure:LTE:SIGN:CONN:RMC:UL N50,QPSK,KEEP")
    Callbox.write("CONFigure:LTE:SIGN:DL:RSEP:LEV -50.0")
    Callbox.write("CONFigure:LTE:SIGN:UL:TPC:SET CLO")
    Callbox.write("CONFigure:LTE:SIGN:UL:TPC:CLTP 10")
    Callbox.write("INIT:LTE:MEAS:MEV")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:MEAS:MEV:RES:ACLR ON")
    Callbox.write("CONFigure:LTE:MEAS:MEV:REP SING")
    Callbox.write("ROUT:LTE:MEAS:SCEN:SAL RF1C, RX1")
    Callbox.write("ROUT:LTE:MEAS:SCEN:CSP 'LTE Sig1'")
    time.sleep(3)
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:CONNection:KRRC OFF")
    func.Check_OPC(Callbox)
    Callbox.query("FETC:LTE:SIGN:PSW:STAT?")
    # CELL ON
    Callbox.write("SOUR:LTE:SIGN:CELL:STAT ON")
    func.Check_OPC(Callbox)
    # 측정셋팅
    Callbox.write("INIT:LTE:MEAS:MEV")
    Callbox.write("CONFigure:LTE:MEAS:MEV:RES:ACLR ON")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:MEAS:MEV:REP SING")
    Callbox.write("ROUT:LTE:MEAS:SCEN:SAL RF1C, RX1")
    Callbox.write("ROUT:LTE:MEAS:SCEN:CSP 'LTE Sig1'")
    time.sleep(2)
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:MEASurement:MEValuation:SCOunt:SPECtrum:ACLR 20")
    func.Check_OPC(Callbox)


def Tdd_initialize(Callbox, band, channel, text_area):
    # TDD 초기화
    # text_area.insert(tk.END, "TDD Initialize\n")
    Callbox.write("ABORt:LTE:MEAS:MEValuation")
    Callbox.write("SOUR:LTE:SIGN:CELL:STAT OFF")
    Callbox.write("CONFigure:LTE:SIGN:DL:RSEP:LEV -50.0")
    Callbox.write("CONFigure:LTE:SIGN:DMODe TDD")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:RFS:EATT:INP 0;OUTP 0")
    Callbox.write("CONFigure:LTE:SIGN:UL:TPC:SET CLO")
    Callbox.write("CONFigure:LTE:SIGN:UL:TPC:CLTP -10")
    Callbox.write("CONFigure:LTE:SIGN:UL:PUSCh:OLNPower -10")
    Callbox.write("CONFigure:LTE:SIGN:DL:RSEP:LEV -85")
    Callbox.write(f"CONFigure:LTE:SIGN:BAND OB{band}")
    Callbox.write(f"CONFigure:LTE:SIGN:RFS:CHAN:DL {channel}")
    Callbox.write("CONFigure:LTE:SIGN:CELL:BAND:DL B100")
    Callbox.write("CONFigure:LTE:SIGN:CONN:RMC:UL N50,QPSK,KEEP")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SECurity:AUTHenticat ON")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SECurity:NAS ON")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SECurity:AS ON")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SECurity:MILenage OFF")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SECurity:IALGorithm S3G")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:CELL:SEC:OPC #H0000000000000000000000000")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SECurity:SKEY #H4147494C454E5420544543484E4F0000")
    Callbox.write("CONFigure:LTE:SIGN:CELL:MNC:DIGits TWO")
    Callbox.write("CONFigure:LTE:SIGN:CELL:MCC 1")
    Callbox.write("CONFigure:LTE:SIGN:CELL:MNC 1")
    Callbox.write("CONFigure:LTE:SIGN:CONN:OBCH RED")
    Callbox.write("CONFigure:LTE:SIGN:CONN:FCH BHAN")
    Callbox.write("CONFigure:LTE:SIGN:UL:PMAX 26")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:CELL:ULDL 1")
    Callbox.write("CONFigure:LTE:SIGN:CELL:SSUBframe 7")
    Callbox.write("ROUTe:LTE:MEAS:SCENario:CSPath 'LTE Sig1'")
    Callbox.write("CONFigure:LTE:SIGN:CONNection:KRRC OFF")
    Callbox.write("SOUR:LTE:SIGN:CELL:STAT ON")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:CONNection:SCC1:ASEMission:CAGGregation ns01")


def Fdd_measure_setting(Callbox):
    # 측정셋팅
    Callbox.write("ABORt:LTE:MEAS:MEValuation")
    Callbox.write("INIT:LTE:MEAS:MEV")
    func.Check_OPC(Callbox)
    Callbox.write(
        "CONFigure:LTE:MEAS:MEV:RES:ALL OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF"
    )
    time.sleep(1)
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:MEAS:MEV:RES:ACLR ON")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:MEAS:MEV:REP SING")
    Callbox.write("CONFigure:LTE:MEAS:MEValuation:SCON NONE")
    Callbox.write("CONFigure:LTE:MEAS:MEV:RBAL:AUTO ON")
    Callbox.write("CONFigure:LTE:MEASurement:MEValuation:SCOunt:SPECtrum:ACLR 20")
    Callbox.write("INIT:LTE:MEAS:MEV")
    func.Check_OPC(Callbox)


def Tdd_measure_setting(Callbox):
    # 측정셋팅
    Callbox.write("ABORt:LTE:MEAS:MEValuation")
    Callbox.write("ROUTe:LTE:MEAS:SCENario:CSPath 'LTE Sig1'")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:CONN:PCC:RMC:DL N50,QPSK,KEEP")
    Callbox.write("CONFigure:LTE:SIGN:CONN:PCC:RMC:UL N12,QPSK,KEEP")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:CONN:PCC:RMC:RBP:UL LOW")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:SIGN:UPL:TPC:SET MAXP")
    func.Check_OPC(Callbox)
    Callbox.write("CONFigure:LTE:MEAS:MEV:MSUB 0,10,2")
    Callbox.write("TRIG:LTE:MEAS:MEV:SOUR 'LTE Sig1: FrameTrigger'")
    Callbox.write("CONFigure:LTE:MEAS:MEValuation:MOEXception OFF")
    Callbox.write("CONFigure:LTE:MEAS:MEValuation:REPetition SINGleshot")
    Callbox.write("CONFigure:LTE:MEAS:MEValuation:SCON NONE")
    Callbox.write("CONFigure:LTE:MEAS:MEV:RBALlocation:AUTO ON")
    Callbox.write("CONFigure:LTE:MEAS:MEV:MOD:MSCH AUTO")
    Callbox.write("CONFigure:LTE:MEAS:MEV:CTYP AUTO")
    Callbox.write("CONFigure:LTE:MEAS:MEV:SCOunt:MODulation 10")
    Callbox.write("CONFigure:LTE:MEAS:MEV:SCOunt:SPECtrum:SEMask 1")
    Callbox.write("CONFigure:LTE:MEAS:MEV:SCOunt:SPECtrum:ACLR 1")
    Callbox.write("CONFigure:LTE:MEAS:MEV:SCOunt:POWer 1")
    Callbox.write(
        "CONFigure:LTE:MEAS:MEV:RES:ALL OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF"
    )
    time.sleep(1)
    Callbox.write("CONFigure:LTE:MEAS:MEV:RES:ACLR ON")
    func.Check_OPC(Callbox)
    Callbox.write("INIT:LTE:MEAS:MEV")
    func.Check_OPC(Callbox)


def calldrop_check(dut, Callbox, E3632a_1, E3632a_2, PwrL, text_area):
    Callbox.write("INIT:LTE:MEAS:MEV")
    aclr = Callbox.query("FETCh:LTE:MEASurement:MEValuation:ACLR:AVER?").split(",")

    while aclr[4] == "INV":
        stat = Callbox.query("FETC:LTE:SIGN:PSW:STAT?").strip("\n")
        func.Check_OPC(Callbox)
        if stat == "ATT":
            Callbox.write("CALL:LTE:SIGN:PSWitched:ACT CONN")
            func.Check_OPC(Callbox)
        stat = Callbox.query("FETC:LTE:SIGN:PSW:STAT?").strip("\n")
        func.Check_OPC(Callbox)
        if stat == "CEST":
            break
        text_area.insert(tk.END, "Call Dropped\n")
        response = dut.at_write("AT+MODECHAN=0,2")
        response = dut.at_write("AT+AIRPMODE=0,0,0,1")
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
        time.sleep(1)
        response = dut.at_write("AT+AIRPMODE=0,0,0,0")
        text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
        response = dut.at_write("AT+MODECHAN=0,0")
        stat = Call_connection(Callbox, E3632a_1, E3632a_2, dut, text_area)
        aclr = Callbox.query("FETCh:LTE:MEAS:MEValuation:ACLR:AVERage?").split(",")

    Callbox.write("CONFigure:LTE:SIGN:UL:TPC:SET MAXP")
    func.Check_OPC(Callbox)
    Callbox.write(f"CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:CLTPower {PwrL}")
    Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:SET CLOop")
    Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:SET CONS")
    Callbox.write("CONFigure:LTE:SIGN:DL:RSEP:LEV -85")
    Callbox.write("INIT:LTE:MEAS:MEV")
    func.Check_OPC(Callbox)
    aclr = Callbox.query("FETCh:LTE:MEAS:MEValuation:ACLR:AVERage?").split(",")

    return aclr


def Pwr_setting(Callbox, PwrL, text_area):
    Callbox.write("CONFigure:LTE:SIGN:DL:RSEP:LEV -88")

    if PwrL == 23:
        Status = Callbox.query("FETC:LTE:SIGN:PSW:STAT?").strip("\n")
        func.Check_OPC(Callbox)
        while Status == "ATT":
            if Status == "CEST":
                break
            Callbox.write("CALL:LTE:SIGN:PSWitched:ACTion CONNect")
            time.sleep(3)
            func.Check_OPC(Callbox)
            Status = Callbox.query("FETC:LTE:SIGN:PSW:STAT?")  # loop를 벗어나기 위한 state check
            func.Check_OPC(Callbox)

        # UL RMC Config for 23dBm Partial RB Setting
        Callbox.write("CONFigure:LTE:SIGN:CONN:RMC:UL N12,QPSK,KEEP")
        func.Check_OPC(Callbox)
        Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:CLTPower 26")
        func.Check_OPC(Callbox)
        Callbox.write("CONFigure:LTE:SIGN:UL:TPC:SET MAXP")
        func.Check_OPC(Callbox)

    else:
        Callbox.write("CALL:LTE:SIGN:PSWitched:ACTion DISConnect")
        func.Check_OPC(Callbox)
        Status = Callbox.query("FETC:LTE:SIGN:PSW:STAT?").strip("\n")

        while Status == "ATT":
            if Status == "CEST":
                break
            Callbox.write("CALL:LTE:SIGN:PSWitched:ACTion CONNect")
            time.sleep(3)
            func.Check_OPC(Callbox)
            Status = Callbox.query("FETC:LTE:SIGN:PSW:STAT?")  # loop를 벗어나기 위한 state check

    Callbox.write(f"CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:CLTPower {PwrL}")
    Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:SET CLOop")
    Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:SET CONS")
    Callbox.write("CONFigure:LTE:MEAS:MEValuation:REP SING")
    Callbox.write("INIT:LTE:MEAS:MEV")
    func.Check_OPC(Callbox)

    Status = Callbox.query("FETCh:LTE:MEASurement:MEV:STATe?")
    while Status != "RDY\n":
        Status = Callbox.query("FETCh:LTE:MEASurement:MEV:STATe?")
        time.sleep(0.1)
        if Status == "RDY\n":
            break


def Power_loop(
    dut,
    Callbox,
    path,
    Testband,
    channel,
    bandwidth,
    pwr_levels,
    E3632a_1,
    E3632a_2,
    canvas,
    fig,
    ax1,
    ax2,
    ax3,
    save_dir,
    text_area,
):
    response = dut.at_write("AT+MODECHAN=0,2")
    response = dut.at_write("AT+DISPTEST=0,4")
    response = dut.at_write("AT+MODECHAN=0,0")
    list_Power = []
    Power_delta = []
    list_Pa_current = []
    list_ACLR_L = []
    list_ACLR_R = []
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
        "Total",
    ]
    tx_result = pd.DataFrame("", index=pwr_levels, columns=columns)
    tx_result.columns.name = "Target"

    text_area.insert(
        tk.END,
        f"   TARGET  |   POWER   |   UTRA2   |   UTRA1   |  E-UTRA1  |  E-UTRA1  |   UTRA1   |   UTRA2   |"
        f"   P.AMP  |  SYSTEM  \n",
    )
    text_area.see(tk.END)
    text_area.insert(tk.END, "-" * 116)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)

    for PwrL in pwr_levels:
        Retry_count = 1

        aclr = calldrop_check(dut, Callbox, E3632a_1, E3632a_2, PwrL, text_area)
        Pwr_setting(Callbox, PwrL, text_area)

        Callbox.write("INIT:LTE:MEAS:MEV")
        func.Check_OPC(Callbox)
        aclr = Callbox.query("FETCh:LTE:MEASurement:MEValuation:ACLR:AVER?").split(",")

        if aclr[4] == "INV":
            aclr = calldrop_check(dut, Callbox, E3632a_1, E3632a_2, PwrL, text_area)

        Callbox.write("INIT:LTE:MEAS:MEV")
        func.Check_OPC(Callbox)
        aclr = Callbox.query("FETCh:LTE:MEASurement:MEValuation:ACLR:AVER?").split(",")

        if aclr[4] == "INV":
            aclr = calldrop_check(dut, Callbox, E3632a_1, E3632a_2, PwrL, text_area)

        Lutra2 = round(float(aclr[1]), 2)
        Lutra1 = round(float(aclr[2]), 2)
        Leutra = round(float(aclr[3]), 2)
        TX_power = round(float(aclr[4]), 2)
        Reutra = round(float(aclr[5]), 2)
        Rutra1 = round(float(aclr[6]), 2)
        Rutra2 = round(float(aclr[7]), 2)

        Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)
        total_current = Pa_current + Sy_current

        if PwrL != 23:
            Power_diff = round(abs(TX_power - float(PwrL)), 1)
            Max_diff = 0.5

            while Power_diff > Max_diff:
                List_aclr = [Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2]
                text_area.tag_config("red_bold", foreground="red", font=("Consolas", 9, "bold"))
                text_area.insert(tk.END, f"    {PwrL:>3}    |  {TX_power:>6.2f}   |   ")
                for i_aclr in List_aclr:
                    if i_aclr < 38.0:
                        text_area.insert(tk.END, f"{i_aclr:^5.2f}", "red_bold")
                        text_area.insert(tk.END, f"   |   ")
                    else:
                        text_area.insert(tk.END, f"{i_aclr:^5.2f}")
                        text_area.insert(tk.END, f"   |   ")
                text_area.insert(tk.END, f"{Pa_current:>4d}   |   {Sy_current:>4d}   \n")
                text_area.see(tk.END)
                text_area.insert(tk.END, "-" * 116)
                text_area.insert(
                    tk.END,
                    f"\nPower difference is greater than {Max_diff}dB, Target = {PwrL}, Retry Count"
                    f" {Retry_count} (Max : 3)\n",
                )
                text_area.see(tk.END)

                Callbox.write("CONFigure:LTE:SIGN:CONN:RMC:UL N50,QPSK,KEEP")
                func.Check_OPC(Callbox)
                Callbox.write("CALL:LTE:SIGN:PSWitched:ACTion DISConnect")
                func.Check_OPC(Callbox)
                Callbox.write("CONFigure:LTE:SIGN:UL:TPC:SET MAXP")
                Callbox.write("CALL:LTE:SIGN:PSWitched:ACTion CONNect")
                time.sleep(2)
                func.Check_OPC(Callbox)
                Callbox.write(f"CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:CLTPower {PwrL}")
                func.Check_OPC(Callbox)
                Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:SET CLOop")
                func.Check_OPC(Callbox)
                Callbox.write("CONFigure:LTE:SIGN:UL:PCC:PUSCh:TPC:SET CONS")
                func.Check_OPC(Callbox)
                Callbox.write("CONFigure:LTE:SIGN:DL:RSEP:LEV -88")
                Callbox.write("INIT:LTE:MEAS:MEV")
                func.Check_OPC(Callbox)

                Closed_loop_PW = float(Callbox.query("CONFigure:LTE:SIGN:UL:TPC:CLTP?"))
                func.Check_OPC(Callbox)
                aclr = Callbox.query("FETCh:LTE:MEASurement:MEValuation:ACLR:AVER?").split(",")

                if aclr[4] == "INV":
                    aclr = calldrop_check(dut, Callbox, E3632a_1, E3632a_2, PwrL, text_area)

                TX_power = round(float(aclr[4]), 1)
                Leutra = round(float(aclr[3]), 1)
                Reutra = round(float(aclr[5]), 1)
                Sy_current, Pa_current = func.PA_Current_Measure(E3632a_1, E3632a_2)
                total_current = Pa_current + Sy_current
                Power_diff = round(abs(TX_power - float(PwrL)), 1)

                if Power_diff < Max_diff:
                    break
                elif Retry_count >= 3:
                    text_area.insert(tk.END, "TX Power mismatch\n")
                    break
                else:
                    Retry_count += 1

        List_aclr = [Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2]
        text_area.tag_config("red_bold", foreground="red", font=("Consolas", 9, "bold"))
        text_area.insert(tk.END, f"    {PwrL:>3}    |  {TX_power:>6.2f}   |   ")
        for i_aclr in List_aclr:
            if i_aclr < 38.0:
                text_area.insert(tk.END, f"{i_aclr:^5.2f}", "red_bold")
                text_area.insert(tk.END, f"   |   ")
            else:
                text_area.insert(tk.END, f"{i_aclr:^5.2f}")
                text_area.insert(tk.END, f"   |   ")
        text_area.insert(tk.END, f"{Pa_current:>4d}   |   {Sy_current:>4d}   \n")
        text_area.see(tk.END)

        tx_result.loc[PwrL, :] = [
            TX_power,
            Lutra2,
            Lutra1,
            Leutra,
            Reutra,
            Rutra1,
            Rutra2,
            Pa_current,
            Sy_current,
            total_current,
        ]
        # plot Start
        list_Power.append(TX_power)
        list_ACLR_L.append(0 - Leutra)
        list_ACLR_R.append(0 - Reutra)
        list_ACLR_max = max(list_ACLR_L, list_ACLR_R)
        Power_delta.append(TX_power - PwrL)

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
            Testband,
            channel,
            bandwidth,
            list_Power,
            Power_delta,
            list_Pa_current,
            list_ACLR_max,
        )
    str_time = datetime.now().strftime("%y%m%d_%H%M%S_")
    fig.savefig(save_dir + str_time + f"Signaling_LTE_B{Testband}_{channel}CH {bandwidth}MHz" + ".png", dpi=300)

    return tx_result


def LTE_Signaling_test(
    dut,
    Equip,
    Callbox,
    E3632a_1,
    E3632a_2,
    Main_loss,
    Sub_loss,
    rat,
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
):

    Equipment = Callbox.query("*IDN?").split(",")[1]

    if (Equipment == "CMW") & (Equip == "TCPIP0::127.0.0.1"):
        msgbox.showwarning("Warning", "Impossible to run with CMW100")
        return

    Callbox.write("SYST:DISP:UPD ON")

    Nonsig.Set_factolog(dut, text_area)

    for key in Test_band_ch_list:
        if key == 0:
            path = "Main"
            path_number = 0
            func.loss_table(Main_loss, "Loss_table_Main", Equip, Callbox)

        elif key == 1:
            path = "Sub"
            path_number = 1
            func.loss_table(Sub_loss, "Loss_table_Sub", Equip, Callbox)

        for Testband in Test_band_ch_list[key]:
            channel_list = Test_band_ch_list[key][Testband]
            bandwidth_list = BW_list[key][Testband]
            Status = Callbox.query("FETC:LTE:SIGN:PSW:STAT?").strip("\n")
            band_tx_result = []
            ch_tx_result = []
            if Status != "CEST":
                if Testband in [38, 39, 40, 41]:
                    Tdd_initialize(Callbox, 38, 38000, text_area)
                    stat = Call_connection(Callbox, E3632a_1, E3632a_2, dut, text_area)
                    time.sleep(3)
                    Tdd_measure_setting(Callbox)
                else:
                    Fdd_initialize(Callbox, 1, 300, text_area)
                    stat = Call_connection(Callbox, E3632a_1, E3632a_2, dut, text_area)
                    time.sleep(3)
                    Fdd_measure_setting(Callbox)

            for channel in channel_list:
                bandwidth_tx_result = []

                for bandwidth in bandwidth_list:
                    Connected_CH = int(Callbox.query("CONFigure:LTE:SIGN:RFS:PCC:CHAN:DL?"))

                    if channel != Connected_CH:
                        Connected_CH = Handover(Callbox, dut, E3632a_1, E3632a_2, Testband, channel, text_area)

                    text_area.insert(tk.END, "\n")
                    text_area.insert(tk.END, "*" * 44)
                    text_area.insert(tk.END, f" {rat} B{Testband:<2} {path} {Connected_CH:>5}CH {bandwidth:>2d}MHz ")
                    text_area.insert(tk.END, "*" * 44)
                    text_area.insert(tk.END, "\n")
                    text_area.see(tk.END)

                    tx_result = Power_loop(
                        dut,
                        Callbox,
                        path,
                        Testband,
                        channel,
                        bandwidth,
                        pwr_levels,
                        E3632a_1,
                        E3632a_2,
                        canvas,
                        fig,
                        ax1,
                        ax2,
                        ax3,
                        save_dir,
                        text_area,
                    )
                    bandwidth_tx_result.append(tx_result)

                ch_tx_result = pd.concat(
                    bandwidth_tx_result,
                    axis=0,
                    keys=[str(bw) + " MHz" for bw in bandwidth_list],
                    names=[f"LTE B{Testband} {path} {channel}CH"],
                )
                band_tx_result.append(ch_tx_result)

            Total_tx_result = pd.concat(
                band_tx_result,
                axis=1,
                keys=[str(ch) + " CH" for ch in channel_list],
                names=[f"LTE B{Testband} {path}"],
            )

            func.resut_to_excel(Total_tx_result, filename, f"LTE B{Testband} {path}")
            func.WB_Format(filename, 1, 1, 0)

    func.images2PdfFile(save_dir, filename)
