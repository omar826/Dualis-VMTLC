#include "../../FuzzImpl/FlatHashMapImpl.h"

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());
    if (fuzzLen <= 0) continue;

    if (fuzzLen < 7) continue;

    FlatHashMap fhm;
    init(fhm, fuzzBuf, fuzzLen - 2);

    DECLARE_FHM_INSERT_STATE_VARS();

    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, k);
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, v);

    FHM_INSERT_WITH_STATE(fhm, k, v);
        
    bool expr = (containsk1 == 1 && (!(k == v && k == len && containsk == 0) || (len1 == len + 1)));

    if (!expr) {
      LOG_FHM_INSERT_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);
  }
  ceFile.close();
  return 0;
}
