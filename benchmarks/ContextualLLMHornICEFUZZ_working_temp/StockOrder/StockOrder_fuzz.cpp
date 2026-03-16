#include "../../FuzzImpl/StockOrderImpl.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint> // For uint8_t
#include <unistd.h>  // For read

int main(int argc, char *argv[]) {
    bool fuzzer_mode = getenv("FUZZING") != nullptr;

    std::string filePath = argv[1];
    std::ofstream ceFile(filePath, std::ios::app);
    if (!ceFile.is_open()) {
        std::cerr << "Error: Unable to open log file." << std::endl;
        return 1;
    }

    // AFL persistent loop
    while (__AFL_LOOP(10000)) {
        std::vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

        if (fuzzLen < 5) {
            continue;
        }

        StockOrder so;

        uint8_t N;
        READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1, N);
        if ( N <= 0){
            continue;
        }
        
        if (static_cast<size_t>((N * 2) + 2) >= static_cast<size_t>(fuzzLen)) {
            continue;
        }

        unsigned int current_offset = 2;
        for (int i = 0; i < N; ++i) {
           
            int8_t stock_raw;
            READ_UINT8_FROM_FUZZBUF(fuzzBuf, current_offset, stock_raw);
            current_offset++; // Advance offset

            int8_t order_raw;
            READ_UINT8_FROM_FUZZBUF(fuzzBuf, current_offset, order_raw);
            current_offset++; // Advance offset

            int stock_val = stock_raw % 128;
            int order_val = order_raw % 128;

            if (stock_val >= 0 && order_val >= 0 && order_val <= stock_val)
            {
                DECLARE_SO_ADDSTOCKORDER_STATE_VARS();
               
                stock = stock_val;
                order = order_val;

                SO_ADDSTOCKORDER_WITH_STATE(so, stock_val, order_val);
                bool expr_addStockOrder = ((len1 == len + 1) && (minDiff1 == ((stock - order) < minDiff ? (stock - order) : minDiff)));
                
                if (!expr_addStockOrder) {
                    LOG_SO_ADDSTOCKORDER_STATE(ceFile, fuzzer_mode);
                }
                assert(expr_addStockOrder);
            }
        }
       
     }

    ceFile.close();
    return 0;
}
