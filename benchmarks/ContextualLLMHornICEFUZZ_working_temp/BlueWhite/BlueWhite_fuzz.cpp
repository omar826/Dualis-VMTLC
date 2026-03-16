#include "../../FuzzImpl/BlueWhiteImpl.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint> // For uint8_t
#include <unistd.h>  // For read

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;

  // FIX 1: Hardcode the log file path.
  // Relying on argv[1] is problematic for AFL.
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);
  if (!ceFile.is_open()) {
    std::cerr << "Error: Unable to open log file: " << filePath << std::endl;
    return 1;
  }

  // AFL persistent loop
  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen < 5) {
      continue;
    }

    BWList bwl;
        
    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, N);

    if (N <= 0){
      continue;
    }

    // FIX 2 (cont.): Add the dynamic length check.
    if (static_cast<size_t>(N + 3) >= static_cast<size_t>(fuzzLen)) {
      continue;
    }
    
    // FIX 3: Fix the 'inserted_blue' logic.
    // The old code read a random byte from [fL-2] and then required
    // it to be 0. This is a "fuzzer blockade" that rejects 255/256
    // of all inputs.
    // This is clearly meant to be a state-tracking variable,
    // so we initialize it to 'false'.
    bool inserted_blue = false;
    // READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, inserted_blue); // <-- REMOVED
    // if (inserted_blue != 0) { // <-- REMOVED
    //   continue;
    // }

    unsigned int current_offset = 2;
    for (int i = 0; i < N; ++i) {
      uint8_t color_raw;
      READ_UINT8_FROM_FUZZBUF(fuzzBuf, current_offset, color_raw);
      current_offset++; // Advance offset for next iteration

      if (color_raw == 0 || color_raw == 1){
        int color_val = color_raw;

        if (color_val == 0 && !inserted_blue) {
          DECLARE_BWL_PUSH_STATE_VARS();
          BWL_PUSH_WITH_STATE(bwl, 0);
          bool expr_push = bcount1 == (color == 0 ? bcount + 1 : bcount);

          if (!expr_push) {
            LOG_BWL_PUSH_STATE(ceFile, fuzzer_mode);
          }
          assert(expr_push);

          inserted_blue = bwl.blue_present();
        } 
        else if (color_val == 1) {
          DECLARE_BWL_PUSH_STATE_VARS();
          BWL_PUSH1_WITH_STATE(bwl, 1);

          bool expr_push1 = bcount1 == bcount;

          if (!expr_push1) {
            LOG_BWL_PUSH1_STATE(ceFile, fuzzer_mode);
          }
          assert(expr_push1);
        }
      }
    }
  }
  ceFile.close();
  return 0;
}
