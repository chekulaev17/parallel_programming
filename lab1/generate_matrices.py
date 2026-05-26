#!/usr/bin/env python3
import numpy as np
import os

def generate_matrix(size, filename, min_val=-10, max_val=10):
    """Генерация квадратной матрицы и сохранение в файл"""
    matrix = np.random.uniform(min_val, max_val, (size, size))
    
    with open(filename, 'w') as f:
        f.write(f"{size}\n")
        for row in matrix:
            f.write(" ".join(f"{x:.6f}" for x in row) + "\n")
    
    print(f"Сгенерирована матрица {size}x{size} -> {filename}")
    return matrix

if __name__ == "__main__":
    # Создаём папку data если её нет
    os.makedirs("lab1/data", exist_ok=True)
    
    # Размеры матриц для тестирования
    sizes = [200, 400, 800, 1200, 1600, 2000]
    
    for size in sizes:
        generate_matrix(size, f"lab1/data/matrixA_{size}.txt")
        generate_matrix(size, f"lab1/data/matrixB_{size}.txt")
    
    print("\nГенерация завершена!")
