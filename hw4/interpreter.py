import argparse
import yaml


MEMORY_SIZE = 2048  # Размер памяти в байтах

class Interpreter:
    def __init__(self, binary_file, result_file, memory_range):
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory_range = memory_range
        self.memory = [0] * MEMORY_SIZE
        self.acc = 0
        
    def check_address(self, addr, operation):
        if not (0 <= addr < MEMORY_SIZE):
            raise ValueError(f"Адрес {addr} выходит за пределы памяти при выполнении {operation}")
    
    def load_program(self):
        with open(self.binary_file, "rb") as file:
            self.program = file.read()

    def execute(self):
        pointer = 0
        while pointer < len(self.program):
            # Получаем opcode из первого байта
            first_byte = self.program[pointer]
            
            if first_byte & 0xF == 0x06:  # LOAD (3 байта)
                B = ((self.program[pointer] & 0xF0) >> 4) | (self.program[pointer + 1] << 4) | \
                    (self.program[pointer + 2] << 12)
                self.acc = B
                print(f"LOAD: введено значение {B}")
                pointer += 3
            
            elif first_byte & 0xF == 0x03:  # READ (3 байта)
                B = ((self.program[pointer] & 0xF0) >> 4) | (self.program[pointer + 1] << 4) | \
                    (self.program[pointer + 2] << 12)
                self.check_address(B, "READ source")
                value = self.acc + B
                self.check_address(value, "READ computed")
                self.acc = self.memory[value]
                print(f"READ: прочитано значение {self.acc}")
                pointer += 3

            elif first_byte & 0xF == 0x00:  # WRITE (4 байта)
                # Декодируем B (адрес) из следующих байтов
                B = ((self.program[pointer] & 0xF0) >> 4) | (self.program[pointer + 1] << 4) | \
                    (self.program[pointer + 2] << 12) | (self.program[pointer + 2] << 16)
                self.check_address(B, "WRITE destination")
                self.memory[B] = self.acc
                print(f"WRITE: записано значение {self.acc}")
                pointer += 4

            elif first_byte & 0xF == 0xD:  # REV (4 байтa)
                # Декодируем B (адрес) из следующих байтов
                B = ((self.program[pointer] & 0xF0) >> 4) | (self.program[pointer + 1] << 4) | \
                    (self.program[pointer + 2] << 12) | (self.program[pointer + 2] << 16)
                
                self.check_address(B, "MIN address")
                
                result = self.acc ^ 255
                print(f"REV: значение {self.acc} перевёрнуто в {result}")
                self.memory[B] = result
                pointer += 4

            else:
                raise ValueError(f"Неизвестная команда: {hex(first_byte)}")
        self.save_results()

    def save_results(self):
        start, end = self.memory_range
        with open(self.result_file, "w", newline="") as file:
            to_yaml = {}
            for addr in range(start, end + 1):
                to_yaml[addr] = self.memory[addr]
            yaml.dump(to_yaml, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Интерпретатор УВМ.")
    parser.add_argument("-i", "--input", required=True, help="Путь к бинарному файлу")
    parser.add_argument("-r", "--result", required=True, help="Путь к файлу результата")
    parser.add_argument("--range", required=True, type=int, nargs=2, help="Диапазон памяти (start end)")

    args = parser.parse_args()
    interpreter = Interpreter(args.input, args.result, args.range)
    interpreter.load_program()
    interpreter.execute()
