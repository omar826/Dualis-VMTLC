#include "../../FuzzImpl/MaxImpl.h"
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

    if (fuzzLen < 4) {
      continue;
    }

    Max ml;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if(N <= 0){
      continue;
    }
     
    if (static_cast<size_t>(N + 2) >= static_cast<size_t>(fuzzLen)) {
        continue;
    }
    
    unsigned int current_offset = 2;
        
    for (int i = 0; i < N; ++i) {
      int8_t v_val;
      READ_INT8_FROM_FUZZBUF(fuzzBuf, current_offset, v_val);
      current_offset++; // Advance offset for next iteration
              
      DECLARE_MAXL_APPEND_STATE_VARS();
              
      v = v_val; 

      MAXL_APPEND_WITH_STATE(ml, v_val);

      bool expr_append = lmax1 == (v > lmax ? v : lmax);

      if (!expr_append) {
        LOG_MAXL_APPEND_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_append);

    }
  }
  ceFile.close();
  return 0;
}
