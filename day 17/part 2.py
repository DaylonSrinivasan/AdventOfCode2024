import enum
import math

class Instruction(enum.Enum):
    # Value must be correct opcode specified.
    # i.e., "0" must represent "adv".
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7

class Computer:
    A: int = 62769524
    B: int = 0
    C: int = 0
    program: str = "2417750340175530"
    instruction_ptr = 0
    out_buffer: list[str] = []
    
    def _get_instruction(x: int):
        return Instruction(x)

    def _get_combo(self, x: int) -> int:
        if x in range(4):
            return x
        elif x == 4:
            return self.A
        elif x == 5:
            return self.B
        elif x == 6:
            return self.C
        raise "Unexpected combo operand: %s" % x

    def _execute(self, instruction: Instruction, operand: int):
        if instruction == Instruction.adv:
            numerator = self.A
            denominator = 2 ** self._get_combo(operand)
            self.A = math.floor(numerator / denominator)
        elif instruction == Instruction.bxl:
            self.B ^= operand
        elif instruction == Instruction.bst:
            self.B = self._get_combo(operand) % 8
        elif instruction == Instruction.jnz:
            if self.A:
                self.instruction_ptr = operand
                return  # return early to avoid incrementing instruction counter
        elif instruction == Instruction.bxc:
            self.B ^= self.C
        elif instruction == Instruction.out:
            self.out_buffer.append(str(self._get_combo(operand) % 8))
        elif instruction == Instruction.bdv:
            numerator = self.A
            denominator = 2 ** self._get_combo(operand)
            self.B = math.floor(numerator / denominator)
        elif instruction == Instruction.cdv:
            numerator = self.A
            denominator = 2 ** self._get_combo(operand)
            self.C = math.floor(numerator / denominator)
        self.instruction_ptr += 2


    def run(self) -> str:
        self.instruction_ptr = 0
        while self.instruction_ptr < len(self.program) - 1:
            instruction = Computer._get_instruction(int(self.program[self.instruction_ptr]))
            operand = int(self.program[self.instruction_ptr+1])
            self._execute(instruction, operand)
        output = "".join(self.out_buffer)
        self.out_buffer = []
        return output

    # Finds the minimum A needed s.t. the program
    # "2417750340175530" outputs "2417750340175530".
    #
    # This program is broken down into the following instructions:
    #.  "24" --> B = A % 8  # get last 3 digits of A, put into B
    #.  "17" --> B = B ^ 7  # flip B
    #.  "75" --> C = A >> B # get (some digits of A)
    #.  "03" --> A = A >> 3 # shift A down by 3
    #.  "40" --> B = B ^ C  # flip with C bits
    #.  "17" --> B = B ^ 7  # flip B
    #.  "55" --> output(B % 8) # output last 3 bits as int
    #.  30" --> go to beginning if A != 0
    #
    # By analyzing this, we realize that we can reverse engineer A by
    # building it up 3 bits at a time. Specifically:
    # 
    # 1. For all possibilities of 3 bits (0..7):
    # Try running the algorithm. If it produces a B value that
    # outputs the last 3 bits, then consider it a possibility.
    # In the end, return the minimum possibility.
    def findA(self) -> str:
        self.A = 0
        a_possibilities = [0]
        for idx in range(len(self.program)):
            possibilities = []
            for a_possibility in a_possibilities:
                for i in range(8):
                    guess = a_possibility * 8 + i
                    self.A = guess
                    output = self.run()
                    if len(output) == idx + 1 and self.program.endswith(output):
                        possibilities.append(guess)
            a_possibilities = possibilities
        return str(min(a_possibilities))
            


    

### Run program ###
computer = Computer()
print(computer.findA())




### Notes ###
#
# instruction:
#.  0: "24" --> B = A % 8  # get last 3 digits of A, put into B
#.  1: "17" --> B = B ^ 7  # flip B
#.  2: "75" --> C = A >> B # get (some digits of A)
#.  3: "03" --> A = A >> 3 # shift A down by 3
#.  4: "40" --> B = B ^ C  # flip with C bits
#.  5: "17" --> B = B ^ 7  # flip B
#.  6 :"55" --> output(B % 8) # output last 3 bits as int
#.  7: "30" --> go to beginning if A != 0
# Final state: A = 0, B = 0, C = 0
#
# Pseudocode of the algorithm:
# pick some 3 digits of A such that:
#   guessB = guessA % 8
#.  guessB = guessB ^ 7
#.  guessC = guessA >> guessB
#.  guessA >>= 3
#.  guessB ^= guessC
#.  guessB ^= 7
# results in guessB = b
# found A, get B and C