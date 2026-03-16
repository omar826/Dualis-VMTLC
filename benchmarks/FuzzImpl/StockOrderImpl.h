#include <iostream>
#include <fstream>
#include <vector>
#include <limits.h> // for INT_MAX
#include <filesystem>
#include <utility>   // Added for std::pair
#include <cmath>     // Added for std::abs
#include <cstdint>   // Added for fuzzer types
#include <unistd.h>    // Added for ssize_t
#include <string>    // Added for std::string
#include <cassert>

using namespace std;

#define MIN -129
#define MAX 128

// --- Generated Macros from Harnesses ---

#define DECLARE_SO_ADDSTOCKORDER_STATE_VARS()	\
  int stock, order;				\
  int len, minDiff;				\
  int len1, minDiff1;

#define SO_ADDSTOCKORDER_WITH_STATE(so_obj, stock_param, order_param) \
  do {								\
    len = (so_obj).len();					\
    minDiff = (so_obj).getMinDiff();				\
    auto p = std::make_pair(stock_param, order_param);		\
    (so_obj).addStockOrder(p);					\
    len1 = (so_obj).len();					\
    minDiff1 = (so_obj).getMinDiff();				\
  } while(0)

#define LOG_SO_ADDSTOCKORDER_STATE(log_file_stream, is_fuzzer_mode) \
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(addStockOrder stock = " << stock	\
			  << ", order = " << order		\
			  << ", len = " << len			\
			  << ", len1 = " << len1		\
			  << ", minDiff = " << minDiff		\
			  << ", minDiff1 = " << minDiff1	\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define READ_INT8_FROM_FUZZBUF(buffer_ptr, offset, target_var_name)	\
  do {									\
    const uint8_t *valptr_##target_var_name = &(buffer_ptr)[offset];	\
    target_var_name = read_int8(valptr_##target_var_name);		\
  } while(0)

#define READ_UINT8_FROM_FUZZBUF(buffer_ptr, offset, target_var_name)	\
  do {									\
    const uint8_t *valptr_##target_var_name = &(buffer_ptr)[offset];	\
    target_var_name = read_uint8(valptr_##target_var_name);		\
  } while(0)

class StockOrder {
 private:
  vector<pair<int, int>> cal;
  int md;

 public:
  StockOrder() : md(MAX) {}

  StockOrder(vector<pair<int, int>> elements) {
    md = MAX;
    for (auto e : elements) {
      addStockOrder(e);
    }
  }
  
  void addStockOrder(pair<int, int> evp) {
    if((abs(evp.second - evp.first)) <= md || cal.empty()){ // Modified to set initial md
      md = abs(evp.second - evp.first);
    }
    cal.push_back(evp);
  }

  int len() const {
    return cal.size();
  }

  int getMinDiff(){
    return md;
  }
};

constexpr uint8_t CMD_ADDSTOCKORDER = 0x01;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0];
  return static_cast<uint32_t>(u);
}

void init(StockOrder &so, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 2;
    int v1, v2;

    switch (command) {
    case CMD_ADDSTOCKORDER: {
      if ((i+2+1) > initLen) {
	i = initLen;
	break;
      }
      READ_UINT8_FROM_FUZZBUF(buf, i+1, v1);
      READ_UINT8_FROM_FUZZBUF(buf, i+2, v2);
      so.addStockOrder(std::make_pair(v1, v2));
      i += 2;
      break;
    }
    default:
      break;
    }
  }
}
