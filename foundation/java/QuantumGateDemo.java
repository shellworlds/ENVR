public class QuantumGateDemo {
  public static void main(String[] args) {
    double theta = 1.2;
    double prob0 = Math.pow(Math.cos(theta / 2.0), 2);
    System.out.println("P(|0>)=" + prob0);
  }
}
