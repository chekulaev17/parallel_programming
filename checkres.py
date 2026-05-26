import numpy as np
import sys

def read_matrix(fpath):
    with open(fpath, 'r') as f:
        dim = int(f.readline())
        mat = []
        for line in f:
            if line.strip():
                vals = [float(x) for x in line.split()]
                mat.append(vals)
    return mat

def start():
    try:
        X = read_matrix('data/matrixA.txt')
        Y = read_matrix('data/matrixB.txt')
        Z_cpp = read_matrix('data/matrixC.txt')
        
        X_np = np.array(X)
        Y_np = np.array(Y)
        Z_np = np.array(Z_cpp)
        Z_true = np.dot(X_np, Y_np)
        
        if np.allclose(Z_np, Z_true):
            print("PASSED")
            return 0
        else:
            print("FAILED")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(start())
