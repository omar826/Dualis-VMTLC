#include <iostream>
#include <fstream>
#include <vector>
#include <climits>
#include <filesystem>
#include <algorithm>
#include <cassert>
#include <unistd.h>
#include <cstdint>
#include <string>

#define MIN -129
#define MAX 128

using namespace std;

#define DECLARE_MIN_APPEND_STATE_VARS()		\
  short v;					\
  int lmin;					\
  int lmin1;

#define MIN_APPEND_WITH_STATE(min_obj, v_param)		\
  do {							\
    lmin = (min_obj).minElem();				\
    (min_obj).append(v_param);				\
    lmin1 = (min_obj).minElem();			\
  } while(0)

#define LOG_MIN_APPEND_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(append v = " << v			\
			  << ", lmin = " << lmin		\
			  << ", lmin1 = " << lmin1		\
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



class Min {
private:
  vector<short> ml; 

public:
  Min() = default;

  Min(vector<short> elements) {
    for (auto e : elements) {
      append(e);
    }
  }

  void append(short e) {
    ml.push_back(e);  
  }

  int len()  {
    return ml.size();
  }

  int minElem()  {
    if (ml.empty()) {
      return MAX;
    }
    auto result = *min_element(ml.cbegin(), ml.cend());
    return result;
  }
};

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


void init(Min &minl, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 2; // 0=default, 1=append
    short v; // value for append

    switch (command) {
    case CMD_APPEND: {
      if ((i+1+1) > initLen) { // Need 1 byte for parameter
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, v);
      minl.append(v);
      i += 1; // Consumed 1 param byte
      break;
    }
    default:
      break;
    }
  }
}
