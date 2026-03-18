#include "../../FuzzImpl/SkipListImpl.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <unistd.h>

int main(int argc, char *argv[]) {
    bool fuzzer_mode = getenv("FUZZING") != nullptr;
    
    std::string filePath = argv[1];
    std::ofstream ceFile(filePath, std::ios::app);
    if (!ceFile.is_open()) {
        std::cerr << "Error: Unable to open log file." << std::endl;
        return 1;
    }

    while (__AFL_LOOP(10000)) {
        std::vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

        if (fuzzLen < 3) {
            continue;
        }

        SkipList sl;

        int8_t N;
        READ_UINT8_FROM_FUZZBUF(fuzzBuf, 1, N);
        if(N <= 0){
            continue;
        }

        if (static_cast<size_t>(2 + N) > static_cast<size_t>(fuzzLen)) {
            continue;
        }

        unsigned int current_offset = 2;
        for (int i = 0; i < N; ++i) {
            DECLARE_SL_INSERT_STATE_VARS();
            
            READ_INT8_FROM_FUZZBUF(fuzzBuf, current_offset, v);
            current_offset++;
            
            SL_INSERT_WITH_STATE(sl, v);

            bool expr_insert = (false); 

            if (!expr_insert) {
                LOG_SL_INSERT_STATE(ceFile, fuzzer_mode);
            }
            assert(expr_insert);
        }

        DECLARE_SL_LOWERBOUND_STATE_VARS();
        
        k = sl.max();
        SL_LOWERBOUND_WITH_STATE(sl, k); 

        bool expr_lower_bound = (false);

        if (!expr_lower_bound) {
            LOG_SL_LOWERBOUND_STATE(ceFile, fuzzer_mode);
        }
        assert(expr_lower_bound);
    }
    ceFile.close();
    return 0;
}
