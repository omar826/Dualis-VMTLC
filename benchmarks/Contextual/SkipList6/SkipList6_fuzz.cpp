#include "../../FuzzImpl/SkipListImpl.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <unistd.h>

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;

   std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);
  if (!ceFile.is_open()) {
    std::cerr << "Error: Unable to open log file." << std::endl;
    return 1;
  }

  // AFL persistent loop
  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen < 4) {
      continue;
    }

    SkipList sl;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if (N <= 0) { // Add safety check
        continue;
    }

    
    for (int i = 0; i < N; ++i) {
      DECLARE_SL_INSERT_STATE_VARS();
      READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -2, v);
      v = 1;
      SL_INSERT_WITH_STATE(sl, v);
        bool expr_insert = (false);
        
        if (!expr_insert) {
          LOG_SL_INSERT_STATE(ceFile, fuzzer_mode);
        }
        assert(expr_insert);
    }
        
    {
      DECLARE_SL_REMOVE_STATE_VARS();
      k = 1;
      SL_REMOVE_WITH_STATE(sl, k);
      bool expr_remove = (true);
        
      if (!expr_remove) {
	LOG_SL_REMOVE_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_remove);
    }
  }
  ceFile.close();
  return 0;
}
