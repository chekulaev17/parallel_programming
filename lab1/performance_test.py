#!/usr/bin/env python3
import subprocess
import csv
import os
import re
import sys

# Конфигурация тестирования
TEST_SIZES = [10, 50, 100, 500, 1000]
RESULTS_FILE = "lab1/performance_stats.csv"
EXECUTABLE_PATH = "lab1/src/matrix_processor"
SOURCE_FILE = "lab1/src/matrix_processor.cpp"
DATA_DIR = "lab1/data"

def compileProgram():
    """Компиляция C++ программы"""
    print("=== КОМПИЛЯЦИЯ ===")
    
    if not os.path.exists(SOURCE_FILE):
        print(f"[ОШИБКА] Исходный файл не найден: {SOURCE_FILE}")
        return False
    
    compileCmd = ["g++", "-O2", "-std=c++11", SOURCE_FILE, "-o", EXECUTABLE_PATH]
    
    try:
        result = subprocess.run(compileCmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print("[OK] Компиляция успешно завершена")
            return True
        else:
            print(f"[ОШИБКА] Ошибка компиляции:\n{result.stderr}")
            return False
    except Exception as error:
        print(f"[ОШИБКА] Исключение при компиляции: {error}")
        return False

def runSingleTest(matrixSize):
    """Запуск одного теста для заданного размера матрицы"""
    print(f"\n--- ТЕСТ: {matrixSize}x{matrixSize} ---")
    
    # Генерация тестовых данных
    print("Генерация матриц...")
    genCmd = ["python3", "lab1/data_generator.py", str(matrixSize)]
    
    try:
        genResult = subprocess.run(genCmd, capture_output=True, text=True, check=False)
        if genResult.returncode != 0:
            print(f"[ОШИБКА] Генерация данных не удалась:\n{genResult.stderr}")
            return None
    except Exception as error:
        print(f"[ОШИБКА] Исключение при генерации: {error}")
        return None
    
    # Запуск программы умножения
    print("Выполнение умножения...")
    runCmd = [EXECUTABLE_PATH]
    
    try:
        execResult = subprocess.run(runCmd, capture_output=True, text=True, check=False, cwd=".")
        
        if execResult.returncode != 0:
            print(f"[ОШИБКА] Ошибка выполнения:\n{execResult.stderr}")
            return None
        
        # Извлечение времени выполнения из вывода
        outputText = execResult.stdout
        print(outputText)
        
        # Поиск времени выполнения
        timePattern = r"Время выполнения:\s*([\d.]+)\s*сек"
        timeMatch = re.search(timePattern, outputText)
        
        if timeMatch:
            executionTime = float(timeMatch.group(1))
        else:
            print("[ПРЕДУПРЕЖДЕНИЕ] Не удалось найти время выполнения")
            executionTime = 0.0
        
        return executionTime
        
    except Exception as error:
        print(f"[ОШИБКА] Исключение при выполнении: {error}")
        return None

def verifyResults(matrixSize):
    """Проверка корректности вычислений"""
    print("Проверка результатов...")
    
    matrixAPath = f"{DATA_DIR}/matrixA.txt"
    matrixBPath = f"{DATA_DIR}/matrixB.txt"
    resultPath = f"{DATA_DIR}/matrixC.txt"
    
    verifyCmd = ["python3", "lab1/result_checker.py", matrixAPath, matrixBPath, resultPath]
    
    try:
        verifyResult = subprocess.run(verifyCmd, capture_output=True, text=True, check=False)
        print(verifyResult.stdout)
        
        # Анализ статуса проверки
        if "ПРОЙДЕНА" in verifyResult.stdout and "✓" in verifyResult.stdout:
            return "PASSED"
        else:
            return "FAILED"
    except Exception as error:
        print(f"[ОШИБКА] Исключение при проверке: {error}")
        return "ERROR"

def saveResultsToCSV(results):
    """Сохранение результатов тестирования в CSV файл"""
    if not results:
        print("[ПРЕДУПРЕЖДЕНИЕ] Нет данных для сохранения")
        return
    
    with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['MatrixSize', 'ExecutionTime(sec)', 'OperationsCount', 'VerificationStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for record in results:
            writer.writerow(record)
    
    print(f"\n[OK] Результаты сохранены: {RESULTS_FILE}")

def main():
    print("=" * 60)
    print("АВТОМАТИЗИРОВАННОЕ ТЕСТИРОВАНИЕ УМНОЖЕНИЯ МАТРИЦ")
    print("=" * 60)
    
    # Компиляция программы
    if not compileProgram():
        print("[НЕУДАЧА] Тестирование прервано из-за ошибки компиляции")
        sys.exit(1)
    
    # Создание директории для данных
    os.makedirs(DATA_DIR, exist_ok=True)
    
    testResults = []
    
    # Запуск тестов для каждого размера
    for size in TEST_SIZES:
        executionTime = runSingleTest(size)
        
        if executionTime is not None:
            operationsCount = size ** 3
            verificationStatus = verifyResults(size)
            
            testResults.append({
                'MatrixSize': size,
                'ExecutionTime(sec)': round(executionTime, 4),
                'OperationsCount': operationsCount,
                'VerificationStatus': verificationStatus
            })
            
            statusIcon = "✓" if verificationStatus == "PASSED" else "✗"
            print(f"РЕЗУЛЬТАТ [{size}x{size}]: {executionTime:.3f} сек, {verificationStatus} {statusIcon}")
        else:
            print(f"РЕЗУЛЬТАТ [{size}x{size}]: ПРОПУЩЕН")
    
    # Сохранение и отображение итогов
    saveResultsToCSV(testResults)
    
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)
    
    if testResults:
        print("\nСводка:")
        for record in testResults:
            print(f"  {record['MatrixSize']}x{record['MatrixSize']}: "
                  f"{record['ExecutionTime(sec)']} сек, {record['VerificationStatus']}")

if __name__ == "__main__":
    main()
