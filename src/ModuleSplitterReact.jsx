import React, { useState, useEffect } from 'react';
import './ModuleSplitter.css';

/**
 * React component for Module Splitting Theorem visualization
 */
const ModuleSplitterReact = () => {
    const [lDim, setLDim] = useState(2);
    const [nDim, setNDim] = useState(3);
    const [conditions, setConditions] = useState([
        { name: 'βα = 0', satisfied: false },
        { name: 'βσ = 1', satisfied: false },
        { name: 'ρσ = 0', satisfied: false },
        { name: 'ρα = 1', satisfied: false },
        { name: 'αρ + σβ = 1', satisfied: false }
    ]);
    const [theoremVerified, setTheoremVerified] = useState(false);

    // Matrix operations
    const createMatrix = (rows, cols, fill = 0) => 
        Array(rows).fill().map(() => Array(cols).fill(fill));

    const matrixMultiply = (A, B) => {
        const rowsA = A.length, colsA = A[0].length;
        const rowsB = B.length, colsB = B[0].length;
        if (colsA !== rowsB) throw new Error('Invalid dimensions');
        
        const result = createMatrix(rowsA, colsB);
        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsB; j++) {
                let sum = 0;
                for (let k = 0; k < colsA; k++) {
                    sum += A[i][k] * B[k][j];
                }
                result[i][j] = sum;
            }
        }
        return result;
    };

    const matrixAdd = (A, B) => {
        const rows = A.length, cols = A[0].length;
        const result = createMatrix(rows, cols);
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                result[i][j] = A[i][j] + B[i][j];
            }
        }
        return result;
    };

    const isZeroMatrix = (matrix, tolerance = 1e-10) => 
        matrix.every(row => row.every(val => Math.abs(val) < tolerance));

    const isIdentityMatrix = (matrix, tolerance = 1e-10) => {
        if (matrix.length !== matrix[0].length) return false;
        for (let i = 0; i < matrix.length; i++) {
            for (let j = 0; j < matrix.length; j++) {
                const expected = i === j ? 1 : 0;
                if (Math.abs(matrix[i][j] - expected) > tolerance) return false;
            }
        }
        return true;
    };

    const verifyTheorem = () => {
        const mDim = lDim + nDim;
        
        // Create standard maps
        const alpha = createMatrix(mDim, lDim);
        const beta = createMatrix(nDim, mDim);
        const sigma = createMatrix(mDim, nDim);
        const rho = createMatrix(lDim, mDim);
        
        for (let i = 0; i < lDim; i++) alpha[i][i] = 1;
        for (let i = 0; i < nDim; i++) beta[i][lDim + i] = 1;
        for (let i = 0; i < nDim; i++) sigma[lDim + i][i] = 1;
        for (let i = 0; i < lDim; i++) rho[i][i] = 1;
        
        // Check conditions
        const ba = matrixMultiply(beta, alpha);
        const bs = matrixMultiply(beta, sigma);
        const rs = matrixMultiply(rho, sigma);
        const ra = matrixMultiply(rho, alpha);
        const ar = matrixMultiply(alpha, rho);
        const sb = matrixMultiply(sigma, beta);
        const arPlusSb = matrixAdd(ar, sb);
        
        const newConditions = [
            { name: 'βα = 0', satisfied: isZeroMatrix(ba) },
            { name: 'βσ = 1', satisfied: isIdentityMatrix(bs) },
            { name: 'ρσ = 0', satisfied: isZeroMatrix(rs) },
            { name: 'ρα = 1', satisfied: isIdentityMatrix(ra) },
            { name: 'αρ + σβ = 1', satisfied: isIdentityMatrix(arPlusSb) }
        ];
        
        setConditions(newConditions);
        setTheoremVerified(newConditions.every(c => c.satisfied));
    };

    useEffect(() => {
        verifyTheorem();
    }, [lDim, nDim]);

    return (
        <div className="module-splitter-container">
            <header className="header">
                <h1>Module Splitting Theorem</h1>
                <p className="subtitle">Interactive proof that M = L ⊕ N</p>
            </header>
            
            <div className="content">
                <div className="control-panel">
                    <div className="dimension-control">
                        <label>
                            L Dimension: {lDim}
                            <input 
                                type="range" 
                                min="1" 
                                max="5" 
                                value={lDim}
                                onChange={(e) => setLDim(parseInt(e.target.value))}
                            />
                        </label>
                        <label>
                            N Dimension: {nDim}
                            <input 
                                type="range" 
                                min="1" 
                                max="5" 
                                value={nDim}
                                onChange={(e) => setNDim(parseInt(e.target.value))}
                            />
                        </label>
                    </div>
                    
                    <div className="theorem-statement">
                        <h3>Theorem Conditions:</h3>
                        <p>For A-modules L, M, N and homomorphisms:</p>
                        <p>α: L → M, β: M → N, σ: N → M, ρ: M → L</p>
                        <p>M = L ⊕ N with α=iₗ, β=πₙ, σ=iₙ, ρ=πₗ iff:</p>
                    </div>
                    
                    <div className="conditions-list">
                        {conditions.map((cond, index) => (
                            <div key={index} className="condition-item">
                                <span className="condition-name">{cond.name}</span>
                                <span className={`condition-status ${cond.satisfied ? 'satisfied' : 'failed'}`}>
                                    {cond.satisfied ? '✓' : '✗'}
                                </span>
                            </div>
                        ))}
                    </div>
                    
                    <div className={`verification-result ${theoremVerified ? 'verified' : 'not-verified'}`}>
                        <h3>
                            {theoremVerified ? '✓ Theorem Verified' : '✗ Theorem Not Verified'}
                        </h3>
                        <p>
                            {theoremVerified 
                                ? `M (${lDim + nDim}D) = L (${lDim}D) ⊕ N (${nDim}D)`
                                : 'Conditions not satisfied'}
                        </p>
                    </div>
                </div>
                
                <div className="visualization">
                    <div className="matrix-representation">
                        <h3>Matrix Representations</h3>
                        <div className="matrices">
                            <div className="matrix-group">
                                <h4>α: L → M</h4>
                                <p>Inclusion of L into M</p>
                            </div>
                            <div className="matrix-group">
                                <h4>β: M → N</h4>
                                <p>Projection onto N</p>
                            </div>
                            <div className="matrix-group">
                                <h4>σ: N → M</h4>
                                <p>Inclusion of N into M</p>
                            </div>
                            <div className="matrix-group">
                                <h4>ρ: M → L</h4>
                                <p>Projection onto L</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <footer className="footer">
                <p>ENVR Module Splitter • React Implementation • shellworlds</p>
            </footer>
        </div>
    );
};

export default ModuleSplitterReact;
