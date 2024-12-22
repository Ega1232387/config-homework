import argparse
import struct
import yaml

class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file
        self.opcodes = {
            "LOAD": 6,    # Загрузка константы (3 байта)
            "READ": 3,    # Чтение значения из памяти (3 байта)
            "WRITE": 0,   # Запись значения в память (4 байта)
            "REV": 13,     # bitreverse (4 байта)
        }

    def assemble(self):
        binary_data = []
        log_entries = {}

        # Считываем текстовый файл с программой
        with open(self.input_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue

            # Удаляем комментарии в конце строки
            if '#' in line:
                line = line[:line.index('#')].strip()

            # Разделяем команду и операнды
            parts = line.split()
            if len(parts) < 2:
                raise ValueError(f"Неправильный формат команды: {line}")

            command = parts[0].upper()
            operands = list(map(int, parts[1:]))

            # Проверяем, существует ли команда в таблице опкодов
            if command not in self.opcodes:
                raise ValueError(f"Неизвестная команда: {command}")

            opcode = self.opcodes[command]

            # Пакуем данные в бинарный формат
            if command == "LOAD":  # A=6, B - константа (19 бит)
                if len(operands) != 2:
                    raise ValueError(f"Команда LOAD ожидает 2 операнда")
                if not (0 <= operands[1] < 2**19):  # B: 19 бит для константы
                    raise ValueError(f"Константа B должна быть в диапазоне [0, {2**19-1}]")
                
                first_byte = (operands[1] & 0xF) << 4 | 0x6
                
                b_high = ((operands[1] & 0xF0) | (operands[1] & 0xF00)) >> 4
                b_low = ((operands[1] & 0xF000) | (operands[1] & 0x70000)) >> 12
                
                packed_data = bytes([
                    first_byte,
                    b_high,          # старшие биты B
                    b_low,           # младшие биты B
                ])

            elif command == "READ":  # A=3, B - смещение (15 бит)
                if len(operands) != 2:
                    raise ValueError(f"Команда READ ожидает 2 операнда")
                if not (0 <= operands[1] < 2**15):  # B: 15 бит для смещения
                    raise ValueError(f"Смещение B должно быть в диапазоне [0, {2**15-1}]")

                first_byte = (operands[1] & 0xF) << 4 | 0x3

                b_high = ((operands[1] & 0xF0) | (operands[1] & 0xF00)) >> 4
                b_low = (operands[1] & 0x7000) >> 8

                packed_data = bytes([
                    first_byte,
                    b_high,          # старшие биты B
                    b_low,           # младшие биты B
                ])

            elif command == "WRITE":  # A=0, B - адрес (24 бита)
                if len(operands) != 2:
                    raise ValueError(f"Команда WRITE ожидает 2 операнда")
                if not (0 <= operands[1] < 2**24):
                    raise ValueError(f"Адрес должен быть в диапазоне [0, {2**23-1}]")

                first_byte = (operands[1] & 0xF) << 4 | 0x0

                b_high = ((operands[1] & 0xF0) | (operands[1] & 0xF00)) >> 4
                b_mid = ((operands[1] & 0xF000) | (operands[1] & 0xF0000)) >> 12
                b_low = (operands[1] & 0xF00000) >> 16

                packed_data = bytes([
                    first_byte,
                    b_high,  # старшие биты B
                    b_mid,  # средние биты B
                    b_low,  # младшие биты B
                ])


            elif command == "REV":  # A=0, B - адрес (24 бита)

                if len(operands) != 2:
                    raise ValueError(f"Команда REV ожидает 2 операнда")
                if not (0 <= operands[1] < 2 ** 24):
                    raise ValueError(f"Адрес должен быть в диапазоне [0, {2 ** 23 - 1}]")

                first_byte = (operands[1] & 0xF) << 4 | 0xD

                b_high = ((operands[1] & 0xF0) | (operands[1] & 0xF00)) >> 4
                b_mid = ((operands[1] & 0xF000) | (operands[1] & 0xF0000)) >> 12
                b_low = (operands[1] & 0xF00000) >> 16

                packed_data = bytes([

                    first_byte,

                    b_high,  # старшие биты B
                    b_mid,  # средние биты B
                    b_low,  # младшие биты B

                ])

            else:
                raise ValueError(f"Команда {command} не поддерживается: {line}")

            binary_data.append(packed_data)
            if command not in log_entries.keys():
                log_entries[command] = []
            log_entries[command].append(f"{command} {operands}")

            # Отладочный вывод
            print(f"Обработана команда: {command} {operands} {packed_data}")

        # Записываем бинарные данные в выходной файл
        with open(self.output_file, 'wb') as bin_file:
            for entry in binary_data:
                bin_file.write(entry)

        # Создаем лог-файл в формате CSV
        with open(self.log_file, 'w') as log_file:
            yaml.dump(log_entries, log_file)

        print(f"Сборка завершена. Бинарный файл: {self.output_file}, Лог-файл: {self.log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for the educational virtual machine.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input assembly file.")
    parser.add_argument('-o', '--output', required=True, help="Path to the output binary file.")
    parser.add_argument('-l', '--log', required=True, help="Path to the log file.")

    args = parser.parse_args()

    assembler = Assembler(args.input, args.output, args.log)
    assembler.assemble()
