#include "../../FuzzImpl/StackImpl.h"
int main(int argc, char *argv[]) {

  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen <= 3) continue;

    Stack st;
    init(st, fuzzBuf, fuzzLen);

    DECLARE_STACK_POP_STATE_VARS();
    STACK_POP_WITH_STATE(st);
        
    bool expr = sl1 == sl - 1;
        
    if (!expr) {
      LOG_STACK_POP_STATE(ceFile, fuzzer_mode);
    }
    assert(expr);
    fuzzBuf.clear();
  }
  ceFile.close();
  return 0;
}
