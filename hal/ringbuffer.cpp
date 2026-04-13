#include <iostream>
#include <vector>
#include <atomic>

template<typename T>
class RingBuffer {
    std::vector<T> buffer;
    std::atomic<size_t> head{0};
    std::atomic<size_t> tail{0};
    const size_t capacity;
public:
    RingBuffer(size_t cap) : buffer(cap), capacity(cap) {}
    bool push(const T& item) {
        size_t current_tail = tail.load();
        size_t next_tail = (current_tail + 1) % capacity;
        if (next_tail == head.load()) return false;
        buffer[current_tail] = item;
        tail.store(next_tail);
        return true;
    }
};

int main() {
    RingBuffer<int> rb(1024);
    rb.push(42);
    std::cout << "Ring buffer initialized." << std::endl;
    return 0;
}
