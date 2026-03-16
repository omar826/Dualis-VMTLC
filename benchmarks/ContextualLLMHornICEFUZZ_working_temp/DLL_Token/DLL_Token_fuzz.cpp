#include "../../FuzzImpl/DLL_TokenImpl.h"
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


    if (fuzzLen < 3) {
      continue;
    }

    DLLTok dt;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if (N <= 0){
      continue;
    }

    for (int i = 0; i < N; ++i) {
      DECLARE_DLT_PUSH_STATE_VARS();
      val = 0;
      DLT_PUSH_WITH_STATE(dt, val);
            
      bool expr_push = (len1 == len + 1 && (len == 0 ? (min1 == val && max1 == val) : (min1 == (val < min ? val : min) && max1 == (val > max ? val : max))));

      if (!expr_push) {
	LOG_DLT_PUSH_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_push);
    }
  }

  ceFile.close();
  return 0;
}
