#include "../../FuzzImpl/MaxImpl.h" // MAPPING: Path changed to FuzzImpl

int main(int argc, char* argv[])
{
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  
  string filePath = argv[1];
  cout << "Final Path: " << filePath << endl;

  ofstream ceFile(filePath, ios::app);
  if (!ceFile) {
    return 1;
  }

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());


    if (fuzzLen <= 4) {
        continue;
    }

    Max mx;
    init(mx, fuzzBuf, fuzzLen-2);

    DECLARE_MAXL_APPEND_STATE_VARS();
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, v);

    MAXL_APPEND_WITH_STATE(mx, v);
    
    bool expr = lmax1 == (v > lmax ? v : lmax);

    if(!expr){
      if (ceFile.is_open()){
        LOG_MAXL_APPEND_STATE(ceFile, fuzzer_mode);
      }
    }
    
    assert(expr);
    fuzzBuf.clear();
  }
  ceFile.close();
  return 0;
}
