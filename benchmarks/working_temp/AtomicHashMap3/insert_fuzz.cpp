#include "../../FuzzImpl/AtomicHashMapImpl.h"

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());
    if (fuzzLen < 6) continue;
    HashTable ahm;
    init(ahm, fuzzBuf, fuzzLen);

    DECLARE_AHM_INSERT_STATE_VARS();

    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, k);
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, v);

    AHM_INSERT_WITH_STATE(ahm, k, v);

    bool expr = ((len == 0 || (k < min || k > max)) ? (len1 == len + 1 && min1 == (len == 0 ? k : (k < min ? k : min)) && max1 == (len == 0 ? k : (k > max ? k : max)) && kveq1 == ((k == v && (len == 0 || kveq == 1)) ? 1 : 0)) : (((len > 0 && max - min + 1 == len) && k >= min && k <= max) ? (len1 == len && min1 == min && max1 == max && kveq1 == kveq) : ((len1 == len && min1 == min && max1 == max && kveq1 == kveq) || (len1 == len + 1 && min1 == (len == 0 ? k : (k < min ? k : min)) && max1 == (len == 0 ? k : (k > max ? k : max)) && kveq1 == ((k == v && (len == 0 || kveq == 1)) ? 1 : 0)))));

    if (!expr) {
        LOG_AHM_INSERT_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);
  }
  ceFile.close();
  return 0;
}
