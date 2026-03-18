#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <utility>
#include <cstdint>
#include <unistd.h>
#include <string>
#include <algorithm>
#include <climits>
#include <cassert>

#define MIN -129
#define MAX 128

#define DECLARE_MM_EMPLACE_STATE_VARS()		\
  int k, v, k_one = 1;				\
  int len, countko;				\
  int len1, countko1;

#define DECLARE_MM_EMPLACE1_STATE_VARS()	\
  int k, v, k_one = 1, k_two = 2;		\
  int countko, countkt, len;			\
  int countko1, countkt1, len1;

#define MM_EMPLACE_WITH_STATE(mm_obj, key_param, val_param)	\
  do {								\
    len = (mm_obj).size();					\
    countko = (mm_obj).count(k_one);				\
    k = key_param;						\
    v = val_param;						\
    (mm_obj).emplace(k, v);					\
								\
    countko1 = (mm_obj).count(k_one);				\
    len1 = (mm_obj).size();					\
  } while(0)

#define MM_EMPLACE1_WITH_STATE(ms_obj, key_param, val_param)	\
  do {								\
    countko = (ms_obj).count(k_one);				\
    countkt = (ms_obj).count(k_two);				\
    len = (ms_obj).size();					\
    k = key_param;						\
    v = val_param;						\
								\
    (ms_obj).emplace(k, v);					\
    								\
    countko1 = (ms_obj).count(k_one);				\
    countkt1 = (ms_obj).count(k_two);				\
    len1 = (ms_obj).size();					\
  } while(0)

#define LOG_MM_EMPLACE_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(emplace k=" << k			\
			  << ", v=" << v			\
			  << ", countko=" << countko		\
			  << ", len=" << len			\
			  << ", countko1=" << countko1		\
			  << ", len1=" << len1			\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_MM_EMPLACE1_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(emplace k=" << k			\
			  << ", v=" << v			\
			  << ", countko=" << countko		\
			  << ", countkt=" << countkt		\
			  << ", len=" << len			\
			  << ", countko1=" << countko1		\
			  << ", countkt1=" << countkt1		\
			  << ", len1=" << len1			\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_MM_EMPLACE2_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(emplace1 k=" << k		\
			  << ", v=" << v			\
			  << ", countko=" << countko		\
			  << ", countkt=" << countkt		\
			  << ", len=" << len			\
			  << ", countko1=" << countko1		\
			  << ", countkt1=" << countkt1		\
			  << ", len1=" << len1			\
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


constexpr uint8_t CMD_EMPLACE = 0x01;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

void init(std::multimap<int, int> &map, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 2;
    int k, v; 

    switch (command) {
    case CMD_EMPLACE: {
      if ((i+2+1) > initLen) { 
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, k);
      READ_INT8_FROM_FUZZBUF(buf, i+2, v);
      map.emplace(k, v);
      i += 2;
      break;
    }

    default:
      break;
    }
  }
}
