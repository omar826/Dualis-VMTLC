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

    int8_t N;
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, N);

    if (N <= 0){
      continue;
    }
        
    int i = 0;
    while (i < N) {
      DECLARE_FHM_INSERT_STATE_VARS();
      
      // FIX: Force k and v to equal i, perfectly matching CHC: (= k i) (= v i)
      k = i;
      v = i;
      
      FHM_INSERT_WITH_STATE(fhm, k, v);

      bool expr_insert = (false);
      if (!expr_insert) {
        LOG_FHM_INSERT_STATE(ceFile, fuzzer_mode);
      }
      assert(expr_insert);
      
      i++;
    }

    // --- LOOP 2: ERASURE ---
    i = 0;
    int gflag = 1;

    while(i < N) {
      // FIX: The CHC only calls erase when flag == 1
      if (gflag == 1) {
          DECLARE_FHM_ERASE_STATE_VARS();
          k = i;
          
          FHM_ERASE_WITH_STATE(fhm, k, gflag);

          bool expr_erase = (false); 
          if (!expr_erase) {
            LOG_FHM_ERASE_STATE(ceFile, fuzzer_mode);
          }
          assert(expr_erase);
      }           
      i++;
      gflag = 1 - gflag; 
    }
    fuzzBuf.clear();
  }
  ceFile.close();
}
