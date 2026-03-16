#include "../../FuzzImpl/SkipListImpl.h"

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());
    if (fuzzLen < 9) continue;
    SkipList sl;
    init(sl, fuzzBuf, fuzzLen - 2);

    DECLARE_SL_REMOVE_STATE_VARS();

    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, k);

    SL_REMOVE_WITH_STATE(sl, k);
      
    bool expr = ((len == 1 && k == min && k == max) ? (len1 == 0 && min1 == 128 && max1 == -129 && ret1 == 1) : (len1 == len && min1 == min && max1 == max && ret1 == 0));

    if (!expr) {
      LOG_SL_REMOVE_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);  
  }
  ceFile.close();
  return 0;
}
