#include "../../FuzzImpl/StackImpl.h"

int main(int argc, char *argv[]) {

  bool fuzzer_mode = getenv("FUZZING") != nullptr;

  std::string filePath = argv[1];
  std::cout << "Output file path: " << filePath << std::endl;
    
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen <= 3) continue;

    Stack st;
    init(st, fuzzBuf, fuzzLen);

    DECLARE_STACK_PUSH_STATE_VARS();
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -2, N);
    STACK_PUSH_WITH_STATE(st, N);

    bool expr = sl1 == sl + 1;
        
    if (!expr) {
      if (ceFile.is_open()) {
	LOG_STACK_PUSH_STATE(ceFile, fuzzer_mode);
      }
    }
    assert(expr);
    fuzzBuf.clear();
  }
  ceFile.close();
  return 0;
}
