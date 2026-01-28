package com.envr.modulesplitter;

import java.util.Arrays;

/**
 * Java implementation of Module Splitting Theorem.
 * Theorem: M = L ⊕ N with α, β, σ, ρ iff
 * βα=0, βσ=1, ρσ=0, ρα=1, αρ+σβ=1
 */
public class ModuleSplitter {
    private final int lDim;
    private final int nDim;
    private final int mDim;
    
    public ModuleSplitter(int lDim, int nDim) {
        this.lDim = lDim;
        this.nDim = nDim;
        this.mDim = lDim + nDim;
    }
    
    public static class Matrix {
        private final double[][] data;
        private final int rows;
        private final int cols;
        
        public Matrix(int rows, int cols) {
            this.rows = rows;
            this.cols = cols;
            this.data = new double[rows][cols];
        }
        
        public Matrix multiply(Matrix other) {
            if (this.cols != other.rows) {
                throw new IllegalArgumentException("Matrix dimensions incompatible");
            }
            
            Matrix result = new Matrix(this.rows, other.cols);
            for (int i = 0; i < this.rows; i++) {
                for (int j = 0; j < other.cols; j++) {
                    double sum = 0.0;
                    for (int k = 0; k < this.cols; k++) {
                        sum += this.data[i][k] * other.data[k][j];
                    }
                    result.data[i][j] = sum;
                }
            }
            return result;
        }
        
        public Matrix add(Matrix other) {
            if (this.rows != other.rows || this.cols != other.cols) {
                throw new IllegalArgumentException("Matrix dimensions must match");
            }
            
            Matrix result = new Matrix(rows, cols);
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    result.data[i][j] = this.data[i][j] + other.data[i][j];
                }
            }
            return result;
        }
        
        public boolean isZero(double tolerance) {
            for (double[] row : data) {
                for (double val : row) {
                    if (Math.abs(val) > tolerance) return false;
                }
            }
            return true;
        }
        
        public boolean isIdentity(double tolerance) {
            if (rows != cols) return false;
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    double expected = (i == j) ? 1.0 : 0.0;
                    if (Math.abs(data[i][j] - expected) > tolerance) return false;
                }
            }
            return true;
        }
        
        public void setIdentity() {
            int minDim = Math.min(rows, cols);
            for (int i = 0; i < minDim; i++) {
                data[i][i] = 1.0;
            }
        }
        
        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (double[] row : data) {
                sb.append(Arrays.toString(row)).append("\n");
            }
            return sb.toString();
        }
    }
    
    public Matrix createAlpha() {
        Matrix alpha = new Matrix(mDim, lDim);
        for (int i = 0; i < lDim; i++) {
            alpha.data[i][i] = 1.0;
        }
        return alpha;
    }
    
    public Matrix createBeta() {
        Matrix beta = new Matrix(nDim, mDim);
        for (int i = 0; i < nDim; i++) {
            beta.data[i][lDim + i] = 1.0;
        }
        return beta;
    }
    
    public Matrix createSigma() {
        Matrix sigma = new Matrix(mDim, nDim);
        for (int i = 0; i < nDim; i++) {
            sigma.data[lDim + i][i] = 1.0;
        }
        return sigma;
    }
    
    public Matrix createRho() {
        Matrix rho = new Matrix(lDim, mDim);
        for (int i = 0; i < lDim; i++) {
            rho.data[i][i] = 1.0;
        }
        return rho;
    }
    
    public boolean verifyTheorem(Matrix alpha, Matrix beta, Matrix sigma, Matrix rho) {
        double tolerance = 1e-10;
        
        Matrix ba = beta.multiply(alpha);
        Matrix bs = beta.multiply(sigma);
        Matrix rs = rho.multiply(sigma);
        Matrix ra = rho.multiply(alpha);
        Matrix ar = alpha.multiply(rho);
        Matrix sb = sigma.multiply(beta);
        Matrix arPlusSb = ar.add(sb);
        
        return ba.isZero(tolerance) &&
               bs.isIdentity(tolerance) &&
               rs.isZero(tolerance) &&
               ra.isIdentity(tolerance) &&
               arPlusSb.isIdentity(tolerance);
    }
    
    public static void main(String[] args) {
        ModuleSplitter splitter = new ModuleSplitter(2, 3);
        
        Matrix alpha = splitter.createAlpha();
        Matrix beta = splitter.createBeta();
        Matrix sigma = splitter.createSigma();
        Matrix rho = splitter.createRho();
        
        System.out.println("Module Splitting Theorem - Java Implementation");
        System.out.println("Dimensions: L=" + splitter.lDim + 
                         ", N=" + splitter.nDim + 
                         ", M=" + splitter.mDim);
        
        if (splitter.verifyTheorem(alpha, beta, sigma, rho)) {
            System.out.println("✓ Theorem verified: M = L ⊕ N");
        } else {
            System.out.println("✗ Theorem conditions not satisfied");
        }
    }
}
