#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>
#include <cassert>
#include <unistd.h>
#include <utility>
#include <cstdint>
#include <cassert>

#define MIN 0
#define MAX 10

using namespace std;


#define DECLARE_CAL_INSERT_STATE_VARS()		\
  int ev1, ev2;					\
  int len, maxDiff;				\
  int len1, maxDiff1;

#define CAL_INSERT_WITH_STATE(cal_obj, ev1_param, ev2_param)	\
  do {								\
    len = (cal_obj).len();					\
    maxDiff = (cal_obj).maxDiff();				\
								\
    auto p = std::make_pair(ev1_param, ev2_param);		\
    (cal_obj).insert(p);					\
								\
    len1 = (cal_obj).len();					\
    maxDiff1 = (cal_obj).maxDiff();				\
  } while(0)

#define LOG_CAL_INSERT_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(insert len = " << len		\
			  << ", len1 = " << len1		\
			  << ", ev1 = " << ev1			\
			  << ", ev2 = " << ev2			\
			  << ", maxDiff = " << maxDiff		\
			  << ", maxDiff1 = " << maxDiff1	\
			  << ")\n" << std::endl;		\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define READ_INT8_FROM_FUZZBUF(buffer_ptr, offset, target_var_name)	\
  do {									\
    const uint8_t *valptr_##target_var_name = &(buffer_ptr)[offset];	\
    target_var_name = read_int8(valptr_##target_var_name);		\
  } while(0)

#define READ_UINT8_FROM_FUZZBUF(buffer_ptr, offset, target_var_name)  \
  do {                                                                \
    const uint8_t *valptr_##target_var_name = &(buffer_ptr)[offset];  \
    target_var_name = read_uint8(valptr_##target_var_name);           \
  } while(0)

class Cal {
private:
  vector<pair<int, int>> cal;
  int md;
  bool md_set;

public:
  Cal() : md(0), md_set(false) {}

  Cal(vector<pair<int, int>> elements) : md(0), md_set(false) {
    for (auto e : elements) {
      insert(e);
    }
  }  
  
  void insert(pair<int, int> evp) {
    if(not md_set){
      md = abs(evp.first - evp.second);
      md_set = true;
    }else if(abs(evp.first - evp.second) >= md){
      md = abs(evp.first - evp.second);
    }
    cal.push_back(evp);
  }

  int len() const {
    return cal.size();
  }

  int maxDiff(){
    // Only return md if it has been set, otherwise return 0
    return md_set ? md : 0;
  }
};


constexpr uint8_t CMD_INSERT = 0x01;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0];
  return static_cast<uint32_t>(u);
}

void init(Cal &cal, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 2;
    int v1, v2;

    switch (command) {
    case CMD_INSERT: {
      if ((i+2+1) > initLen) {
	i = initLen;
	break;
      }
      READ_UINT8_FROM_FUZZBUF(buf, i+1, v1);
      READ_UINT8_FROM_FUZZBUF(buf, i+2, v2);
      
      auto p = std::make_pair(v1, v2);
      cal.insert(p);
      
      i += 2;
      break;
    }
    default:
      break;
    }
  }
}
