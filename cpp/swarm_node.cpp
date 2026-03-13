// SN-112BA Swarm node (C++). Main developer: shellworlds.
#include <iostream>
#include <vector>
#include <cmath>

double pso_objective(const std::vector<double>& x) {
    double s = 0.0;
    for (double v : x) s += v * v;
    return s;
}

int main() {
    std::vector<double> pos = { 0.1, 0.2, -0.1 };
    double f = pso_objective(pos);
    std::cout << "SN-112BA Swarm node objective: " << f << std::endl;
    return 0;
}
