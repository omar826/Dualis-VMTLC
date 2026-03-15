#include "../../FuzzImpl/BlueWhiteImpl.h"

int main(int argc, char* argv[])
{
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

        BWList bwl;
        init(bwl, fuzzBuf, fuzzLen - 2);

        DECLARE_BWL_PUSH_STATE_VARS();
        READ_INT8_FROM_FUZZBUF(fuzzBuf, fuzzLen -2, color);
        BWL_PUSH_WITH_STATE(bwl, color);
        
        bool expr = ((color == 0) ? (bcount1 == bcount + 1) : (bcount1 == bcount));

        if(!expr){
            if (ceFile.is_open()){
                LOG_BWL_PUSH_STATE(ceFile, fuzzer_mode);
            }
        }
        
        assert(expr);
        fuzzBuf.clear();
    }
    ceFile.close();
    return 0;
}
