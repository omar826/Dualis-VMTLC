#include "../../FuzzImpl/MultiSetImpl.h"

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

        if (fuzzLen < 4) {
            continue; 
        }

        std::multiset<int> set;
        init(set, fuzzBuf, fuzzLen - 2);


        DECLARE_MS_EMPLACE_STATE_VARS();
        READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -1, v);

        MS_EMPLACE_WITH_STATE(set, v);
        
        bool expr = (len1 == len + 1 && countv1 == countv + 1);

        if (!expr) {
            LOG_MS_EMPLACE_STATE(ceFile, fuzzer_mode);
        }
        
        assert(expr);
        
        fuzzBuf.clear();
    }

    ceFile.close();
    return 0;
}
