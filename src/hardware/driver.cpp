#include <iostream>
#include <chrono>
#include <thread>

class Keithley2400Mock {
public:
    double measure_voltage() {
        return 0.452; // mA bias voltage
    }
};

int main() {
    Keithley2400Mock keithley;
    while (true) {
        std::cout << "JPA Bias: " << keithley.measure_voltage() << " mA" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(2));
    }
    return 0;
}
