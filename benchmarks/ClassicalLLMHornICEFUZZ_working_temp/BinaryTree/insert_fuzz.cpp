#include "../../FuzzImpl/BinaryTreeImpl.h"
int main(int argc, char *argv[]) {
  // if (argc < 2) {
  //   std::cerr << "Usage: " << argv[0] << " <output_file_path>" << std::endl;
  //   return 1;
  //}

  bool fuzzer_mode = getenv("FUZZING") != nullptr;
  std::string filePath = argv[1];
  std::ofstream ceFile(filePath, std::ios::app);
    
  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen <= 4) continue;
    BinaryTree bt;
    init(bt, fuzzBuf, fuzzLen-2);

    DECLARE_BT_INSERT_STATE_VARS();

    READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, n);

    BT_INSERT_WITH_STATE(bt, n);
    bool expr = (isEmpty1 == 0 && min1 == (n < min ? n : min));

    if (!expr) {
      LOG_BT_INSERT_STATE(ceFile, fuzzer_mode);
    }
    fuzzBuf.clear();
    assert(expr);  
  }
  ceFile.close();
  return 0;
}
