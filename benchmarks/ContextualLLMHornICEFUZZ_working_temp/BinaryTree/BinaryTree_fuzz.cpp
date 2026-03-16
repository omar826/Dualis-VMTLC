#include "../../FuzzImpl/BinaryTreeImpl.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint> // For uint8_t/int8_t
#include <unistd.h>  // For read

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;


  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);
  if (!ceFile.is_open()) {
    std::cerr << "Error: Unable to open log file: " << filePath << std::endl;
    return 1;
  }

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen < 6) {
      continue;
    }

    BinaryTree bt;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, N);

    if(N <= 0){
      continue;
    }

    if (static_cast<size_t>(N + 4) >= static_cast<size_t>(fuzzLen)) {
      continue;
    }

    unsigned int current_offset = 2; // Kept from original
    for (int i = 0; i < N; ++i) {
      int8_t n_raw;
      READ_INT8_FROM_FUZZBUF(fuzzBuf, current_offset, n_raw);
      current_offset++; // Advance offset for next iteration
      
      if (n_raw >= 0) {
        
        DECLARE_BT_INSERT_STATE_VARS();
        

        n = n_raw; 
        
        BT_INSERT_WITH_STATE(bt, n);
        

	bool expr_insert = (isEmpty1 == 0 && min1 == (isEmpty == 1 ? n : (n < min ? n : min)));

        if (!expr_insert) {
          if (ceFile.is_open()) {
             LOG_BT_INSERT_STATE(ceFile, fuzzer_mode);
          }
        }
        assert(expr_insert);
      }
    }
    
    {
      int8_t v_raw;
      READ_INT8_FROM_FUZZBUF(fuzzBuf, current_offset, v_raw);
      
      if (v_raw >= 0){
        continue;
      }
      
      DECLARE_BT_SEARCH_STATE_VARS();
      v = v_raw;
      BT_SEARCH_WITH_STATE(bt, v);
      
      bool expr_search = ret1 == 0;

      if (!expr_search) {
        if (ceFile.is_open()) {
          LOG_BT_SEARCH_STATE(ceFile, fuzzer_mode);
        }
      }
      assert(expr_search);
    }
  }

  ceFile.close();
  return 0;
}
