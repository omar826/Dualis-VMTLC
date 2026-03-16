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

    DECLARE_SL_INSERT_STATE_VARS();

    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, v);

    SL_INSERT_WITH_STATE(sl, v);

    bool expr = ((len1 == len + 1) && (min1 == (v < min ? v : min)) && (max1 == (v > max ? v : max)) && (isPresent1 == 1));

    if (!expr) {
      LOG_SL_INSERT_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);
  }

  ceFile.close();
  return 0;
}
