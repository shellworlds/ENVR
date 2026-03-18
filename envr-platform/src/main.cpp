// ENVR C++ probe: g++ -std=c++17 -o probe main.cpp && ./probe
#include <iostream>
#ifdef __linux__
#include <sys/utsname.h>
#endif

int main() {
    std::cout << "ENVR C++ probe OK\n";
#ifdef __linux__
    struct utsname u{};
    if (uname(&u) == 0) {
        std::cout << "kernel " << u.release << " " << u.machine << "\n";
    }
#endif
    return 0;
}
