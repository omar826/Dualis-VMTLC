#include "../../FuzzImpl/RedBlackTreeImpl.h"
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

    RedBlackTree rbt;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if (N <= 0) { // Added this check for safety
      continue;
    }

    for (int i_loop = 0; i_loop < N; ++i_loop) {

      DECLARE_RBT_INSERT_STATE_VARS();
      RBT_INSERT_WITH_STATE(rbt, i_loop);

      bool expr_insert = (true);
        
      if (!expr_insert) {
	LOG_RBT_INSERT_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_insert);
    }
        
    {
      DECLARE_RBT_SEARCH_STATE_VARS();

      uint8_t data_raw;
      READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, data_raw);
      data = data_raw % N;
      RBT_SEARCH_WITH_STATE(rbt, data);

      bool expr_search = (true);
        
      if (!expr_search) {
	LOG_RBT_SEARCH_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_search);
    }
  }
  ceFile.close();
  return 0;
}
