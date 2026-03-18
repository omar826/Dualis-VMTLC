#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <utility>
#include <cstdint>
#include <unistd.h>
#include <string>
#include <algorithm>
#include <climits>
#include <cassert>

#define MIN -129
#define MAX 128

#define DECLARE_MS_EMPLACE_STATE_VARS()		\
  int v;					\
  int countv, len;				\
  int countv1, len1;

#define DECLARE_MS_EMPLACE1_STATE_VARS()	\
  int v, vo = 1, vt = 2;			\
  int countvo, countvt, len;			\
  int countvo1, countvt1, len1;

#define MS_EMPLACE_WITH_STATE(ms_obj, val_param)	\
  do {							\
    v = val_param;					\
    countv = (ms_obj).count(val_param);			\
    len = (ms_obj).size();				\
							\
    (ms_obj).emplace(v);				\
							\
    countv1 = (ms_obj).count(val_param);		\
    len1 = (ms_obj).size();				\
  } while(0)

#define MS_EMPLACE1_WITH_STATE(ms_obj, val_param)	\
  do {							\
    v = val_param;					\
    countvo = (ms_obj).count(vo);			\
    countvt = (ms_obj).count(vt);			\
    len = (ms_obj).size();				\
							\
    (ms_obj).emplace(v);				\
							\
    countvo1 = (ms_obj).count(vo);			\
    countvt1 = (ms_obj).count(vt);			\
    len1 = (ms_obj).size();				\
  } while(0)


#define LOG_MS_EMPLACE_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(emplace v=" << v			\
			  << ", countv=" << countv		\
			  << ", len=" << len			\
			  << ", countv1=" << countv1		\
			  << ", len1=" << len1			\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_MS_EMPLACE1_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(emplace v=" << v			\
			  << ", countvo=" << countvo		\
			  << ", countvt=" << countvt		\
			  << ", len=" << len			\
			  << ", countvo1=" << countvo1		\
			  << ", countvt1=" << countvt1		\
			  << ", len1=" << len1			\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_MS_EMPLACE2_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(emplace1 v=" << v		\
			  << ", countvo=" << countvo		\
			  << ", countvt=" << countvt		\
			  << ", len=" << len			\
			  << ", countvo1=" << countvo1		\
			  << ", countvt1=" << countvt1		\
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

#define READ_UINT8_FROM_FUZZBUF(buffer_ptr, offset, target_var_name)	\
  do {									\
    const uint8_t *valptr_##target_var_name = &(buffer_ptr)[offset];	\
    target_var_name = read_uint8(valptr_##target_var_name);		\
  } while(0)


constexpr uint8_t CMD_EMPLACE = 0x01;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0];
  return static_cast<uint32_t>(u);
}

void init(std::multiset<int> &set, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 2; // 0=default, 1=emplace
    int v; 

    switch (command) {
    case CMD_EMPLACE: {
      if ((i+1+1) > initLen) { // Need 1 byte for param (v)
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, v);
      set.emplace(v);
      i += 1; // Consumed 1 param byte
      break;
    }

    default:
      break;
    }
  }
}
