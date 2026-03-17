#include "../../FuzzImpl/AtomicHashMapImpl.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint> // For uint8_t
#include <unistd.h>  // For read

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

    if (fuzzLen < 6) {
      continue;
    }
        
    HashTable ahm;
    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, N);

    if (N <= 0 || N >= 128) {
      continue;
    }

    if (static_cast<size_t>((N * 2) + 3) >= static_cast<size_t>(fuzzLen)) {
      continue;
    }

    unsigned int current_offset = 2;

    for (int i = 0; i < N; ++i) {
      DECLARE_AHM_INSERT_STATE_VARS();
      k = i;
      v = i;
      AHM_INSERT_WITH_STATE(ahm, k, v);
            
      bool expr_insert = (true);
            
      if (!expr_insert) {
	LOG_AHM_INSERT_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_insert);
    }

    for (int i = 0; i < N; ++i) {
      DECLARE_AHM_INSERT1_STATE_VARS();
            
      k = i;
      v = i;

      AHM_INSERT1_WITH_STATE(ahm, k, v);
      bool expr_insert1 = (true);
      if (!expr_insert1) {
	LOG_AHM_INSERT1_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_insert1);
    }

    if (N > 0) {
      DECLARE_AHM_FIND_STATE_VARS();
      k = ahm.maxKey();
      AHM_FIND_WITH_STATE(ahm, k); 
      bool expr_find = (false);
      if (!expr_find) {
	LOG_AHM_FIND_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_find);
    }
  }
  ceFile.close();
  return 0;
}
