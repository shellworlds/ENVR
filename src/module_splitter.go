package main

import (
	"fmt"
	"sync"
)

// Matrix represents a 2D matrix
type Matrix struct {
	Rows, Cols int
	Data       [][]float64
}

// NewMatrix creates a new matrix with given dimensions
func NewMatrix(rows, cols int) *Matrix {
	data := make([][]float64, rows)
	for i := range data {
		data[i] = make([]float64, cols)
	}
	return &Matrix{Rows: rows, Cols: cols, Data: data}
}

// Identity creates an identity matrix
func Identity(n int) *Matrix {
	m := NewMatrix(n, n)
	for i := 0; i < n; i++ {
		m.Data[i][i] = 1.0
	}
	return m
}

// Multiply multiplies two matrices concurrently
func (m *Matrix) Multiply(other *Matrix) *Matrix {
	if m.Cols != other.Rows {
		panic("incompatible dimensions")
	}

	result := NewMatrix(m.Rows, other.Cols)
	var wg sync.WaitGroup

	for i := 0; i < m.Rows; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			for j := 0; j < other.Cols; j++ {
				sum := 0.0
				for k := 0; k < m.Cols; k++ {
					sum += m.Data[i][k] * other.Data[k][j]
				}
				result.Data[i][j] = sum
			}
		}(i)
	}
	wg.Wait()
	return result
}

// Add adds two matrices
func (m *Matrix) Add(other *Matrix) *Matrix {
	if m.Rows != other.Rows || m.Cols != other.Cols {
		panic("dimensions must match")
	}

	result := NewMatrix(m.Rows, m.Cols)
	for i := 0; i < m.Rows; i++ {
		for j := 0; j < m.Cols; j++ {
			result.Data[i][j] = m.Data[i][j] + other.Data[i][j]
		}
	}
	return result
}

// IsZero checks if matrix is zero within tolerance
func (m *Matrix) IsZero(tolerance float64) bool {
	for i := 0; i < m.Rows; i++ {
		for j := 0; j < m.Cols; j++ {
			if m.Data[i][j] > tolerance || m.Data[i][j] < -tolerance {
				return false
			}
		}
	}
	return true
}

// IsIdentity checks if matrix is identity within tolerance
func (m *Matrix) IsIdentity(tolerance float64) bool {
	if m.Rows != m.Cols {
		return false
	}
	for i := 0; i < m.Rows; i++ {
		for j := 0; j < m.Cols; j++ {
			expected := 0.0
			if i == j {
				expected = 1.0
			}
			if m.Data[i][j] > expected+tolerance || m.Data[i][j] < expected-tolerance {
				return false
			}
		}
	}
	return true
}

// ModuleSplitter implements the splitting theorem
type ModuleSplitter struct {
	LDim, NDim, MDim int
}

// NewModuleSplitter creates a new splitter instance
func NewModuleSplitter(lDim, nDim int) *ModuleSplitter {
	return &ModuleSplitter{
		LDim: lDim,
		NDim: nDim,
		MDim: lDim + nDim,
	}
}

// CreateMaps creates the standard maps
func (ms *ModuleSplitter) CreateMaps() (alpha, beta, sigma, rho *Matrix) {
	// α: L → M (inclusion)
	alpha = NewMatrix(ms.MDim, ms.LDim)
	for i := 0; i < ms.LDim; i++ {
		alpha.Data[i][i] = 1.0
	}

	// β: M → N (projection)
	beta = NewMatrix(ms.NDim, ms.MDim)
	for i := 0; i < ms.NDim; i++ {
		beta.Data[i][ms.LDim+i] = 1.0
	}

	// σ: N → M (inclusion)
	sigma = NewMatrix(ms.MDim, ms.NDim)
	for i := 0; i < ms.NDim; i++ {
		sigma.Data[ms.LDim+i][i] = 1.0
	}

	// ρ: M → L (projection)
	rho = NewMatrix(ms.LDim, ms.MDim)
	for i := 0; i < ms.LDim; i++ {
		rho.Data[i][i] = 1.0
	}

	return alpha, beta, sigma, rho
}

// VerifyTheorem checks all conditions concurrently
func (ms *ModuleSplitter) VerifyTheorem(alpha, beta, sigma, rho *Matrix) bool {
	tolerance := 1e-10
	var wg sync.WaitGroup
	results := make(chan bool, 5)

	// Check βα = 0
	wg.Add(1)
	go func() {
		defer wg.Done()
		ba := beta.Multiply(alpha)
		results <- ba.IsZero(tolerance)
	}()

	// Check βσ = 1
	wg.Add(1)
	go func() {
		defer wg.Done()
		bs := beta.Multiply(sigma)
		results <- bs.IsIdentity(tolerance)
	}()

	// Check ρσ = 0
	wg.Add(1)
	go func() {
		defer wg.Done()
		rs := rho.Multiply(sigma)
		results <- rs.IsZero(tolerance)
	}()

	// Check ρα = 1
	wg.Add(1)
	go func() {
		defer wg.Done()
		ra := rho.Multiply(alpha)
		results <- ra.IsIdentity(tolerance)
	}()

	// Check αρ + σβ = 1
	wg.Add(1)
	go func() {
		defer wg.Done()
		ar := alpha.Multiply(rho)
		sb := sigma.Multiply(beta)
		arPlusSb := ar.Add(sb)
		results <- arPlusSb.IsIdentity(tolerance)
	}()

	wg.Wait()
	close(results)

	allTrue := true
	for result := range results {
		allTrue = allTrue && result
	}
	return allTrue
}

func main() {
	splitter := NewModuleSplitter(2, 3)
	alpha, beta, sigma, rho := splitter.CreateMaps()

	fmt.Println("Module Splitting Theorem - Go Implementation")
	fmt.Printf("Dimensions: L=%d, N=%d, M=%d\n", splitter.LDim, splitter.NDim, splitter.MDim)

	if splitter.VerifyTheorem(alpha, beta, sigma, rho) {
		fmt.Println("✓ All conditions satisfied: M = L ⊕ N")
	} else {
		fmt.Println("✗ Conditions failed")
	}
}
