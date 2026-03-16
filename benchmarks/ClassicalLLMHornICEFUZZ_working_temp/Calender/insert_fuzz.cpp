#include "../../FuzzImpl/CalenderImpl.h" // MAPPING: Path changed to FuzzImpl

int main(int argc, char* argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  if (argc < 2) { // Check for file path
    return 1;
  }
  std::string filePath = argv[1];
    
  std::ofstream ceFile(filePath, std::ios::app);
  if (!ceFile) {
    return 1;
  }

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen <= 6) {
      continue;
    }

    Cal cal;
    init(cal, fuzzBuf, fuzzLen-2);

    DECLARE_CAL_INSERT_STATE_VARS();
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, ev1);
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, ev2);
        
    CAL_INSERT_WITH_STATE(cal, ev1, ev2);
        
    bool expr = (len1 == len + 1 && maxDiff1 == (maxDiff > (ev1 - ev2 >= 0 ? ev1 - ev2 : -(ev1 - ev2)) ? maxDiff : (ev1 - ev2 >= 0 ? ev1 - ev2 : -(ev1 - ev2))));

    if (!expr) {
      if (ceFile.is_open()) {
	LOG_CAL_INSERT_STATE(ceFile, fuzzer_mode);
      }
    }
  
    assert(expr);
    fuzzBuf.clear();
  }

  ceFile.close(); // Correct placement
  return 0;
}
