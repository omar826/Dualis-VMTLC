#include "../../FuzzImpl/MultiSetImpl.h" // Assumed path to your Impl header
#include <set>           // For std::multiset
#include <vector>        // For fuzzBuf
#include <fstream>       // For std::ofstream
#include <iostream>      // For std::cerr
#include <cassert>       // For assert
#include <cstdint>       // For int8_t/uint8_t

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

    std::multiset<int> set;

    uint8_t N;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);
    if (N <= 0 || N >= 128) {
      continue;
    }
        
    for (int i = 0; i < N; ++i) {
      DECLARE_MS_EMPLACE1_STATE_VARS();
      v = 1;
      MS_EMPLACE1_WITH_STATE(set, v%128);

      bool expr_emplace = (v == 1 ? ((countvo1 == countvo + 1) && (countvt1 == countvt) && (len1 == len + 1)) : (v == 2 ? ((countvo1 == countvo) && (countvt1 == countvt + 1) && (len1 == len + 1)) : false));
        
      if (!expr_emplace) {
	LOG_MS_EMPLACE1_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_emplace);
    }
    {
      DECLARE_MS_EMPLACE1_STATE_VARS();
      v = 2;
      
      MS_EMPLACE1_WITH_STATE(set, v%128);

      bool expr_emplace1 = (v == 1 ? (countvo1 == countvo + 1 && countvt1 == countvt && len1 == len + 1) : (v == 2 ? (countvo1 == countvo && countvt1 == countvt + 1 && len1 == len + 1) : false));
        
      if (!expr_emplace1) {
	LOG_MS_EMPLACE2_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_emplace1);
    }
        
  }

  ceFile.close();
  return 0;
}
