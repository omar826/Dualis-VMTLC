#include "../../FuzzImpl/FlatHashMapImpl.h"

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen <= 7) continue;

    FlatHashMap fhm;
    init(fhm, fuzzBuf, fuzzLen - 2);

    DECLARE_FHM_REMOVENONE_STATE_VARS();

    FHM_REMOVENONE_WITH_STATE(fhm);
        
    bool expr = ((len1 == len) && (remove_count1 == remove_count));

    if (!expr) {
      LOG_FHM_REMOVENONE_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);
  }
  ceFile.close();
  return 0;
}
