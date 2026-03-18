#include <iostream>
#include <fstream>
#include <vector>
#include <climits>
#include <filesystem>
#include <algorithm>
#include <cstdint>
#include <unistd.h>
#include <string>
#include <cassert>

#define MIN -129
#define MAX 128

using namespace std;

// --- Generated Macros from Harnesses ---

#define DECLARE_MAXL_APPEND_STATE_VARS()	\
  int v;					\
  int lmax;					\
  int lmax1;

#define MAXL_APPEND_WITH_STATE(maxl_obj, val_param)	\
  do {							\
    lmax = (maxl_obj).maxElem();			\
    (maxl_obj).append(val_param);			\
    lmax1 = (maxl_obj).maxElem();			\
  } while(0)

#define LOG_MAXL_APPEND_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(append v = " << v		\
			  << ", lmax = " << lmax		\
			  << ", lmax1 = " << lmax1		\
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


// --- Transformed Class Definition ---

class Max {
private:
  vector<int> ml;  // Vector to hold the queue elements

public:
  Max() = default; // Added default constructor

  Max(vector<int> elements) {
    for (auto e : elements) {
      append(e);
    }
  }

  void append(int e) {
    ml.push_back(e);  
  }

  int len()  {
    return ml.size();
  }


  int maxElem()  {
    if (ml.empty()) {
      return MIN;
    }
    auto result = *max_element(ml.cbegin(), ml.cend());
    return result;
  }

};

// --- Injected Fuzzer Utilities (Standardized) ---

constexpr uint8_t CMD_APPEND = 0x01;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0];
  return static_cast<uint32_t>(u);
}

#define READ_UINT8_FROM_FUZZBUF(buffer_ptr, offset, target_var_name)    \
  do {									\
    const uint8_t *valptr_##target_var_name = &(buffer_ptr)[offset];	\
    target_var_name = read_uint8(valptr_##target_var_name);		\
  } while(0)

void init(Max &maxl, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 2; // 0=default, 1=append
    int v; // value for insertion

    switch (command) {
    case CMD_APPEND: {
      if ((i+1+1) > initLen) { // Need 1 byte for parameter
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, v);
      maxl.append(v);
      i += 1; // Consumed 1 param byte
      break;
    }
    
    default:
      break;
    }
  }
}
