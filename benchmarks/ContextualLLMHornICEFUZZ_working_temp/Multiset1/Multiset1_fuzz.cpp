#include "../../FuzzImpl/MultiSetImpl.h" // Assumed path to your Impl header
#include <set>                     // For std::multiset
#include <vector>                  // For fuzzBuf
#include <fstream>                 // For std::ofstream
#include <iostream>                // For std::cerr
#include <cassert>                 // For assert
#include <cstdint>                 // For int8_t

// Note: Assumes MultiSetImpl.h provides:
// - All DECLARE/MS/LOG macros
// - read_int8()
// - READ_INT8_FROM_FUZZBUF()

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;

  if (argc < 2) {
    std::cerr << "Error: Please provide a file path for logging." << std::endl;
    return 1;
  }
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

    if (fuzzLen <= 12) {
      continue;
    }

    std::multiset<int> set;

    int8_t N;
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if (N <= 0) {
      continue;
    }
        
    int8_t v_from_fuzz;
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -2, v_from_fuzz);
    int v_val = v_from_fuzz; // This value is constant for the whole loop

    for (int i = 0; i < N; ++i) {
      DECLARE_MS_EMPLACE_STATE_VARS();
      READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -3, v);
      MS_EMPLACE_WITH_STATE(set, v%128);
      bool expr_emplace = (countv1 == countv + 1 && len1 == len + 1);
      if (!expr_emplace) {
	LOG_MS_EMPLACE_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_emplace);
    }
    fuzzBuf.clear();
  }
  ceFile.close();
  return 0;
}
