#include "../../FuzzImpl/TokenBucketImpl.h" // MAPPING: Path changed to FuzzImpl

int main(int argc, char* argv[]) {
    bool fuzzer_mode = getenv("FUZZING") != nullptr;
    if (argc < 2) {
        std::cerr << "Error: Please provide a file path for logging." << std::endl;
        return 1;
    }
    std::string filePath = argv[1];
    std::cout << "Final Path: " << filePath << std::endl; // Logic preserved
    
    std::ofstream ceFile(filePath, std::ios::app);
    if (!ceFile) {
        std::cerr << "Error: Unable to open log file." << std::endl;
        return 1;
    }

    while (__AFL_LOOP(10000)) {
        std::vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());
        if (fuzzLen < 6) {
            continue; 
        }

        TokenBucket bucket;
        init(bucket, fuzzBuf, fuzzLen);

        DECLARE_TB_CONSUME_STATE_VARS();

        READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, b_size);

        TB_GENERATETOKENS_WITH_STATE(bucket, b_size);
        
        bool expr = avai_tokens == b_size;

        if (!expr) {
            LOG_TB_GENERATETOKENS_STATE(ceFile, fuzzer_mode);
        }
        
        assert(expr);
        fuzzBuf.clear();
    }

    ceFile.close();
    return 0;
}
