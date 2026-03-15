#include "../../FuzzImpl/BinaryHeapImpl.h"

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());
    if (fuzzLen < 6) continue;
    BinaryHeap bh;

    init(bh, fuzzBuf, fuzzLen-2);

    DECLARE_BH_INSERT_STATE_VARS();

    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, i);

    BH_INSERT_WITH_STATE(bh, i);
    
    bool expr = ((len1 == len_var + 1) && (isHeap1 == isHeap));
    if (!expr) {
      LOG_BH_INSERT_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);
  }
  ceFile.close();
  return 0;
}
