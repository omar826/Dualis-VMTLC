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

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen < 3) {
      continue;
    }

    SkipList sl;

    uint8_t N_raw;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, N_raw);
    
    uint8_t N = N_raw % 128;

    if ( N <= 0){
      continue;
    }

    for (int i = 0; i < N; ++i) {
      DECLARE_SL_INSERT_STATE_VARS();
      v = 1;
      SL_INSERT_WITH_STATE(sl, v);
      bool expr_insert = (false);
      if (!expr_insert) {
	LOG_SL_INSERT_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_insert);
    }
  }

  ceFile.close();
  return 0;
}
