#include "../../FuzzImpl/DLL_CircularImpl.h"
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

    DLLCircular dlc;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if (N <= 0) {
        continue;
    }

    if (static_cast<size_t>(N + 4) >= static_cast<size_t>(fuzzLen)) {
        continue;
    }

    unsigned int current_offset = 2;
    
    int current_val = 0;

    for (int i = 0; i < N; ++i) {
      uint8_t condition_raw;
      READ_UINT8_FROM_FUZZBUF(fuzzBuf, current_offset, condition_raw);
      current_offset++; // Advance offset for next iteration
          
      bool condition = (condition_raw % 2);
      
      if (condition) {
        if (current_val < 3) {
          current_val = current_val + 1;
        }
      }
            
      DECLARE_DLC_PUSH_STATE_VARS();
            
      val = current_val; 

      DLC_PUSH_WITH_STATE(dlc, current_val);

      bool expr_push = max_out == (val_in > max_in ? val_in : max_in);
      
      if (!expr_push) {
        LOG_DLC_PUSH_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_push);
    }
        
  }

  ceFile.close();
  return 0;
}
