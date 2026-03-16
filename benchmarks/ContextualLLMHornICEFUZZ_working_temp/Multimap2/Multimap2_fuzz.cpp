#include "../../FuzzImpl/MultiMapImpl.h" // Assumed path to your Impl header
#include <map>           // For std::multimap
#include <vector>        // For fuzzBuf
#include <fstream>       // For std::ofstream
#include <iostream>      // For std::cerr
#include <cassert>       // For assert
#include <cstdint>       // For int8_t
#include <unistd.h>      // For read

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

    if (fuzzLen < 7) {
      continue;
    }

    std::multimap<int, int> map;

    int8_t N;
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if (N <= 0) {
      continue;
    }
    
    if (static_cast<size_t>(N + 5) >= static_cast<size_t>(fuzzLen)) {
      continue;
    }

    unsigned int current_offset = 2;

    for (int i = 0; i < N; ++i) {
            
      int8_t v_from_fuzz;
      READ_INT8_FROM_FUZZBUF(fuzzBuf, current_offset, v_from_fuzz);
      current_offset++; // Move to the next byte for the next iteration


      DECLARE_MM_EMPLACE1_STATE_VARS();
      k = 1;
      v = v_from_fuzz;
      MM_EMPLACE1_WITH_STATE(map, k, v%128);


      bool expr_emplace = (countko1 == countko + 1 && countkt1 == countkt && len1 == len + 1);
        
      if (!expr_emplace) {
	LOG_MM_EMPLACE1_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_emplace);
    }
        
    int8_t v_from_fuzz;
    READ_INT8_FROM_FUZZBUF(fuzzBuf, current_offset, v_from_fuzz);
    {
      DECLARE_MM_EMPLACE1_STATE_VARS();
      k = 2;
      v = v_from_fuzz;
      MM_EMPLACE1_WITH_STATE(map, k, v%128);

      bool expr_emplace1 = (countko1 == countko && countkt1 == countkt + 1 && len1 == len + 1);
        
      if (!expr_emplace1) {
	LOG_MM_EMPLACE2_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_emplace1);
    }
  }

  ceFile.close();
  return 0;
}
