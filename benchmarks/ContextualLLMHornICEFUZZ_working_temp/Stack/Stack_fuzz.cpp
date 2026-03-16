#include "../../FuzzImpl/StackImpl.h"
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

    Stack st;
    uint8_t N_val;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N_val);
    if (N_val <= 0) {
      continue;
    }
        
    if (static_cast<size_t>(N_val + 2) >= static_cast<size_t>(fuzzLen)) {
      continue;
    }
       
    unsigned int current_offset = 2;
    for (int c = 0; c < N_val; c++) {
      DECLARE_STACK_PUSH_STATE_VARS();
      N = N_val;
      current_offset++;
      STACK_PUSH_WITH_STATE(st, N);

      bool expr_pu = sl1 == sl + 1;
              
      if (!expr_pu) {
	LOG_STACK_PUSH_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_pu);
    }
       
    while (st.len() != 0) {
      DECLARE_STACK_POP_STATE_VARS();
           
      STACK_POP_WITH_STATE(st);

      bool expr_po = sl1 == sl - 1;
            
      if (!expr_po) {
	LOG_STACK_POP_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_po);
    }
  }
  ceFile.close();
  return 0;
}
