#include "../../FuzzImpl/AtomicLinkedListImpl.h" // MAPPING: Path changed to FuzzImpl
int main(int argc, char* argv[]) {
    bool fuzzer_mode = getenv("FUZZING") != nullptr;
    if (argc < 2) {
        std::cerr << "Error: Please provide a file path for logging." << "\n";
        return 1;
    }
    std::string filePath = argv[1];
    
    std::ofstream ceFile(filePath, std::ios::app);

    while (__AFL_LOOP(10000)) {
        std::vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

        if (fuzzLen <= 4) {
            continue;
        }

        AtomicLinkedList list;
        init(list, fuzzBuf, fuzzLen-2);

        DECLARE_ALL_POPHEAD_STATE_VARS();
        
        ALL_POPHEAD_WITH_STATE(list);

        bool expr = (len > 0 ? (len1 == len - 1) : (len1 == len));

        if (!expr) {
            if (ceFile.is_open()) {
                LOG_ALL_POPHEAD_STATE(ceFile, fuzzer_mode);
            }
        }
        
        assert(expr);
        fuzzBuf.clear();
    }

    ceFile.close();
    return 0;
}
