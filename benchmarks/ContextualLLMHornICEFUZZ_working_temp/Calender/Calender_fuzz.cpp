#include "../../FuzzImpl/CalenderImpl.h"
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

  // AFL persistent loop
  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen < 4) {
      continue;
    }

    Cal cal;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, 1, N);

    if (N <= 0) {
        continue;
    }

    if (static_cast<size_t>(2 + (N * 2)) > static_cast<size_t>(fuzzLen)) {
        continue;
    }

    unsigned int current_offset = 2;

    for (int i = 0; i < N; ++i) {
      uint8_t ev1_val;
      READ_UINT8_FROM_FUZZBUF(fuzzBuf, current_offset, ev1_val);
      current_offset++;

      uint8_t ev2_val;
      READ_UINT8_FROM_FUZZBUF(fuzzBuf, current_offset, ev2_val);
      current_offset++;

      if (((ev1_val >= 0 && ev1_val <= 3) && (ev2_val >= 0 && ev2_val <= 3)) &&
      ((ev1_val - ev2_val) < 2)) 
    {
      DECLARE_CAL_INSERT_STATE_VARS();
      ev1 = ev1_val;
      ev2 = ev2_val;
      CAL_INSERT_WITH_STATE(cal, ev1, ev2);


      bool expr_insert = ((len1 == len + 1) && (maxDiff1 == ((maxDiff > ((ev1 - ev2 >= 0) ? (ev1 - ev2) : -(ev1 - ev2))) ? maxDiff : ((ev1 - ev2 >= 0) ? (ev1 - ev2) : -(ev1 - ev2)))));

      if (!expr_insert) {
        LOG_CAL_INSERT_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_insert);
    }
    }

  }

  ceFile.close();
  return 0;
}
