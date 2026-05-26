#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <iomanip>

using namespace std;
using namespace chrono;

// Функция для чтения матрицы из файла
vector<vector<double>> readMatrix(const string& filename, int& n) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка открытия файла: " << filename << endl;
        exit(1);
    }
    
    file >> n;
    vector<vector<double>> matrix(n, vector<double>(n));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            file >> matrix[i][j];
        }
    }
    
    file.close();
    return matrix;
}

// Функция для записи матрицы в файл
void writeMatrix(const string& filename, const vector<vector<double>>& matrix) {
    ofstream file(filename);
    int n = matrix.size();
    file << n << endl;
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            file << matrix[i][j];
            if (j < n - 1) file << " ";
        }
        file << endl;
    }
    
    file.close();
}

// Последовательное умножение матриц
vector<vector<double>> multiplyMatrices(const vector<vector<double>>& A, 
                                         const vector<vector<double>>& B) {
    int n = A.size();
    vector<vector<double>> C(n, vector<double>(n, 0.0));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    
    return C;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Использование: " << argv[0] << " <matrixA.txt> <matrixB.txt> <result.txt>" << endl;
        return 1;
    }
    
    string fileA = argv[1];
    string fileB = argv[2];
    string fileResult = argv[3];
    
    int n;
    cout << "Чтение матриц..." << endl;
    auto start = high_resolution_clock::now();
    
    vector<vector<double>> A = readMatrix(fileA, n);
    vector<vector<double>> B = readMatrix(fileB, n);
    
    auto read_end = high_resolution_clock::now();
    auto read_duration = duration_cast<milliseconds>(read_end - start);
    
    cout << "Умножение матриц размером " << n << "x" << n << "..." << endl;
    auto multiply_start = high_resolution_clock::now();
    
    vector<vector<double>> C = multiplyMatrices(A, B);
    
    auto multiply_end = high_resolution_clock::now();
    auto multiply_duration = duration_cast<milliseconds>(multiply_end - multiply_start);
    
    cout << "Запись результата..." << endl;
    writeMatrix(fileResult, C);
    
    auto total_end = high_resolution_clock::now();
    auto total_duration = duration_cast<milliseconds>(total_end - start);
    
    // Вывод статистики
    cout << "\n=== РЕЗУЛЬТАТЫ ===" << endl;
    cout << "Размер матрицы: " << n << " x " << n << endl;
    cout << "Объем задачи: " << n * n * 2 << " элементов" << endl;
    cout << "Время чтения: " << read_duration.count() << " мс" << endl;
    cout << "Время умножения: " << multiply_duration.count() << " мс" << endl;
    cout << "Общее время: " << total_duration.count() << " мс" << endl;
    cout << "Результат сохранен в: " << fileResult << endl;
    
    return 0;
}
