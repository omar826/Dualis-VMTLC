#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>
#include <cassert>
#include <cstdint>
#include <unistd.h>

#define MIN -129
#define MAX 128

#define DECLARE_PQ_INSERT_STATE_VARS()		\
  int nexttime;					\
  int len, min_ttw;				\
  int len1, min_ttw1;

#define DECLARE_PQ_CHOOSENEXT_STATE_VARS()	\
  int len, min_ttw;				\
  int len1, min_ttw1;

#define PQ_INSERT_WITH_STATE(pq_obj, nexttime_param)	\
  do {							\
    nexttime = nexttime_param;				\
    len = (pq_obj).len();				\
    min_ttw = (pq_obj).minttw();			\
							\
    (pq_obj).insert(nexttime);				\
							\
    len1 = (pq_obj).len();				\
    min_ttw1 = (pq_obj).minttw();			\
  } while(0)

#define PQ_CHOOSENEXT_WITH_STATE(pq_obj)		\
  do {							\
    len = (pq_obj).len();				\
    min_ttw = (pq_obj).minttw();			\
							\
    (pq_obj).choosenext();				\
							\
    len1 = (pq_obj).len();				\
    min_ttw1 = (pq_obj).minttw();			\
  } while(0)

#define LOG_PQ_INSERT_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(insert nexttime = " << nexttime	\
			  << ", len = " << len			\
			  << ", len1 = " << len1		\
			  << ", min_ttw = " << min_ttw		\
			  << ", min_ttw1 = " << min_ttw1	\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_PQ_CHOOSENEXT_STATE(log_file_stream, is_fuzzer_mode) \
  do {								 \
    if (!(log_file_stream)) {					 \
      std::cerr << "Error: Unable to open log file." << "\n";	 \
      exit(1);							 \
    }								 \
    if (!(is_fuzzer_mode)) {					 \
      if ((log_file_stream).is_open()) {			 \
	(log_file_stream) << "(choosenext len = " << len		 \
			  << ", len1 = " << len1		 \
			  << ", min_ttw = " << min_ttw		 \
			  << ", min_ttw1 = " << min_ttw1	 \
			  << ")\n";				 \
	(log_file_stream).flush();				 \
      }								 \
    }								 \
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

class ProcessQueue {
private:
  std::vector<int> Q;  // Vector to hold the queue elements

public:
  ProcessQueue() = default; // Added default constructor

  ProcessQueue(std::vector<int> elements) {
    for (auto e : elements) {
      insert(e);
    }
  }

  void insert(int nexttime) {
    Q.push_back(nexttime); 	
  }

  int len()  {
    return Q.size();
  }

  int minttw()  {
    if (Q.empty()) {
      return MAX;
    }
    return *(std::min_element(Q.begin(), Q.end()));
  }

  void choosenext() {
    for (auto it = Q.begin(); it != Q.end();) {
      if (*it == 1) {
	it = Q.erase(it);
      } else {
	(*it)--;
	++it;
      }
    }
  }

  bool isEmpty() { return Q.size() == 0; }
};


constexpr uint8_t CMD_INSERT = 0x01;
constexpr uint8_t CMD_CHOOSENEXT = 0x02;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0]; // Correct
  return static_cast<uint32_t>(u);
}

void init(ProcessQueue &pq, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 3;
    int v;

    switch (command) {
    case CMD_INSERT: {
      if ((i+1+1) > initLen) { // Need 1 byte for parameter
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, v);
      
      pq.insert(v);
      i += 1;
      break;
    }

    case CMD_CHOOSENEXT: {
      pq.choosenext();
      break;
    }

    default:
      break;
    }
  }
}
