#include "../../FuzzImpl/TokenBucketImpl.h"
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

    if (fuzzLen < 3) {
      continue;
    }

    TokenBucket tb;

    uint8_t b_size_raw;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, 1, b_size_raw);
       
    uint8_t c_rate_raw;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, 2, c_rate_raw);

       
    if (!(b_size_raw >= c_rate_raw)) {
      continue;
    }
    {
      DECLARE_TB_GENERATETOKENS_STATE_VARS();
      b_size = b_size_raw;

      TB_GENERATETOKENS_WITH_STATE(tb, b_size);
	    
      bool expr_generateTokens = avai_tokens1 == b_size;
            
      if (!expr_generateTokens) {
	LOG_TB_GENERATETOKENS_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_generateTokens);
    }
       
    int current_avai_tokens = tb.getAvailableTokens();
       
    while (current_avai_tokens >= c_rate_raw) {
           
      DECLARE_TB_CONSUME_STATE_VARS();
      c_rate = c_rate_raw;

      TB_CONSUME1_WITH_STATE (tb, c_rate);
      bool expr_consume = avai_tokens1 == (avai_tokens - c_rate);
            
      if (!expr_consume) {
	LOG_TB_CONSUME_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_consume);
      current_avai_tokens = avai_tokens1;
    }
  }

  ceFile.close();
  return 0;
}
