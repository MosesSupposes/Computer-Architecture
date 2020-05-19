"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    commands = {
       "HLT": 0b01,
       "LDI": 0b10000010,
       "PRN": 0b01000111,
       "MUL": 0b10100100
    }

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 
        self.reg = [0] * 8
        self.pc = 0

    def load(self, program):
        """Load a program into memory."""
        address = 0
        try: 
            with open(program) as p:
                for instruction in p:
                    if instruction.strip().split("#")[0] != "":
                        self.ram_write(address, int(instruction.split("#")[0], 2))
                        address += 1
        except Exception:
            raise ValueError("Invalid file path.")

    def ram_read(self, address): 
        try: 
            return self.ram[address]
        except IndexError:
            raise ValueError("The address of value  " + str(address) +  " isn't a valid location in memory")
    
    def ram_write(self, address, value):
        self.ram[address] = value
        return value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        IR = None
        while IR != self.commands["HLT"]:
            IR = self.ram_read(self.pc)

            if IR == self.commands["HLT"]:
                self.pc += 1
                break

            elif IR == self.commands["LDI"]:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                self.pc += 3
            
            elif IR == self.commands["PRN"]:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2

            elif IR == self.commands["MUL"]:
                self.alu("MUL", self.reg[self.ram[self.pc + 1]], self.reg[self.ram[self.pc + 2]])
                self.pc += 3

            else:
                raise Exception(f"Invalid Command: {IR}")
        
        # Reset the program counter
        self.pc = 0
