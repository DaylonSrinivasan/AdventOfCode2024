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
        while self.instruction_ptr < len(self.program) - 1:
            instruction = Computer._get_instruction(int(self.program[self.instruction_ptr]))
            operand = int(self.program[self.instruction_ptr+1])
            self._execute(instruction, operand)
        return ",".join(self.out_buffer)


### Run program ###
computer = Computer()
print(computer.run())




