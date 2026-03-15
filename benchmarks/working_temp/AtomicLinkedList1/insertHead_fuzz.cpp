#include "../../FuzzImpl/AtomicLinkedListImpl.h"

int main(int argc, char* argv[]) {
    bool fuzzer_mode = getenv("FUZZING") != nullptr;
    if (argc < 2) {
        std::cerr << "Error: Please provide a file path for logging." << "\n";
        return 1;
    }
    std::string filePath = argv[1];
    std::cout << "Final Path: " << filePath << "\n"; // Logic preserved
    
    std::ofstream ceFile(filePath, std::ios::app);
    if (!ceFile) {
        std::cerr << "Error: Unable to open log file." << "\n";
        return 1;
    }

    while (__AFL_LOOP(10000)) {
        std::vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

        if (fuzzLen <= 4) {
            continue;
        }

        AtomicLinkedList list;
        init(list, fuzzBuf, fuzzLen - 2);

        DECLARE_ALL_INSERTHEAD_STATE_VARS();
        
        READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, k);

        ALL_INSERTHEAD_WITH_STATE(list, k);

        bool expr = len1 == len + 1;

        if (!expr) {
            if (ceFile.is_open()) {
                LOG_ALL_INSERTHEAD_STATE(ceFile, fuzzer_mode);
            }
        }
        
        assert(expr);
        fuzzBuf.clear();
    }

    ceFile.close();
    return 0;
}
