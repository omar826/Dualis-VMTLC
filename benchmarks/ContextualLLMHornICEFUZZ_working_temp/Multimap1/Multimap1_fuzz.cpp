#include "../../FuzzImpl/MultiMapImpl.h" // Assumed path to your header file

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

    if (fuzzLen <= 10) {
      continue;
    }

    std::multimap<int, int> map;

    int8_t N;
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen-1, N);

    if (N <= 0) {
      continue;
    }
        
    unsigned int current_offset = 2;

    for (int i = 0; i < N; ++i) {
            
      if (current_offset >= fuzzLen) {
	break; // Stop loop if we run out of data
      }

      int8_t v_from_fuzz;
      READ_INT8_FROM_FUZZBUF(fuzzBuf, current_offset, v_from_fuzz);
      current_offset++;
      DECLARE_MM_EMPLACE_STATE_VARS();
      READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, k);
      k = 1;
      v = v_from_fuzz;
      MM_EMPLACE_WITH_STATE(map, k, v%128);
      bool expr_emplace = (countko1 == countko + 1 && len1 == len + 1);

      if (!expr_emplace) {
	LOG_MM_EMPLACE_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_emplace);
    }        
    fuzzBuf.clear();
  }
  ceFile.close();
  return 0;
}
