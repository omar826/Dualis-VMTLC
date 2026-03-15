#include "../../FuzzImpl/AlternatingListImpl.h" // MAPPING: Path changed to FuzzImpl
int main(int argc, char* argv[]) {
    bool fuzzer_mode = getenv("FUZZING") != nullptr;
    if (argc < 2) {
        return 1;
    }
    std::string filePath = argv[1];
    
    std::ofstream ceFile(filePath, std::ios::app);
    if (!ceFile) {
        return 1;
    }

    while (__AFL_LOOP(10000)) {
        std::vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

        if (fuzzLen <= 4) {
            continue;
        }

        AlternatingList al;
        init(al, fuzzBuf, fuzzLen - 2);

        DECLARE_AL_PUSH_STATE_VARS();
        READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, val);
        AL_PUSH_WITH_STATE(al, val);
        
        bool expr = ((val == 1 || val == 2) ? (top1 == val && len1 == len + 1) : (top1 == top && len1 == len));

        if (!expr) {
            if (ceFile.is_open()) {
                LOG_AL_PUSH_STATE(ceFile, fuzzer_mode);
            }
        }
        
        assert(expr);
        fuzzBuf.clear();
    }

    ceFile.close();
    return 0;
}
