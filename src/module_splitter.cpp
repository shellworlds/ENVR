#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>

class Matrix {
private:
    std::vector<std::vector<double>> data;
    int rows, cols;
    
public:
    Matrix(int r, int c) : rows(r), cols(c), data(r, std::vector<double>(c, 0.0)) {}
    
    void setIdentity() {
        for (int i = 0; i < std::min(rows, cols); ++i) {
            data[i][i] = 1.0;
        }
    }
    
    Matrix operator*(const Matrix& other) const {
        assert(cols == other.rows);
        Matrix result(rows, other.cols);
        
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < other.cols; ++j) {
                double sum = 0.0;
                for (int k = 0; k < cols; ++k) {
                    sum += data[i][k] * other.data[k][j];
                }
                result.data[i][j] = sum;
            }
        }
        return result;
    }
    
    Matrix operator+(const Matrix& other) const {
        assert(rows == other.rows && cols == other.cols);
        Matrix result(rows, cols);
        
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                result.data[i][j] = data[i][j] + other.data[i][j];
            }
        }
        return result;
    }
    
    bool isZero(double tolerance = 1e-10) const {
        for (const auto& row : data) {
            for (double val : row) {
                if (std::abs(val) > tolerance) return false;
            }
        }
        return true;
    }
    
    bool isIdentity(double tolerance = 1e-10) const {
        if (rows != cols) return false;
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                double expected = (i == j) ? 1.0 : 0.0;
                if (std::abs(data[i][j] - expected) > tolerance) return false;
            }
        }
        return true;
    }
    
    void print() const {
        for (const auto& row : data) {
            for (double val : row) {
                std::cout << val << " ";
            }
            std::cout << "\n";
        }
    }
};

class ModuleSplitter {
private:
    int l_dim, n_dim, m_dim;
    
public:
    ModuleSplitter(int l, int n) : l_dim(l), n_dim(n), m_dim(l + n) {}
    
    void createStandardMaps(Matrix& alpha, Matrix& beta, Matrix& sigma, Matrix& rho) {
        // α: L → M (inclusion)
        alpha = Matrix(m_dim, l_dim);
        for (int i = 0; i < l_dim; ++i) {
            alpha.data[i][i] = 1.0;
        }
        
        // β: M → N (projection)
        beta = Matrix(n_dim, m_dim);
        for (int i = 0; i < n_dim; ++i) {
            beta.data[i][l_dim + i] = 1.0;
        }
        
        // σ: N → M (inclusion)
        sigma = Matrix(m_dim, n_dim);
        for (int i = 0; i < n_dim; ++i) {
            sigma.data[l_dim + i][i] = 1.0;
        }
        
        // ρ: M → L (projection)
        rho = Matrix(l_dim, m_dim);
        for (int i = 0; i < l_dim; ++i) {
            rho.data[i][i] = 1.0;
        }
    }
    
    bool verifyTheorem(const Matrix& alpha, const Matrix& beta,
                      const Matrix& sigma, const Matrix& rho) {
        Matrix ba = beta * alpha;
        Matrix bs = beta * sigma;
        Matrix rs = rho * sigma;
        Matrix ra = rho * alpha;
        Matrix ar = alpha * rho;
        Matrix sb = sigma * beta;
        Matrix ar_sb = ar + sb;
        
        return ba.isZero() && bs.isIdentity() && 
               rs.isZero() && ra.isIdentity() && 
               ar_sb.isIdentity();
    }
};

int main() {
    ModuleSplitter splitter(2, 3);
    
    Matrix alpha(5, 2), beta(3, 5), sigma(5, 3), rho(2, 5);
    splitter.createStandardMaps(alpha, beta, sigma, rho);
    
    std::cout << "Module Splitting Theorem Verification\n";
    std::cout << "Dimensions: L=" << 2 << ", N=" << 3 << ", M=" << 5 << "\n";
    
    if (splitter.verifyTheorem(alpha, beta, sigma, rho)) {
        std::cout << "✓ All conditions satisfied: M = L ⊕ N\n";
    } else {
        std::cout << "✗ Conditions failed\n";
    }
    
    return 0;
}
