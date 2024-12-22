import os
import sys
import tarfile
from io import BytesIO
from bs4 import BeautifulSoup as Soup

import requests
from collections import defaultdict

def download_data(base_url, distro, component, arch):
    url = f"{base_url}/{distro}/{component}/{arch}/APKINDEX.tar.gz"
    print(url)
    #try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with tarfile.open('rb', fileobj=BytesIO(response.content), encoding='utf-8') as f:
        ff = f.extractfile("APKINDEX")
        return ff.readlines()
    #except Exception as e:
    #    print(f"Ошибка при загрузке {url}: {e}")
    #    sys.exit(1)

def parse_packages(packages_data):
    dependencies = defaultdict(list)
    current_package = None

    for line in packages_data:
        line = line.strip().decode("utf8")
        if line.startswith("P:"):
            current_package = line.split(":", 1)[1].strip()
        elif line.startswith("D:") and current_package:
            dep_line = line.split(":", 1)[1].strip()
            deps = []
            for dep in dep_line.split():
                if dep.startswith("so:"):
                    deps.append(dep.split(":")[1].split(".")[0])
                else:
                    deps.append(dep)
            dependencies[current_package].extend(deps)
        elif not line:  # Пустая строка — конец блока текущего пакета
            current_package = None
    return dependencies

def build_dependency_graph(package_name, dependencies, max_depth):
    #Построение графа зависимостей до указанной глубины.
    graph = defaultdict(list)
    visited = set()

    def fetch_deps(pkg, depth):
        if depth > max_depth or pkg in visited:
            return
        visited.add(pkg)
        for dep in dependencies.get(pkg, []):
            graph[pkg].append(dep)
            fetch_deps(dep, depth + 1)

    fetch_deps(package_name, 0)
    return graph

def generate_mermaid_graph(graph):
    #Генерирует граф в формате Mermaid.
    mermaid = ["graph TD"]
    for pkg, deps in graph.items():
        for dep in deps:
            mermaid.append(f"    {pkg} --> {dep}")
    return "\n".join(mermaid)

def read_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        soup = Soup(file.read(),features="xml")
        sp = soup.find("root")
        visualizer_path = sp.find("visualizer_path").text
        package_name = sp.find("package_name").text
        output_file = sp.find("output_file").text
        base_url = sp.find("base_url").text
        max_depth = sp.find("max_depth").text
        return visualizer_path, package_name, output_file, base_url, int(max_depth)
def main():
    # Настройки
    config_path = r"config.xml"
    distro = "edge"
    component = "main"
    arch = "x86_64"

    # Проверка конфигурации
    if not os.path.exists(config_path):
        print(f"Ошибка: файл конфигурации {config_path} не найден.")
        sys.exit(1)

    # Чтение конфигурации

    visualizer_path, package_name, output_file, base_url, max_depth = read_config(config_path)

    max_depth = int(max_depth)

    print("Загрузка APKINDEX...")
    packages_data = download_data(base_url, distro, component, arch)
    print("Парсинг APKINDEX...")
    dependencies = parse_packages(packages_data)

    # Построение графа зависимостей
    print("Построение графа зависимостей...")
    graph = build_dependency_graph(package_name, dependencies, max_depth)

    # Генерация Mermaid-графа
    print("Генерация Mermaid-графа...")
    mermaid_graph = generate_mermaid_graph(graph)

    # Запись в файл
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(mermaid_graph)
        print(f"Граф зависимостей записан в файл {output_file}.")
    else:
        print("Граф зависимостей:")
        print(mermaid_graph)

if __name__ == "__main__":
    main()
