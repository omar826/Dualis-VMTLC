#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>
#include <cstdint>
#include <unistd.h>
#include <cassert>

#define MIN -129
#define MAX 128

#define DECLARE_BWL_PUSH_STATE_VARS()		\
  int color;					\
  int bcount, bcount1;

#define BWL_PUSH_WITH_STATE(bwl_obj, color_param)	\
  do {							\
    color = color_param;				\
    bcount = (bwl_obj).blue_count();			\
    (bwl_obj).push(color_param);			\
    bcount1 = (bwl_obj).blue_count();			\
  } while(0)

#define BWL_PUSH1_WITH_STATE(bwl_obj, color_param)\
  do {								\
    color = color_param;					\
    bcount = (bwl_obj).blue_count();				\
    (bwl_obj).push1(color_param);				\
    bcount1 = (bwl_obj).blue_count();				\
  } while(0)

#define LOG_BWL_PUSH_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(push color =" << color		\
			  << ", bcount =" << bcount		\
			  << ", bcount1 =" << bcount1		\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_BWL_PUSH1_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(push1 color =" << color		\
			  << ", bcount =" << bcount		\
			  << ", bcount1 =" << bcount1		\
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


class BWList {
private:
  std::vector<short> bwl;

public:
  BWList() = default; // Added default constructor

  BWList(std::vector<short> elements) {
    for (auto e : elements) {
      push(e);
    }
  }
   
  // 0 - blue, 1 - white
  void push(int key) {
    bwl.push_back(key);
  }


  void push1(int key) {
    bwl.push_back(key);
  }

  int blue_present(){
    auto it = std::find(bwl.begin(), bwl.end(), 0);
    return (it != bwl.end()) ? 1 : 0; // Return 1 if found, 0 if not
  }

  int blue_count(){
    return std::count(bwl.begin(), bwl.end(), 0);
  }

  int top() const{
    if (bwl.empty()) {
      return MAX; // Use your sentinel value for the empty case
    }
    return bwl.front(); // .front() is more idiomatic than .at(0)
  }
  
  int len() const{
    return bwl.size();
  }
};

constexpr uint8_t CMD_PUSH = 0x01;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0];
  return static_cast<uint32_t>(u);
}

#define READ_UINT8_FROM_FUZZBUF(buffer_ptr, offset, target_var_name)     \
  do {                                                                   \
    const uint8_t *valptr_##target_var_name = &(buffer_ptr)[offset];     \
    target_var_name = read_uint8(valptr_##target_var_name);              \
  } while(0)

void init (BWList &bw, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; ++i) {
    uint8_t command = buf[i] % 2;

    switch (command) {
    case CMD_PUSH: {
      if ((i+1+1) > initLen) {
	i = initLen;
	break;
      }
      int v;
      READ_INT8_FROM_FUZZBUF(buf, i+1, v);
      bw.push(v);
      i += 1;
      break;
    }
    default:
      break;
    }
  }
}
