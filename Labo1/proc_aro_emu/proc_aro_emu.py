# Allow simple graphical interface
import PySimpleGUI as sg
# Allow file management
import os.path
# Time
import time

# Create left column
left_column = [
    [
        sg.Text("Raw File"),
        sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
        sg.FileBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=False, size=(40, 20), key="-FILE CONTENT-"
        )
    ],
    [
        sg.Button("Execute instruction", key="-EXECUTE-")
    ]
]

# Create left column
right_column = [ 
    [sg.Text("Select your raw file", size=(40, 1), key="-INFO-")],
    [sg.Text("", size=(40, 1), key="-INSTR-")],
    [sg.Text("", size=(40, 1), key="-R0-")],
    [sg.Text("", size=(40, 1), key="-R1-")],
    [sg.Text("", size=(40, 1), key="-R2-")],
    [sg.Text("", size=(40, 1), key="-R3-")],
    [sg.Text("", size=(40, 1), key="-R4-")],
    [sg.Text("", size=(40, 1), key="-R5-")],
    [sg.Text("", size=(40, 1), key="-R6-")],
    [sg.Text("", size=(40, 1), key="-R7-")]    
]

# Create main layout
layout = [
    [
        sg.Column(left_column),
        sg.VSeperator(),
        sg.Column(right_column),
    ]
   
]

# Instanciate window and make in visible
window = sg.Window("ARO - Instructions", layout)

# Custom values
ready_to_run = False
last_instruction = False
current_instruction = 0
registers = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
]
          

# Run the Event Loop
while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Verify user selected a file
    if event == "-FILE-":
        # Init values
        ready_to_run = False
        last_instruction = False
        current_instruction = 0
        registers = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ]
        # Define the filename
        #print("File chosen is " + values["-FILE-"])
        file_loc = open(values["-FILE-"], "r")
        temp_content = file_loc.read()
        temp_content = temp_content.split("\n")
        file_content = []
        for i in range(7,len(temp_content)-1):
            current_line = temp_content[i] # Extract desired line
            current_line = current_line.split(" ")
            for j in range(0, len(current_line)):
                file_content.append(current_line[j])
        #Clean
        file_content = [x for x in file_content if x!= '']
        print(file_content)
        #print(file_content)
        window["-FILE CONTENT-"].update(file_content)
        # Remove text 
        window["-INFO-"].update("")
        # Plot register state
        window["-INSTR-"].update("INSTR = 0x" + str(file_content[current_instruction]))
        window["-R0-"].update("R0       = " + str(registers[0]))
        window["-R1-"].update("R1       = " + str(registers[1]))
        window["-R2-"].update("R2       = " + str(registers[2]))
        window["-R3-"].update("R3       = " + str(registers[3]))
        window["-R4-"].update("R4       = " + str(registers[4]))
        window["-R5-"].update("R5       = " + str(registers[5]))
        window["-R6-"].update("R6 (LR)  = " + str(registers[6]))
        window["-R7-"].update("R7 (PC)  = " + str(registers[7]))
        # Set ready
        ready_to_run = True
    elif event == "-EXECUTE-":
        if ready_to_run == True and last_instruction == False:
            # Execute command to update registers
            instr_bin = bin(int(file_content[current_instruction], 16))[2:].zfill(16)
            # Decoder of instruction (cf : ARMM7-TDMI-manual_pt3.pdf)
            if instr_bin[0:5] == "00000":
                print("move shifted register - LSL")
                Offset5 = int(instr_bin[5:10], 2)
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rs] * 2**Offset5
            elif instr_bin[0:5] == "00001":
                print("move shifted register - LSR")
                Offset5 = int(instr_bin[5:10], 2)
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = int(registers[Rs] / 2**Offset5 )
            elif instr_bin[0:5] == "00010":
                print("move shifted register - ASR (not tested)")
                Offset5 = int(instr_bin[5:10], 2)
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = int(registers[Rs] / 2**Offset5 )
            elif instr_bin[0:7] == "0001100":
                print("Add/substract - Add - Register operand")
                Rn = int(instr_bin[7:10], 2)
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rs] + registers[Rn]
            elif instr_bin[0:7] == "0001101":
                print("Add/substract - Sub - Register operand")
                Rn = int(instr_bin[7:10], 2)
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rs] - registers[Rn]
            elif instr_bin[0:7] == "0001110":
                print("Add/substract - Add - Immediate operand")
                Offset3 = int(instr_bin[7:10], 2)
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rs] + Offset3
            elif instr_bin[0:7] == "0001111":
                print("Add/substract - Sub - Immediate operand")
                Offset3 = int(instr_bin[7:10], 2)
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rs] - Offset3
            elif instr_bin[0:5] == "00100":
                print("move/compare/add/substract immediate - MOV")
                Rd = int(instr_bin[5:8], 2)
                Offset8 = int(instr_bin[8:16], 2)
                registers[Rd] = Offset8
            elif instr_bin[0:5] == "00101":
                print("move/compare/add/substract immediate - CMP (Not implemented)")
            elif instr_bin[0:5] == "00110":
                print("move/compare/add/substract immediate - ADD")
                Rd = int(instr_bin[5:8], 2)
                Offset8 = int(instr_bin[8:16], 2)
                registers[Rd] += Offset8
            elif instr_bin[0:5] == "00111":
                print("move/compare/add/substract immediate - SUB")
                Rd = int(instr_bin[5:8], 2)
                Offset8 = int(instr_bin[8:16], 2)
                registers[Rd] -= Offset8
            elif instr_bin[0:10] == "0100000000":
                print("ALU operations - AND")
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rd] and registers[Rs]
            elif instr_bin[0:10] == "0100000001":
                print("ALU operations - EOR")
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rd] ^ registers[Rs]
            elif instr_bin[0:10] == "0100000010":
                print("ALU operations - LSL")
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = registers[Rd] * 2**registers[Rs]
            elif instr_bin[0:10] == "0100000011":
                print("ALU operations - LSR")
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = int(registers[Rd] / 2**registers[Rs])
            elif instr_bin[0:10] == "0100000100":
                print("ALU operations - ASR (Not tested)")
                Rs = int(instr_bin[10:13], 2)
                Rd = int(instr_bin[13:16], 2)
                registers[Rd] = int(registers[Rd] / 2**registers[Rs])
            elif instr_bin[0:10] == "0100000101":
                print("ALU operations - ADC (Not implemented)")
            elif instr_bin[0:10] == "0100000110":
                print("ALU operations - SBC (Not implemented)")
            elif instr_bin[0:10] == "0100000111":
                print("ALU operations - ROR (Not implemented)")
            elif instr_bin[0:10] == "0100001000":
                print("ALU operations - TST (Not implemented)")
            elif instr_bin[0:10] == "0100001001":
                print("ALU operations - NEG (Not implemented)")
            elif instr_bin[0:10] == "0100001010":
                print("ALU operations - CMP (Not implemented)")
            elif instr_bin[0:10] == "0100001011":
                print("ALU operations - CMN (Not implemented)")
            elif instr_bin[0:10] == "0100001100":
                print("ALU operations - ORR (Not implemented)")
            elif instr_bin[0:10] == "0100001101":
                print("ALU operations - MUL (Not implemented)")
            elif instr_bin[0:10] == "0100001110":
                print("ALU operations - BIC (Not implemented)")
            elif instr_bin[0:10] == "0100001111":
                print("ALU operations - MVN (Not implemented)")
            elif instr_bin[0:6] == "010001":
                print("Hi register operations/branch exchange (Not implemented)")                
            elif instr_bin[0:5] == "01001":
                print("PC-relative load (Not implemented)")                                
            elif instr_bin[0:7] == "0101000":
                print("Load/store with register offset - STORE Word (Not implemented)")      
            elif instr_bin[0:7] == "0101001":
                print("Load/store with register offset - STORE Byte (Not implemented)")      
            elif instr_bin[0:7] == "0101010":
                print("Load/store with register offset - LOAD Word (Not implemented)")      
            elif instr_bin[0:7] == "0101011":
                print("Load/store with register offset - LOAD Byte (Not implemented)")      
            elif instr_bin[0:7] == "0101001":
                print("Load/store sign-extended byte/halfword - Store halfword (Not implemented)")                                                                                
            elif instr_bin[0:7] == "0101101":
                print("Load/store sign-extended byte/halfword - Load halfword (Not implemented)")                                                                                
            elif instr_bin[0:7] == "0101011":
                print("Load/store sign-extended byte/halfword - Load sign-extended byte (Not implemented)")                                                                                
            elif instr_bin[0:7] == "0101111":
                print("Load/store sign-extended byte/halfword - Store sign-extended byte (Not implemented)")                                                                                
            elif instr_bin[0:5] == "01100":
                print("Load/store with immediate offset - Store Word (Not implemented)")                                                                               
            elif instr_bin[0:5] == "01101":
                print("Load/store with immediate offset - Load Word (Not implemented)")                                                                               
            elif instr_bin[0:5] == "01110":
                print("Load/store with immediate offset - Store Byte (Not implemented)")                                                                               
            elif instr_bin[0:5] == "01111":
                print("Load/store with immediate offset - Load Byte (Not implemented)")                                                                              
            elif instr_bin[0:5] == "10000":
                print("Load/store halfword - Store (Not implemented)")                                                                              
            elif instr_bin[0:5] == "10001":
                print("Load/store halfword - Load (Not implemented)")                                                                              
            elif instr_bin[0:5] == "10010":
                print("SP-relative load/store - Store (Not implemented)")                                                                          
            elif instr_bin[0:5] == "10011":
                print("SP-relative load/store - Load (Not implemented)")                                                                         
            elif instr_bin[0:5] == "10100":
                print("Load address - PC (Not implemented)")                                                                         
            elif instr_bin[0:5] == "10101":
                print("Load address - SP (Not implemented)")                                                                         
            elif instr_bin[0:9] == "101100000":
                print("Add offset to stack pointer - Offset positive (Not implemented)")                                             
            elif instr_bin[0:9] == "101100001":
                print("Add offset to stack pointer - Offset negative (Not implemented)")                                             
            elif instr_bin[0:8] == "10110100":
                print("Push/pop registers - Push - Do not store LR/load PC (Not implemented)")                                       
            elif instr_bin[0:8] == "10110101":
                print("Push/pop registers - Push - Store LR/load PC (Not implemented)")                                       
            elif instr_bin[0:8] == "10111100":
                print("Push/pop registers - Pop - Do not store LR/load PC (Not implemented)")                                       
            elif instr_bin[0:8] == "10111101":
                print("Push/pop registers - Pop - Store LR/load PC (Not implemented)")                                             
            elif instr_bin[0:5] == "11000":
                print("Multiple load/store - Store (Not implemented)")                                                   
            elif instr_bin[0:5] == "11001":
                print("Multiple load/store - Load (Not implemented)")                                                    
            elif instr_bin[0:8] == "11010000":
                print("Conditional branch - BEQ (Not implemented)")                                                      
            elif instr_bin[0:8] == "11010001":
                print("Conditional branch - BNE (Not implemented)")                                                      
            elif instr_bin[0:8] == "11010010":
                print("Conditional branch - BCS (Not implemented)")                                                      
            elif instr_bin[0:8] == "11010011":
                print("Conditional branch - BCC (Not implemented)")                                                      
            elif instr_bin[0:8] == "11010100":
                print("Conditional branch - BMI (Not implemented)")                                                      
            elif instr_bin[0:8] == "11010101":
                print("Conditional branch - BPL (Not implemented)")                                                      
            elif instr_bin[0:8] == "11010110":
                print("Conditional branch - BVS (Not implemented)")                                                      
            elif instr_bin[0:8] == "11010111":
                print("Conditional branch - BVC (Not implemented)")                                                      
            elif instr_bin[0:8] == "11011000":
                print("Conditional branch - BHI (Not implemented)")                                                      
            elif instr_bin[0:8] == "11011001":
                print("Conditional branch - BLS (Not implemented)")                                                      
            elif instr_bin[0:8] == "11011010":
                print("Conditional branch - BGE (Not implemented)")                                                      
            elif instr_bin[0:8] == "11011011":
                print("Conditional branch - BLT (Not implemented)")                                                      
            elif instr_bin[0:8] == "11011100":
                print("Conditional branch - BGT (Not implemented)")                                                      
            elif instr_bin[0:8] == "11011101":
                print("Conditional branch - BLE (Not implemented)")                                                      
            elif instr_bin[0:8] == "11011111":
                print("Software interrupt (Not implemented)")                                                            
            elif instr_bin[0:5] == "11100":
                print("Unconditionnal branch (Not implemented)")                                                         
            elif instr_bin[0:5] == "11110":
                print("Long branch with link - Offset high (Not implemented)")                                           
            elif instr_bin[0:5] == "11111":
                print("Long branch with link - Offset low (Not implemented)")      
            else:
                print("Unknown/Unsupported instruction : " + str(instr_bin))
                
            # Update printed values
            if current_instruction == len(file_content)-1:
                window["-INSTR-"].update("INSTR = 0x0000 (empty instructions memory)")
                last_instruction = True
            else:
                current_instruction = current_instruction + 1
                window["-INSTR-"].update("INSTR = 0x" + str(file_content[current_instruction]))
            # Update window
            window["-R0-"].update("R0       = " + str(registers[0]))
            window["-R1-"].update("R1       = " + str(registers[1]))
            window["-R2-"].update("R2       = " + str(registers[2]))
            window["-R3-"].update("R3       = " + str(registers[3]))
            window["-R4-"].update("R4       = " + str(registers[4]))
            window["-R5-"].update("R5       = " + str(registers[5]))
            window["-R6-"].update("R6 (LR)  = " + str(registers[6]))
            window["-R7-"].update("R7 (PC)  = " + str(current_instruction*2)) #str(registers[7]))
        else:            
            window["-INFO-"].update("Please select file before running ! ")

# Clean close
print("Closing windows ...")
window.close()
