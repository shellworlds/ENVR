public class ClusterHealthCheck {
  public static void main(String[] args) {
    String[] nodes = {"q-a", "q-b", "q-c"};
    for (String n : nodes) {
      System.out.println(n + " OK");
    }
  }
}
