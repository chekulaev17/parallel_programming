#!/usr/bin/env python3
import random
import os
import sys

def generateSquareMatrix(size, outputPath):
    """
    Генерация квадратной матрицы заданного размера
    и сохранение в текстовый файл.
    
    Параметры:
        size: размерность матрицы (size x size)
        outputPath: путь для сохранения файла
    """
    # Создание директории при необходимости
    os.makedirs(os.path.dirname(outputPath), exist_ok=True)
    
    with open(outputPath, 'w', encoding='utf-8') as file:
        # Запись размера матрицы
        file.write(f"{size}\n")
        
        # Генерация и запись строк матрицы
        for rowIndex in range(size):
            rowValues = [round(random.uniform(-5.0, 5.0), 6) for _ in range(size)]
            file.write(" ".join(map(str, rowValues)) + "\n")
    
    print(f"[OK] Сгенерирована матрица {size}x{size} -> {outputPath}")

def main():
    # Определение размера матрицы (по умолчанию 100)
    matrixSize = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    
    print(f"=== ГЕНЕРАТОР ТЕСТОВЫХ ДАННЫХ ===")
    print(f"Размер матриц: {matrixSize}x{matrixSize}")
    
    # Генерация двух матриц для умножения
    generateSquareMatrix(matrixSize, "lab1/data/matrixA.txt")
    generateSquareMatrix(matrixSize, "lab1/data/matrixB.txt")
    
    print(f"\n[ГОТОВО] Создано 2 матрицы размером {matrixSize}x{matrixSize}")
    print(f"Расположение: lab1/data/")

if __name__ == "__main__":
    main()
