import subprocess
import sys
import os

def generate():
    print("Ejecutando build_revamped_map.py para compilar mapa con Clustering, Autocompletado, Modal, Skeleton y Filtros...")
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), 'build_revamped_map.py')]
    subprocess.run(cmd, check=True)
    print("Mapa actualizado correctamente.")

if __name__ == '__main__':
    generate()
