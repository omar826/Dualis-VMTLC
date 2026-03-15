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

    DECLARE_BH_DELETEMIN_STATE_VARS();

    BH_DELETEMIN_WITH_STATE(bh);
    
    bool expr = (len1 == len_var - 1 && isHeap1 == false);
    if (!expr) {
      LOG_BH_DELETEMIN_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);
  }
  ceFile.close();
  return 0;
}
