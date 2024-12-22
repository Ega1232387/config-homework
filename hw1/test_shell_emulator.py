import unittest
import os
from shell_emulator import ShellEmulator
import shutil

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        shutil.copyfile("virtual_filesystem.tar", "test_filesystem.tar")
        self.emulator = ShellEmulator('test_filesystem.tar')

    def tearDown(self):
        os.remove("test_filesystem.tar")
        pass

    def test_load_virtual_fs(self):
        self.assertTrue(len(self.emulator.fs_structure) != 0)

    def test_ls_command(self):
        result = self.emulator.execute_command('ls')
        expected_files = {'file2.txt', 'file1.txt', 'directory'}
        self.assertTrue(expected_files.issubset(set(result.split('\n'))))

    def test_ls_command2(self):
        self.emulator.execute_command('cd directory')
        result = self.emulator.execute_command('ls')
        expected_files = {'file3.txt'}
        self.assertTrue(expected_files.issubset(set(result.split('\n'))))

    def test_cd_command(self):
        self.emulator.execute_command('cd directory')
        self.assertEqual(self.emulator.current_directory, "directory")

    def test_cd_command_fail(self):
        result = self.emulator.execute_command('cd non_existing_directory')
        self.assertEqual(result, "Directory non_existing_directory not found")

    def test_exit_command(self):
        result = self.emulator.execute_command('exit')
        self.assertEqual(result, "Exiting...")

    def test_rm_command(self):
        self.emulator.execute_command('rm file1.txt')
        result = self.emulator.execute_command('ls')
        expected_files = {'file2.txt', 'directory'}
        self.assertTrue(expected_files.issubset(set(result.split('\n'))))

    def test_rm_command_fail(self):
        result = self.emulator.execute_command('rm file5928.txt')
        self.assertEqual(result, "File file5928.txt not found")

    def test_whoami_command(self):
        result = self.emulator.execute_command('whoami')
        self.assertEqual(result, "invertie")

if __name__ == '__main__':
    unittest.main()
