#include "../../FuzzImpl/FlatHashMapImpl.h"

int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
    
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen <= 10) {
      continue;
    }

    FlatHashMap fhm;

    int8_t N_raw;
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, N_raw);
    
    // FIX 1: Cap N and strictly enforce the CHC (assume N > 1)
    int8_t N = N_raw % 128;
    if (N <= 1) { 
      continue;
    }
        
    // --- LOOP 1: INSERTION ---
    int i = 0;
    while (i < N) {
      DECLARE_FHM_INSERT_STATE_VARS();
      
      // FIX 2: Stop guessing. Force k and v to equal i.
      k = i;
      v = i;
      
      FHM_INSERT_WITH_STATE(fhm, k, v);

      bool expr_insert = (false); // Set to false so Python injects here!

      if (!expr_insert) {
        LOG_FHM_INSERT_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_insert);
      
      i++;
    }

    // --- LOOP 2: ERASURE ---
    i = 0;
    int gflag = 0; // Starts at 0, per the CHC!

    while(i < N) {
      // FIX 3: The CHC only erases when flag == 1.
      if (gflag == 1) {
        DECLARE_FHM_ERASE_STATE_VARS();
        
        k = i;
        flag = gflag; // Pass the current state of the flag

        FHM_ERASE_WITH_STATE(fhm, k, flag);
        
        bool expr_erase = (false); // Set to false so Python injects here!
              
        if (!expr_erase) {
          LOG_FHM_ERASE_STATE(ceFile, fuzzer_mode);
        }
        assert(expr_erase);
      }
      
      i++;
      gflag = 1 - gflag; // Toggle flag 0 -> 1 -> 0 -> 1
    }
    fuzzBuf.clear();
  }

  ceFile.close();
  return 0;
}
