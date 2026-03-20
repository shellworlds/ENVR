#include <cmath>
#include <iostream>

int main() {
  double theta = 0.7;
  double p0 = std::pow(std::cos(theta / 2.0), 2.0);
  std::cout << "p0=" << p0 << std::endl;
  return 0;
}
