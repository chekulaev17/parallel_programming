import random
import sys
import os

def create_matrix(dim, outpath):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w') as f:
        f.write(f"{dim}\n")
        for i in range(dim):
            vals = [round(random.uniform(1.0, 10.0), 4) for _ in range(dim)]
            f.write(" ".join(map(str, vals)) + "\n")

if __name__ == "__main__":
    dim = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"Generating {dim}x{dim} matrices...")
    create_matrix(dim, "data/matrixA.txt")
    create_matrix(dim, "data/matrixB.txt")
    print("Done!")
