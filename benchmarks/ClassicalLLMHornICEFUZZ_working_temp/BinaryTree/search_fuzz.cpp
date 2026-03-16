#include "../../FuzzImpl/BinaryTreeImpl.h"
int main(int argc, char *argv[]) {
  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);

  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096); //reserving the vector size improves stability
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzBuf.size() < 4) continue;

    BinaryTree bt;
    init(bt, fuzzBuf, fuzzLen - 2);

    DECLARE_BT_SEARCH_STATE_VARS();
     
    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, v);

    BT_SEARCH_WITH_STATE(bt, v);

    bool expr = (!(isEmpty == 1 || v < min) || (ret1 == 0));
        
    if (!expr) {
      LOG_BT_SEARCH_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);
  }
  ceFile.close();
  return 0;
}
