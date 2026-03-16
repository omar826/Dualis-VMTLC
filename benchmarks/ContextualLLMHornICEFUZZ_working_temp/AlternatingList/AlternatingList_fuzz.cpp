#include "../../FuzzImpl/AlternatingListImpl.h"

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

    
  while (__AFL_LOOP(10000)) {
    std::vector<uint8_t> fuzzBuf(4096);
    ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

    if (fuzzLen <= 10) {
      continue;
    }

    AlternatingList al;
        
    uint8_t loop_count;
    READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen-1, loop_count);
    int flag = 1;
    for (int i = 0; i < loop_count; ++i) {
      if (flag) {
	DECLARE_AL_PUSH_STATE_VARS();
	val = 1;
	AL_PUSH_WITH_STATE(al, val);
	bool expr_push = (top1 == val && len1 == len + 1);
	if (!expr_push) {
	  LOG_AL_PUSH_STATE(ceFile, fuzzer_mode);
	}
	assert(expr_push);
      } else {
	DECLARE_AL_PUSH1_STATE_VARS();
	val = 2;
	AL_PUSH1_WITH_STATE(al, val);
	bool expr_push1 = (top1 == val && len1 == len + 1);
	if (!expr_push1) {
	  LOG_AL_PUSH1_STATE(ceFile, fuzzer_mode);
	}
	assert(expr_push1);
      }
      flag = !flag;
    }
    fuzzBuf.clear();
  }
  ceFile.close();
  return 0;
}
