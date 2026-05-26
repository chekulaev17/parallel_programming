#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <string>

using namespace std;
using namespace chrono;

// Функция загрузки матрицы из файла
vector<vector<double>> loadMatrix(const string& filePath, int& dimension) {
    ifstream inputFile(filePath);
    
    if (!inputFile.is_open()) {
        cerr << "[ОШИБКА] Невозможно открыть файл: " << filePath << endl;
        exit(EXIT_FAILURE);
    }
    
    inputFile >> dimension;
    
    vector<vector<double>> matrix(dimension, vector<double>(dimension, 0.0));
    
    for (int row = 0; row < dimension; row++) {
        for (int col = 0; col < dimension; col++) {
            inputFile >> matrix[row][col];
        }
    }
    
    inputFile.close();
    return matrix;
}

// Функция сохранения матрицы в файл
void saveMatrix(const string& filePath, const vector<vector<double>>& matrix, int dimension) {
    ofstream outputFile(filePath);
    
    if (!outputFile.is_open()) {
        cerr << "[ОШИБКА] Невозможно создать файл: " << filePath << endl;
        exit(EXIT_FAILURE);
    }
    
    outputFile << dimension << "\n";
    
    for (int row = 0; row < dimension; row++) {
        for (int col = 0; col < dimension; col++) {
            outputFile << fixed << setprecision(6) << matrix[row][col];
            if (col < dimension - 1) outputFile << " ";
        }
        outputFile << "\n";
    }
    
    outputFile.close();
}

// Алгоритм умножения матриц
vector<vector<double>> multiplyMatrices(const vector<vector<double>>& A, 
                                        const vector<vector<double>>& B, 
                                        int dimension) {
    vector<vector<double>> result(dimension, vector<double>(dimension, 0.0));
    
    for (int i = 0; i < dimension; i++) {
        for (int k = 0; k < dimension; k++) {
            double aik = A[i][k];
            for (int j = 0; j < dimension; j++) {
                result[i][j] += aik * B[k][j];
            }
        }
    }
    
    return result;
}

int main() {
    int dimA, dimB;
    
    cout << "=== КАЛЬКУЛЯТОР МАТРИЦ ===\n";
    cout << "Загрузка данных...\n";
    
    // Чтение матриц из файлов
    vector<vector<double>> matrixA = loadMatrix("lab1/data/matrixA.txt", dimA);
    vector<vector<double>> matrixB = loadMatrix("lab1/data/matrixB.txt", dimB);
    
    // Проверка совместимости
    if (dimA <= 0 || dimB <= 0) {
        cerr << "[ОШИБКА] Неверный размер матрицы\n";
        return 1;
    }
    
    if (dimA != dimB) {
        cerr << "[ОШИБКА] Матрицы должны быть одинакового размера\n";
        return 1;
    }
    
    cout << "Размер матриц: " << dimA << "x" << dimA << "\n";
    cout << "Начало вычислений...\n";
    
    // Измерение времени выполнения
    auto startTime = high_resolution_clock::now();
    
    vector<vector<double>> resultMatrix = multiplyMatrices(matrixA, matrixB, dimA);
    
    auto endTime = high_resolution_clock::now();
    duration<double> elapsedSeconds = endTime - startTime;
    
    // Сохранение результата
    saveMatrix("lab1/data/matrixC.txt", resultMatrix, dimA);
    
    // Вывод статистики
    cout << "\n--- РЕЗУЛЬТАТЫ ---\n";
    cout << "Размер: " << dimA << "x" << dimA << "\n";
    cout << "Время выполнения: " << fixed << setprecision(4) << elapsedSeconds.count() << " сек\n";
    cout << "Кол-во операций: " << dimA * dimA * dimA << "\n";
    cout << "Результат сохранён: lab1/data/matrixC.txt\n";
    cout << "===================\n";
    
    return 0;
}
