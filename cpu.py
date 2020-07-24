import sys


"""STEP 4: Add the `HLT` instruction definition to `cpu.py` so that you can refer to it by
name instead of by numeric value. """
HLT = 0b00000001

"""STEP 5: Add the `LDI` instruction definition to `cpu.py` so that you can refer to it by
name instead of by numeric value. """
LDI = 0b10000010

"""STEP 6: Add the `PRN` instruction"""
PRN = 0b01000111

"""STEP 8: Implement a Multiply and Print the Result"""
MUL = 0b10100010

"""Step 10: Implement System Stack"""
PUSH = 0b01000101
POP = 0b01000110

''' ### SPRINT CHALLENGE ### '''
# Add the CMP instruction and equal flag to your LS-8.
#  Add the JMP instruction.
#  Add the JEQ and JNE instructions.
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:

    """STEP 1: Add the constructor to `cpu.py`"""

    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # registers
        self.ram = [0] * 256  # memory
        self.pc = 0  # pc
        self.SP = 7  # stack pointer
        self.FL = 0

    # `ram_write()` should accept a value to write, and the address to write it to.
    def ram_read(self, MAR):
        return self.ram[MAR]

    # `ram_read()` should accept the address to read and return the value stored there.
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) < 2:
            print("Please pass in two file names")

        file_name = sys.argv[1]

        try:
            with open(file_name) as f:
                for line in f:
                    # ignore whitespace + comments
                    split_line = line.split('#')[0]
                    command = split_line.strip()
                    if command == '':
                        continue

                    # use 2 for base 2 for binary
                    num = int(command, 2)

                    # store in memory
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

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
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    """STEP 3: Implement the core of `CPU`'s `run()` method"""

    def run(self):
        """Run the CPU."""
        # load program into memory
        self.load()

        while self.ram[self.pc] != HLT:
            IR = self.ram[self.pc]  # command

            # read bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            if IR == LDI:  # SAVE
                # save new value in specified register
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:  # PRINT REG
                # Print numeric value stored in the given register.
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:  # MULTIPLY
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:  # PUSH
                # get the register number
                register = operand_a

                # decrement register number
                self.reg[self.SP] -= 1

                # get the value from the given register
                value = self.reg[register]

                # put the value at the stack pointer address
                stack_pointer = self.reg[self.SP]
                self.ram[stack_pointer] = value

                # increment the PC
                self.pc += 2

            elif IR == POP:  # POP
                # get the register number
                register = operand_a

                # use stack pointer to get the value
                stack_pointer = self.reg[self.SP]
                value = self.ram[stack_pointer]

                # put the value into the given register
                self.reg[register] = value

                # increment our stack pointer
                self.reg[self.SP] += 1

                # increment our PC
                self.pc += 2

            # CMP - Compare the values in two registers.
            elif IR == CMP:
                if (self.reg[operand_a] == self.reg[operand_b]) == True:
                    self.FL = 1

                self.pc += 3

            # JMP - Jump to the address stored in the given register.  Set the PC to the address stored in the given register.
            elif IR == JMP:
                self.pc = self.reg[operand_a]

            # JEQ - If equal flag is set (true), jump to the address stored in the given register.
            elif IR == JEQ:
                if self.FL == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            # JNE - If E flag is clear (false, 0), jump to the address stored in the given register.
            elif IR == JNE:
                if self.FL == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

        sys.exit()
