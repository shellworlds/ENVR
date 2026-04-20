#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
  if (argc < 2) return 1;
  std::ifstream f(argv[1]);
  std::string s((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
  std::cout << "bytes=" << s.size() << std::endl;
  return 0;
}
