import pyvisa


def run_main_logic(bands, frequency, cmw_ip):
    print(f"Running main logic with Bands: {bands} and Frequency: {frequency} MHz")

    try:
        # VISA connections
        timeout = 1000
        rm = pyvisa.ResourceManager()
        # = "192.10.11.12"  # Replace with a dynamic value if needed
        cmw = rm.open_resource(f"TCPIP::{cmw_ip}::INSTR")
        print(cmw)
        cmw.timeout = timeout

        # Send SCPI commands to configure the bands and frequency
        cmw.write("*RST; *OPC?; *CLS; *OPC")
        cmw.write(f"FREQ:CENT {frequency}MHZ")
        for band in bands:
            # print("going for measurment check")
            cmw.write("ROUTe:GPRF:MEAS:SCENario:SALone R12, RX11")  # RXConnector & RFConverter
            cmw.write(f"CONFigure:GPRF:MEAS:RFSettings:FREQuency {frequency}")
            cmw.write(f"CONFigure:GPRF:MEAS:RFSettings:EATTenuation 1.0")
            cmw.write("CONFigure:GPRF:MEAS:POWer:MODE POWer")
            cmw.write("CONFigure:GPRF:MEAS:POWer:FILTer:TYPE GAUSs")
            cmw.write(f"CONFigure:GPRF:MEAS:POWer:FILTer:GAUSs:BWIDth 1E+4")
            cmw.write(f"CONFigure:GPRF:MEAS:RFSettings:ENPower 0.0")
            cmw.write(f"CONFigure:GPRF:MEAS:RFSettings:UMARgin 0.0")
            cmw.timeout = timeout

            cmw.write("INITiate:GPRF:MEAS:POWer")
            # print("Measurment setting POWer", cmw.query("SYST:ERR?"))  # Ensure no errors occurred

            cmw.query("*OPC?")
            # print(cmw.query("FETCh:GPRF:MEAS:POWer:AVERage?"))

            raw_power = cmw.query("FETCh:GPRF:MEAS:POWer:AVERage?").strip().split(',')
            cmw.timeout = timeout
            # print("Query issue:", cmw.query("SYST:ERR?"))  # Ensure no errors occurred
            # print(raw_power)

            cmw.write("ABORt:GPRF:MEAS:POWer")
            cmw.timeout = timeout

            cmw.write("SOURce:GPRF:GEN1:STATe OFF")
            cmw.timeout = timeout

            received_power = float(raw_power[1])
            cmw.write(f"BAND:SELECT {band}")  # Assuming `BAND:SELECT` is the SCPI command
            cmw.write("INITiate:GPRF:MEAS:SPECtrum")
            cmw.query("FETCh:GPRF:MEAS1:SPECtrum:MAXimum:CURRent?")
            cmw.query("FETCh:GPRF:MEAS1:SPECtrum:MAXimum:AVERage?")
            cmw.query("FETCh:GPRF:MEAS1:SPECtrum:MAXimum:MAXimum?")
            cmw.query("FETCh:GPRF:MEAS<i>:SPECtrum:MAXimum:MINimum?")
            cmw.query("READ:GPRF:MEAS<i>:SPECtrum:MAXimum:CURRent?")
            cmw.query("READ:GPRF:MEAS<i>:SPECtrum:MAXimum:AVERage?")
            cmw.query("READ:GPRF:MEAS<i>:SPECtrum:MAXimum:MAXimum?")
            cmw.query("READ:GPRF:MEAS<i>:SPECtrum:MAXimum:MINimum?")

            cmw.query("FETCh: GPRF:MEAS: SPECtrum:REFMarker: SPEak? AVERage, AVERage")
            cmw.query("FETCh: GPRF:MEAS: SPECtrum:REFMarker: SPEak? RMS, AVERage")
            cmw.query("FETCh: GPRF:MEAS: SPECtrum:REFMarker: SPEak? SAMPle, AVERage")
            cmw.query("FETCh: GPRF:MEAS: SPECtrum:REFMarker: SPEak? MINPeak, AVERage")
            cmw.query("FETCh: GPRF:MEAS: SPECtrum:REFMarker: SPEak? MAXPeak, AVERage")
        print("Instrument configured successfully!")
    except Exception as e:
        print(f"Error in main logic: {e}")


def main():
    print("This is a placeholder for main.py logic.")
    # Add standalone testing logic here if needed


if __name__ == "__main__":
    main()
