#include "../../FuzzImpl/MultiMapImpl.h"

int main(int argc, char *argv[]) {
    bool fuzzer_mode = getenv("FUZZING") != nullptr;
    if (argc < 2) {
        std::cerr << "Error: Please provide a file path for logging." << std::endl;
        return 1;
    }
    std::string filePath = argv[1];
    
    std::ofstream ceFile(filePath, std::ios::app);
    if (!ceFile) {
        std::cerr << "Error: Unable to open log file." << std::endl;
        return 1;
    }

    while (__AFL_LOOP(10000)) {
        std::vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

        if (fuzzLen < 8) {
            continue;
        }

        std::multimap<int, int> map;
        init(map, fuzzBuf, fuzzLen-2);


	DECLARE_MM_EMPLACE1_STATE_VARS();
        READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, k);
	READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, v);
        MM_EMPLACE1_WITH_STATE(map, k, v);
        
        bool expr = (len1 == len + 1 && (k == 1 ? (countko1 == countko + 1 && countkt1 == countkt) : (k == 2 ? (countko1 == countko && countkt1 == countkt + 1) : (countko1 == countko && countkt1 == countkt))));

        if (!expr) {
            LOG_MM_EMPLACE1_STATE(ceFile, fuzzer_mode);
        }
        
        assert(expr);
        fuzzBuf.clear();
    }

    ceFile.close();
    return 0;
}
