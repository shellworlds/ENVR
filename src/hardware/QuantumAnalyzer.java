public class QuantumAnalyzer {
    private double fluxQuantum = 2.067833848e-15; // Wb

    public double calculateShapiroStep(double frequency, int step) {
        return step * frequency * fluxQuantum;
    }

    public static void main(String[] args) {
        QuantumAnalyzer qa = new QuantumAnalyzer();
        System.out.println("Shapiro step voltage: " + qa.calculateShapiroStep(10e9, 1));
    }
}
