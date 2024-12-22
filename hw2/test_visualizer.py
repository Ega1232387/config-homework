import unittest
from visualizer import read_config, generate_mermaid_graph, download_data

class TestVisualizer(unittest.TestCase):
    def test_read_config(self):
        config = read_config("config.xml")
        self.assertEqual(config[1], "curl")
        self.assertEqual(config[4], 3)

    def test_download_data(self):
        packages_data = download_data("http://dl-cdn.alpinelinux.org/alpine", "edge", "main", "x86_64")
        self.assertTrue(packages_data != None)

    def build_dependency_graph(self):
        deps = [("curl", "libcurl"), ("libcurl", "openssl")]
        mermaid_code = generate_mermaid_graph(deps)
        expected = "graph TD\n    curl --> libcurl\n    libcurl --> openssl"
        self.assertEqual(mermaid_code.strip(), expected)

if __name__ == "__main__":
    unittest.main()
