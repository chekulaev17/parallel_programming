#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <iomanip>

using namespace std;
using namespace chrono;

vector<vector<double>> computeProduct(const vector<vector<double>>& X,
                                      const vector<vector<double>>& Y,
                                      int dim) {
    vector<vector<double>> Z(dim, vector<double>(dim, 0.0));
    
    for (int i = 0; i < dim; ++i) {
        for (int k = 0; k < dim; ++k) {
            double xik = X[i][k];
            for (int j = 0; j < dim; ++j) {
                Z[i][j] += xik * Y[k][j];
            }
        }
    }
    return Z;
}

vector<vector<double>> loadMatrix(const string& fname, int& sz) {
    ifstream infile(fname);
    if (!infile.is_open()) {
        cerr << "Error: cannot open file " << fname << endl;
        exit(1);
    }
    
    infile >> sz;
    vector<vector<double>> M(sz, vector<double>(sz));
    
    for (int i = 0; i < sz; ++i)
        for (int j = 0; j < sz; ++j)
            infile >> M[i][j];
    
    infile.close();
    return M;
}

void saveMatrix(const string& fname, const vector<vector<double>>& M, int sz) {
    ofstream outfile(fname);
    if (!outfile.is_open()) {
        cerr << "Error: cannot write file " << fname << endl;
        exit(1);
    }
    
    outfile << sz << "\n";
    for (int i = 0; i < sz; ++i) {
        for (int j = 0; j < sz; ++j) {
            outfile << fixed << setprecision(15) << M[i][j];
            if (j < sz - 1) outfile << " ";
        }
        outfile << "\n";
    }
    outfile.close();
}

int main() {
    int d1, d2;
    
    vector<vector<double>> X = loadMatrix("data/matrixA.txt", d1);
    vector<vector<double>> Y = loadMatrix("data/matrixB.txt", d2);
    
    if (d1 != d2) {
        cerr << "Error: matrices must be same size" << endl;
        return 1;
    }
    
    int dim = d1;
    cout << "Matrix size: " << dim << "x" << dim << endl;
    
    auto start = high_resolution_clock::now();
    vector<vector<double>> Z = computeProduct(X, Y, dim);
    auto end = high_resolution_clock::now();
    
    duration<double> elapsed = end - start;
    
    saveMatrix("data/matrixC.txt", Z, dim);
    
    cout << "Computation time: " << elapsed.count() << " seconds" << endl;
    cout << "Operations: " << (long long)dim * dim * dim << endl;
    
    return 0;
}
