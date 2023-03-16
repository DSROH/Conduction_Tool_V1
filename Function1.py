def images2PdfFile(save_dir, filename):
    f_name = f"{os.path.splitext(filename)[0]}.pdf"

    filelist = sorted([file for file in os.listdir(save_dir) if file.endswith(r".jpg")])
    img_files = [os.path.join(save_dir, nm) for nm in filelist]

    with open(f_name, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(img_files, log_output=None))

    for f in img_files:
        os.remove(f)


def Check_nr_status(Callbox):
    # Meas rdy check
    word = "FETC:NRS:MEAS:MEV:STAT?"
    while True:
        response = Callbox.query(f"{word}")
        time.sleep(0.1)
        if response == "RDY\n":
            break


def Query_aclr(rat, Callbox):
    if rat == "LTE":
        Callbox.write("INIT:LTE:MEAS:MEV")
        Check_OPC(Callbox)
        aclr = Callbox.query("FETCh:LTE:MEASurement:MEValuation:ACLR:AVER?").split(",")
    elif rat == "NR":
        Callbox.write("INIT:NRS:MEAS:MEV")
        Check_OPC(Callbox)
        aclr = Callbox.query("FETCh:NRS:MEASurement:MEValuation:ACLR:AVER?").split(",")
    Lutra2 = round(float(aclr[1]), 2)
    Lutra1 = round(float(aclr[2]), 2)
    Leutra = round(float(aclr[3]), 2)
    TX_power = round(float(aclr[4]), 2)
    Reutra = round(float(aclr[5]), 2)
    Rutra1 = round(float(aclr[6]), 2)
    Rutra2 = round(float(aclr[7]), 2)

    return TX_power, Lutra2, Lutra1, Leutra, Reutra, Rutra1, Rutra2


def define_BW_number(rat, bandwidth):
    if rat == "LTE":
        match bandwidth:
            case 5:
                number = 2
            case 10:
                number = 3
            case 15:
                number = 4
            case 20:
                number = 5

    elif rat == "NR":
        match bandwidth:
            case 5:
                number = 0
            case 10:
                number = 1
            case 15:
                number = 2
            case 20:
                number = 3
            case 25:
                number = 4
            case 30:
                number = 5
            case 40:
                number = 6
            case 50:
                number = 7
            case 60:
                number = 8
            case 80:
                number = 9
            case 90:
                number = 10
            case 100:
                number = 11
            case 70:
                number = 12

    return number


def Set_limit_mask(Callbox, rat, bandwidth):
    if rat == "LTE":
        match bandwidth:
            case 5:
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN50 ON,0MHz,1MHz,-15,K030"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN50 ON,1MHz,2.5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN50 ON,2.5MHz,2.8MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN50 ON,2.8MHz,5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN50 ON,5MHz,6MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN50 ON,6MHz,10MHz,-25,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN50 OFF,10MHz,10MHz,-25,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN50 OFF,10MHz,10MHz,-25,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN50 OFF,10MHz,10MHz,-25,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN50 OFF,10MHz,10MHz,-25,M1"
                )
            case 10:
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN100 ON,0MHz,1MHz,-18,K030"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN100 ON,1MHz,2.5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN100 ON,2.5MHz,2.8MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN100 ON,2.8MHz,5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN100 ON,5MHz,6MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN100 ON,6MHz,10MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN100 ON,10MHz,15MHz,-25,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN100 OFF,15MHz,15MHz,-25,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN100 OFF,15MHz,15MHz,-25,M1"
                )
            case 15:
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN150 ON,0MHz,1MHz,-20,K030"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN150 ON,1MHz,2.5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN150 ON,2.5MHz,2.8MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN150 ON,2.8MHz,5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN150 ON,5MHz,6MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN150 ON,6MHz,10MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN150 ON,10MHz,15MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN150 ON,15MHz,20MHz,-25,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN150 OFF,20MHz,20MHz,-25,M1"
                )
            case 20:
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN200 ON,0,1MHz,-21,K030"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN200 ON,1MHz,2.5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN200 ON,2.5MHz,2.8MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN200 ON,2.8MHz,5MHz,-10,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN200 ON,5MHz,6MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN200 ON,6MHz,10MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN200 ON,10MHz,15MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN200 ON,15MHz,20MHz,-13,M1"
                )
                Callbox.write(
                    "CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN200 ON,20MHz,25MHz,-25,M1"
                )
    elif rat == "NR":
        match bandwidth:
            case 5:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN5 ON,0.015MHz,0.0985MHz,-13.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN5 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN5 ON,5.5MHz,4.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN5 ON,5.5MHz,9.5MHz,-23.5,M1"
                )
            case 10:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN10 ON,0.015MHz,0.0985MHz,-16.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN10 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN10 ON,5.5MHz,9.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN10 ON,10.5MHz,14.5MHz,-23.5,M1"
                )
            case 15:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN15 ON,0.015MHz,0.0985MHz,-18.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN15 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN15 ON,5.5MHz,14.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN15 ON,15.5MHz,19.5MHz,-23.5,M1"
                )
            case 20:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN20 ON,0.015MHz,0.0985MHz,-19.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN20 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN20 ON,5.5MHz,19.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN20 ON,20.5MHz,24.5MHz,-23.5,M1"
                )
            case 25:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN25 ON,0.015MHz,0.0985MHz,-20.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN25 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN25 ON,5.5MHz,24.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN25 ON,25.5MHz,29.5MHz,-23.5,M1"
                )
            case 30:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN30 ON,0.015MHz,0.0985MHz,-21.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN30 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN30 ON,5.5MHz,29.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN30 ON,30.5MHz,34.5MHz,-23.5,M1"
                )
            case 40:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN40 ON,0.015MHz,0.0985MHz,-22.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN40 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN40 ON,5.5MHz,39.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN40 ON,40.5MHz,44.5MHz,-23.5,M1"
                )
            case 50:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN50 ON,0.015MHz,0.0985MHz,-22.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN50 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN50 ON,5.5MHz,49.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN50 ON,50.5MHz,54.5MHz,-23.5,M1"
                )
            case 60:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN60 ON,0.015MHz,0.0985MHz,-22.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN60 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN60 ON,5.5MHz,59.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN60 ON,60.5MHz,64.5MHz,-23.5,M1"
                )
            case 70:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN70 ON,0.015MHz,0.0985MHz,26.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN70 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN70 ON,5.5MHz,69.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN70 ON,70.5MHz,74.5MHz,-23.5,M1"
                )
            case 80:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN80 ON,0.015MHz,0.0985MHz,-22.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN80 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN80 ON,5.5MHz,79.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN80 ON,80.5MHz,84.5MHz,-23.5,M1"
                )
            case 90:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN90 ON,0.015MHz,0.0985MHz,-22.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN90 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN90 ON,5.5MHz,89.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN90 ON,90.5MHz,94.5MHz,-23.5,M1"
                )
            case 100:
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN100 ON,0.015MHz,0.0985MHz,-22.5,K030"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN100 ON,1.5MHz,4.5MHz,-8.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN100 ON,5.5MHz,99.5MHz,-11.5,M1"
                )
                Callbox.write(
                    f"CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN100 ON,100.5MHz,104.5MHz,-23.5,M1"
                )


def Nonsig_lte_tx_measure_setting(
    dut,
    Callbox,
    Equip,
    path_number,
    band,
    bandwidth,
    BW_number,
    NRB,
    PRB,
    rxfreq,
    txfreq,
    text_area,
):
    Equipment = Callbox.query("*IDN?").split(",")[1]
    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        Callbox.write(f"ROUT:GPRF:GEN:SCEN:SAL R118, TX1")
        Callbox.write(
            f"CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF"
        )
        Check_OPC(Callbox)
    elif (Equipment == "CMW") & (Equip == "GPIB0::20::INSTR"):
        Callbox.write("*CLS")
        Callbox.write(f"ROUT:GPRF:GEN:SCEN:SAL RFAC, TX1")
        Check_OPC(Callbox)

    Callbox.write(f"SOUR:GPRF:GEN1:LIST OFF")
    Check_OPC(Callbox)
    Callbox.write(f"SOUR:GPRF:GEN1:RFS:EATT 0.000000")
    Check_OPC(Callbox)
    Callbox.write(f"SOUR:GPRF:GEN1:BBM ARB")
    Check_OPC(Callbox)

    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        if band in [38, 39, 40, 41]:
            if bandwidth == 10:
                Callbox.write(
                    f"SOUR:GPRF:GEN1:ARB:FILE"
                    f" 'C:\CMW100_WV\SMU_NodeB_Ant0_LTE_SENS_{bandwidth:02d}MHz_TDD_CFG1_SF_CFG4_SIMO_woCIF_AGL8_RC.wv'"
                )
                Check_OPC(Callbox)
            else:
                Callbox.write(
                    f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_Ant0_TDD_FULL_{BW_number+1:02d}.wv'"
                )
                Check_OPC(Callbox)
        else:
            Callbox.write(
                f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_Ant0_FRC_{bandwidth:02d}MHz.wv'"
            )
            Check_OPC(Callbox)

    elif (Equipment == "CMW") & (Equip == "GPIB0::20::INSTR"):
        if band in [38, 39, 40, 41]:
            if bandwidth == 10:
                Callbox.write(
                    f"SOUR:GPRF:GEN1:ARB:FILE 'D:\SMU_NodeB_Ant0_LTE_SENS_{bandwidth:02d}MHz_TDD_CFG1_SF_CFG4_SIMO_woCIF_AGL8_RC.wv'"
                )
                Check_OPC(Callbox)
            else:
                Callbox.write(
                    f"SOUR:GPRF:GEN1:ARB:FILE 'D:\SMU_NodeB_Ant0_TDD_FULL_{BW_number+1:02d}.wv'"
                )
                Check_OPC(Callbox)
        else:
            Callbox.write(
                f"SOUR:GPRF:GEN1:ARB:FILE 'D:\SMU_NodeB_Ant0_FRC_{bandwidth:02d}MHz.wv'"
            )
            Check_OPC(Callbox)

    word = "SOUR:GPRF:GEN1:ARB:FILE?"
    Ask_query(Callbox, text_area, word, word)

    Callbox.write(f"SOUR:GPRF:GEN1:RFS:FREQ {rxfreq}KHz")
    Callbox.write(f"SOUR:GPRF:GEN1:RFS:LEV -70.000000")

    # Sig gen on
    Callbox.write("SOUR:GPRF:GEN1:STAT ON")
    Check_OPC(Callbox)

    word = "SOUR:GPRF:GEN1:STAT?"  # sig gen on check
    while True:
        response = Callbox.query(f"{word}")
        time.sleep(0.1)
        if response == "ON\n":
            break
    Ask_query(Callbox, text_area, word, word)
    # RX Sync는 Main / Sub 상관없이 동작
    # AT+LSYNC = Main, RX Path, Frequency
    # Main : 0, Main : 0, Frequency
    # CA#1 : 1,  4RX : 1, Frequency
    # CA#2 : 2
    # CA#3 : 3
    response = dut.at_write(f"AT+LSYNC=0,0,{rxfreq}")
    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)

    response = dut.at_write(
        f"AT+LTXSENDREQ={path_number},{BW_number},{txfreq},{PRB},0,0,2,1,23"
    )

    text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
    text_area.see(tk.END)

    Callbox.write("*CLS")

    if band in [38, 39, 40, 41]:
        Callbox.write("CONF:LTE:MEAS:DMODe TDD")
        Check_OPC(Callbox)
    else:
        Callbox.write("CONF:LTE:MEAS:DMODe FDD")
        Check_OPC(Callbox)
    # time.sleep(0.1)
    Callbox.write(f"CONF:LTE:MEAS:BAND OB{band}")
    Callbox.write(f"CONF:LTE:MEAS:RFS:FREQ {txfreq}KHz")
    Check_OPC(Callbox)
    Callbox.write(f"CONF:LTE:MEAS:MEV:CBAN B{bandwidth*10:03d}")
    Callbox.write("CONF:LTE:MEAS:MEV:MOD:MSCH QPSK")
    Callbox.write(f"CONF:LTE:MEAS:MEV:RBAL:NRB {PRB}")
    Callbox.write("CONF:LTE:MEAS:MEV:RBAL:ORB 0")
    Callbox.write("CONF:LTE:MEAS:MEV:CPR NORM")
    Callbox.write("CONF:LTE:MEAS:MEV:PLC 0")
    Callbox.write("CONF:LTE:MEAS:MEV:DSSP 0")
    Callbox.write("CONF:LTE:MEAS:MEV:RBAL:AUTO OFF")
    Callbox.write("CONF:LTE:MEAS:MEV:MOEX ON")

    Set_limit_mask(Callbox, "LTE", bandwidth)

    Callbox.write("CONFigure:LTE:MEAS:MEValuation:MSLot ALL")
    Callbox.write("CONF:LTE:MEAS:RFS:UMAR 10.000000")
    Callbox.write("CONF:LTE:MEAS:RFS:ENP 28.00")

    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        Callbox.write("ROUT:LTE:MEAS:SCEN:SAL R11, RX1")  ##
    elif (Equipment == "CMW") & (Equip == "GPIB0::20::INSTR"):
        Callbox.write("ROUT:LTE:MEAS:SCEN:SAL RFAC, RX1")

    Callbox.write("CONF:LTE:MEAS:RFS:UMAR 10.000000")  # User Margin
    Callbox.write("CONF:LTE:MEAS:MEV:RBAL:AUTO ON")
    Callbox.write("CONF:LTE:MEAS:MEV:SCO:MOD 5")

    Callbox.write("CONF:LTE:MEAS:MEV:SCO:SPEC:ACLR 5")
    Callbox.write("CONF:LTE:MEAS:MEV:SCO:SPEC:SEM 5")

    Callbox.write("TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
    Callbox.write("TRIG:LTE:MEAS:MEV:THR -20.0")
    Callbox.write("CONF:LTE:MEAS:MEV:REP SING")
    # EVM, MagnitudeError, PhaseError, InbandEmissions, EVMversusC, IQ, EquSpecFlatness, TXMeasurement, SpecEmMask, ACLR, RBAllocTable, PowerMonitor, BLER, PowerDynamics
    Callbox.write(
        "CONF:LTE:MEAS:MEV:RES:ALL OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, ON, OFF, OFF, OFF, OFF"
    )
    Check_OPC(Callbox)
    Callbox.write("CONF:LTE:MEAS:MEV:MSUB 2, 10, 0")
    Callbox.write("CONF:LTE:MEAS:SCEN:ACT SAL")
    Callbox.write("CONF:LTE:MEAS:RFS:EATT 0.000000")
    Check_OPC(Callbox)

    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        Callbox.write("ROUT:GPRF:MEAS:SCEN:SAL R11, RX1")  ##
        Callbox.write("ROUT:LTE:MEAS:SCEN:SAL R11, RX1")  ##
    elif (Equipment == "CMW") & (Equip == "GPIB0::20::INSTR"):
        Callbox.write("ROUT:GPRF:MEAS:SCEN:SAL RFAC, RX1")
        Callbox.write("ROUT:GPRF:GEN:SCEN:SAL RFAC, TX1")
        Callbox.write("CONF:GPRF:MEAS:POW:SCO 2")
        Callbox.write("CONF:GPRF:MEAS:POW:REP SING")
        Callbox.write("CONF:GPRF:MEAS:POW:LIST OFF")
        Callbox.write("TRIGger:GPRF:MEAS:POWer:SOURce 'Free Run'")
        Callbox.write("CONF:GPRF:MEAS:POW:TRIG:SLOP REDG")
        Callbox.write("CONF:GPRF:MEAS:POW:SLEN 5.0e-3")
        Callbox.write("CONF:GPRF:MEAS:POW:MLEN 8.0e-4")
        Callbox.write("TRIGger:GPRF:MEAS:POWer:OFFSet 2.1E-3")
        Callbox.write("TRIG:GPRF:MEAS:POW:MODE ONCE")


def Nonsig_nr_tx_measure_setting(
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
):
    Equipment = Callbox.query("*IDN?").split(",")[1]

    Callbox.write(f"ROUT:GPRF:GEN:SCEN:SAL R118, TX1")
    Callbox.write(
        f"CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF"
    )
    Check_OPC(Callbox)
    Callbox.write(f"SOUR:GPRF:GEN1:LIST OFF")
    Check_OPC(Callbox)
    Callbox.write(f"SOUR:GPRF:GEN1:RFS:EATT 0.000000")
    Check_OPC(Callbox)
    Callbox.write(f"SOUR:GPRF:GEN1:BBM ARB")
    Check_OPC(Callbox)
    Callbox.write(f"CONFigure:NRSub:MEAS:ULDL:PERiodicity MS10")
    Check_OPC(Callbox)

    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        if Testband in [38, 40, 41, 77, 78]:
            Callbox.write(
                "SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_NR_Ant0_NR_10MHz_SCS30_TDD_Sens_MCS0_rescale.wv'"
            )
            Check_OPC(Callbox)
        else:
            Callbox.write(
                "SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_NR_Ant0_LTE_NR_10MHz_SCS15_FDD_Sens_MCS_0.wv'"
            )
            Check_OPC(Callbox)

    word = "SOUR:GPRF:GEN1:ARB:FILE?"
    Ask_query(Callbox, text_area, word, word)

    Callbox.write(f"SOUR:GPRF:GEN1:RFS:FREQ {rxfreq}KHz")
    Callbox.write(f"SOUR:GPRF:GEN1:RFS:LEV -70.000000")

    # Sig gen on
    Callbox.write("SOUR:GPRF:GEN1:STAT ON")
    Check_OPC(Callbox)

    word = "SOUR:GPRF:GEN1:STAT?"  # sig gen on check
    while True:
        response = Callbox.query(f"{word}")
        time.sleep(0.1)
        if response == "ON\n":
            break
    Ask_query(Callbox, text_area, word, word)

    # AT+NRFSYNC = Main, RX Path, SCS, BW, 256QAM, Frequency
    # Main : 0, Main : 0, SCS 15 : 0,  5M : 0, QPSK : 0, Frequency
    # CA#1 : 1,  4RX : 1, SCS 30 : 1, 10M : 1, 256Q : 3, Frequency
    # CA#2 : 2,  6RX : 2,
    # CA#3 : 3

    # AT+NTXSENDREQ=TX Path, Frequency, BW, SCS, RBSize, RBOffset, MCS, Waveform type, TX Level
    # Main : 0, Frequency,  5M : 0, SCS 15 : 0, RBSize, RBOffset, QPSK : 2, DFT-S : 0, TX Level
    #  Sub : 1, Frequency, 10M : 1, SCS 30 : 1, RBSize, RBOffset, 256Q : 8,    CP : 1, TX Level
    # MIMO : 20
    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        if Testband in [38, 40, 41, 77, 78]:  # SCS 30
            response = dut.at_write(f"AT+NRFSYNC=0,0,1,{BW_number},0,{rxfreq}")
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            text_area.see(tk.END)
            response = dut.at_write(
                f"AT+NTXSENDREQ={path_number},{txfreq},{BW_number},1,{PRB},{infull_offset},2,0,23"
            )
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            text_area.see(tk.END)
            Callbox.write("CONF:NRS:MEAS:MEV:DMODe TDD")
            Check_OPC(Callbox)
            scs = 30
        else:  # SCS 15
            response = dut.at_write(f"AT+NRFSYNC=0,0,0,{BW_number},0,{rxfreq}")
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            text_area.see(tk.END)
            response = dut.at_write(
                f"AT+NTXSENDREQ={path_number},{txfreq},{BW_number},0,{PRB},{infull_offset},2,0,23"
            )
            text_area.insert(tk.END, f"{response[0]:<40}\t|\t{response[2::2]}\n")
            text_area.see(tk.END)
            Callbox.write("CONF:NRS:MEAS:MEV:DMODe FDD")
            Check_OPC(Callbox)
            scs = 15
    # time.sleep(0.1)
    Callbox.write(f"CONF:NRS:MEAS:BAND OB{Testband}")
    Callbox.write(f"CONF:NRS:MEAS:RFS:FREQ {txfreq}KHz")
    Check_OPC(Callbox)
    Callbox.write("CONF:NRS:MEAS:MEV:PLC 0")
    Callbox.write("CONF:NRS:MEAS:MEV:MOEX ON")
    Callbox.write(f"CONF:NRS:MEAS:MEV:BWC S{scs}K, B{bandwidth:03d}")

    Set_limit_mask(Callbox, "NR", bandwidth)

    Callbox.write("CONFigure:NRSub:MEASurement:MEValuation:DFTPrecoding ON")

    if (Equipment == "CMW") & (Equip == "TCPIP::127.0.0.1::INSTR"):
        if Testband in [38, 40, 41, 77, 78]:  # SCS 30
            Callbox.write(
                f"CONFigure:NRSub:MEASurement:MEValuation:PUSChconfig QPSK,A,OFF,{PRB},{infull_offset},14,0,T1,SING,0,2"
            )
        else:
            Callbox.write(
                f"CONFigure:NRSub:MEASurement:MEValuation:PUSChconfig QPSK,A,OFF,{PRB},{infull_offset},14,0,T1,SING,0,2"
            )

    Callbox.write("CONFigure:NRSub:MEASurement:MEValuation:PCOMp OFF, 6000E+6")
    Check_OPC(Callbox)
    Callbox.write("CONFigure:NRSub:MEASurement:MEValuation:REPetition SING")
    Callbox.write("CONFigure:NRSub:MEASurement:MEValuation:PLCid 0")
    Callbox.write("CONFigure:NRSub:MEASurement:MEValuation:CTYPe PUSC")
    Callbox.write("CONF:NRS:MEAS:ULDL:PER MS25")
    Callbox.write(f"CONF:NRS:MEAS:ULDL:PATT S{scs}K, 3,0,1,14")
    Callbox.write("CONFigure:NRSub:MEASurement:MEValuation:MSLot ALL")
    Callbox.write("ROUT:NRS:MEAS:SCEN:SAL R11, RX1")
    Callbox.write("CONF:NRS:MEAS:RFS:ENP 28.00")
    Callbox.write("CONF:NRS:MEAS:RFS:UMAR 10.000000")
    Callbox.write("CONF:NRS:MEAS:MEV:SCO:MOD 5")
    Callbox.write("CONF:NRS:MEAS:MEV:SCO:SPEC:ACLR 5")
    Callbox.write("CONF:NRS:MEAS:MEV:SCO:SPEC:SEM 5")
    Callbox.write("TRIG:NRS:MEAS:MEV:SOUR 'GPRF GEN1: Restart Marker'")
    Callbox.write("TRIG:NRS:MEAS:MEV:THR -20.0")
    Callbox.write("CONF:NRS:MEAS:MEV:REP SING")
    # EVM, MagnitudeError, PhaseError, InbandEmissions, EVMversusC, IQ, EquSpecFlatness, TXMeasurement, SpecEmMask, ACLR, PowerMonitor, PowerDynamics, TxPower
    Callbox.write(
        "CONF:NRS:MEAS:MEV:RES:ALL OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF"
    )
    Callbox.write("CONF:NRS:MEAS:MEV:RES:ACLR ON")
    Callbox.write("CONF:NRS:MEAS:MEV:NSUB 10")
    Callbox.write("CONFigure:NRSub:MEASurement:MEValuation:MSLot ALL")
    Callbox.write("CONF:NRS:MEAS:SCEN:ACT SAL")
    Callbox.write("CONF:NRS:MEAS:RFS:EATT 0.000000")
    Check_OPC(Callbox)
    Callbox.write("ROUT:GPRF:MEAS:SCEN:SAL R11, RX1")
    Check_OPC(Callbox)
    Callbox.write("ROUT:NRS:MEAS:SCEN:SAL R11, RX1")
    Check_OPC(Callbox)
    Callbox.write("INIT:NRS:MEAS:MEV")
    Check_OPC(Callbox)
