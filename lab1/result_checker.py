#!/usr/bin/env python3
import numpy as np
import sys
import os

def readMatrixFromFile(filepath):
    """
    Чтение матрицы из текстового файла.
    Формат: первая строка - размер, затем построчно элементы.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        # Чтение размера матрицы
        dimension = int(file.readline().strip())
        
        matrixData = []
        for line in file:
            if line.strip():  # Пропуск пустых строк
                row = [float(value) for value in line.split()]
                matrixData.append(row)
        
        # Проверка соответствия размерности
        if len(matrixData) != dimension:
            raise ValueError(f"Размерность не совпадает: ожидается {dimension}, получено {len(matrixData)}")
        
        return np.array(matrixData, dtype=np.float64)

def verifyMatrixMultiplication(matrixAPath, matrixBPath, resultPath, tolerance=1e-7):
    """
    Верификация умножения матриц с использованием NumPy.
    Возвращает True если результат корректен, False в противном случае.
    """
    print("\n=== ВЕРИФИКАЦИЯ РЕЗУЛЬТАТОВ ===")
    
    # Загрузка матриц
    print("Загрузка исходных матриц...")
    matrixA = readMatrixFromFile(matrixAPath)
    matrixB = readMatrixFromFile(matrixBPath)
    
    print("Загрузка вычисленного результата...")
    computedResult = readMatrixFromFile(resultPath)
    
    # Вычисление эталонного результата
    print("Вычисление эталонного результата (NumPy)...")
    expectedResult = np.dot(matrixA, matrixB)
    
    # Сравнение результатов
    difference = np.abs(computedResult - expectedResult)
    maxDifference = np.max(difference)
    meanDifference = np.mean(difference)
    
    isCorrect = maxDifference < tolerance
    
    # Вывод отчёта
    print("\n--- ОТЧЁТ О ПРОВЕРКЕ ---")
    print(f"Размер матриц: {matrixA.shape[0]}x{matrixA.shape[1]}")
    print(f"Максимальное отклонение: {maxDifference:.2e}")
    print(f"Среднее отклонение: {meanDifference:.2e}")
    print(f"Допустимая погрешность: {tolerance}")
    print(f"Статус: {'ПРОЙДЕНА ✓' if isCorrect else 'НЕ ПРОЙДЕНА ✗'}")
    print("========================\n")
    
    return isCorrect

def main():
    if len(sys.argv) != 4:
        print("Использование: python result_checker.py <matrixA.txt> <matrixB.txt> <result.txt>")
        print("Пример: python result_checker.py lab1/data/matrixA.txt lab1/data/matrixB.txt lab1/data/matrixC.txt")
        sys.exit(1)
    
    matrixAPath = sys.argv[1]
    matrixBPath = sys.argv[2]
    resultPath = sys.argv[3]
    
    try:
        success = verifyMatrixMultiplication(matrixAPath, matrixBPath, resultPath)
        sys.exit(0 if success else 1)
    except Exception as error:
        print(f"\n[ОШИБКА] {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
