#include "../../FuzzImpl/StockOrderImpl.h" // MAPPING: Path changed to FuzzImpl

int main(int argc, char* argv[])
{
    bool fuzzer_mode = getenv("FUZZING") != nullptr;
    if (argc < 2) { // Check for log file path
        cerr << "Error: Please provide a file path for logging." << endl;
        return 1;
    }
    string filePath = argv[1];
    cout << "Final Path: " << filePath << endl;

    ofstream ceFile(filePath, ios::app);
    if (!ceFile) {
        cerr << "Error: Unable to open log file." << endl;
        return 1;
    }

    while (__AFL_LOOP(10000)) {
        vector<uint8_t> fuzzBuf(4096);
        ssize_t fuzzLen = read(0, fuzzBuf.data(), fuzzBuf.size());

        if (fuzzLen <= 6) {
            continue;
        }

        StockOrder obj;
        init(obj, fuzzBuf, fuzzLen - 2);

        DECLARE_SO_ADDSTOCKORDER_STATE_VARS();
        READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 2, stock);
        READ_UINT8_FROM_FUZZBUF(fuzzBuf, fuzzLen - 1 , order);
        SO_ADDSTOCKORDER_WITH_STATE(obj, stock, order);

        bool expr = ((minDiff == stock + 1) && (minDiff1 == (len - len1 < order ? len - len1 : order)));
        
        if(!expr){
            if(ceFile.is_open()){
                LOG_SO_ADDSTOCKORDER_STATE(ceFile, fuzzer_mode);
            }
        }
        
        assert(expr);
        fuzzBuf.clear();
    }

    ceFile.close(); // Correct place to close the file
    return 0;
}
