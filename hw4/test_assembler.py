import unittest
from assembler import Assembler
from interpreter import Interpreter
import os
import tempfile

class TestAssembler(unittest.TestCase):
    def setUp(self):
        # Создаем временные файлы для тестов
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, "program.asm")
        self.output_file = os.path.join(self.temp_dir, "test.bin")
        self.log_file = os.path.join(self.temp_dir, "test.yaml")
        self.result_file = os.path.join(self.temp_dir, "temp_result.yaml")

    def tearDown(self):
        # Удаляем временные файлы
        for file in [self.input_file, self.output_file, self.log_file]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)

    def test_load_command(self):
        # Тест команды LOAD с параметрами A=6, B=20
        # Ожидаемый результат: 0xA6, 0x00, 0x00
        with open(self.input_file, 'w') as f:
            f.write("LOAD 6 20")

        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        with open(self.output_file, 'rb') as f:
            binary_data = f.read()

        expected = bytes([
            0x46,
            0x01,
            0x00
        ])
        self.assertEqual(binary_data, expected)

    def test_read_command(self):
        # Тест команды READ с параметрами A=3, B=200
        # Ожидаемый результат: 0x83, 0x0C, 0x00
        with open(self.input_file, 'w') as f:
            f.write("READ 3 200")

        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        with open(self.output_file, 'rb') as f:
            binary_data = f.read()

        expected = bytes([
            0x83,
            0x0C,
            0x00
        ])
        self.assertEqual(binary_data, expected)

    def test_write_command(self):
        # Тест команды WRITE с параметрами A=0, B=106
        # Ожидаемый результат: 0xA0, 0x06, 0x00, 0x00
        with open(self.input_file, 'w') as f:
            f.write("WRITE 3 106")

        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        with open(self.output_file, 'rb') as f:
            binary_data = f.read()

        expected = bytes([
            0xA0,
            0x06,
            0x00,
            0x00
        ])
        self.assertEqual(binary_data, expected)

    def test_rev_command(self):
        # Тест команды REV с параметрами A=13, B=326
        # Ожидаемый результат: 0x6D, 0x14, 0x00, 0x00
        with open(self.input_file, 'w') as f:
            f.write("REV 12 326")

        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        with open(self.output_file, 'rb') as f:
            binary_data = f.read()

        expected = bytes([
            0x6D,
            0x14,
            0x00,
            0x00
        ])
        self.assertEqual(binary_data, expected)

    def test_invalid_command(self):
        # Тест на неправильную команду
        with open(self.input_file, 'w') as f:
            f.write("INVALID 1 2 3")

        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        with self.assertRaises(ValueError):
            assembler.assemble()

    def test_invalid_operands_count(self):
        # Тест на неправильное количество операндов
        with open(self.input_file, 'w') as f:
            f.write("LOAD 1 2 3")  # LOAD требует 2 операнда

        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        with self.assertRaises(ValueError):
            assembler.assemble()

    def main_test(self):
        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        interpreter = Interpreter(self.output_file, self.result_file, "100 105")
        interpreter.load_program()
        with self.assertRaises(ValueError):
            interpreter.execute()

if __name__ == '__main__':
    unittest.main()
