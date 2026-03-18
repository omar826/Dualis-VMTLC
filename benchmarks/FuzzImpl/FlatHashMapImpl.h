#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <unordered_map>
#include <climits> 
#include <cstring> 
#include <cassert> 
#include <algorithm>
#include <unistd.h>

#define MIN -129
#define MAX 128

#define DECLARE_FHM_INSERT_STATE_VARS()		\
  int32_t k, v;					\
  int len, containsk;				\
  int len1, containsk1;


#define DECLARE_FHM_REMOVEALL_STATE_VARS()	\
  int len, remove_count;			\
  int len1, remove_count1;


#define DECLARE_FHM_REMOVENONE_STATE_VARS()	\
  int len, remove_count;			\
  int len1, remove_count1;


#define DECLARE_FHM_ERASE_STATE_VARS()		\
  int k, flag;					\
  int len;					\
  int len1, ret1;


#define FHM_INSERT_WITH_STATE(fhm_obj, key_param, val_param)	\
  do{								\
    k = key_param;						\
    v = val_param;						\
    len = (fhm_obj).len();					\
    containsk = (fhm_obj).contains(k);				\
    (fhm_obj).insert(k, v);					\
    len1 = (fhm_obj).len();					\
    containsk1 = (fhm_obj).contains(k);				\
  }while(0)


#define FHM_REMOVEALL_WITH_STATE(fhm_obj)	\
  do{						\
    len = (fhm_obj).len();			\
    remove_count = 0;				\
    remove_count1 = (fhm_obj).len();		\
    (fhm_obj).remove_all();			\
    len1 = (fhm_obj).len();			\
  }while(0)


#define FHM_REMOVENONE_WITH_STATE(fhm_obj)	\
  do{						\
    len = (fhm_obj).len();			\
    remove_count = 0;				\
    len1 = (fhm_obj).len();			\
    remove_count1 = 0;				\
  }while(0)


#define FHM_ERASE_WITH_STATE(fhm_obj, key_param, flag_param)	\
  do{								\
    k = key_param;						\
    flag = flag_param;						\
    len = (fhm_obj).len();					\
    ret1 = (fhm_obj).erase(k, flag);				\
    len1 = (fhm_obj).len();					\
  }while(0)


#define LOG_FHM_INSERT_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream)  << "(insert k=" << k			\
			   << ", v=" << v			\
			   << ", len=" << len			\
			   << ", containsk=" << containsk	\
			   << ", len1=" << len1			\
			   << ", containsk1=" << containsk1	\
			   << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_FHM_REMOVEALL_STATE(log_file_stream, is_fuzzer_mode)	\
  do {									\
    if (!(log_file_stream)) {						\
      std::cerr << "Error: Unable to open log file." << "\n";		\
      exit(1);								\
    }									\
    if (!(is_fuzzer_mode)) {						\
      if ((log_file_stream).is_open()) {				\
	(log_file_stream)						\
	  << "(remove_all len=" << len					\
	  << ", remove_count=" << remove_count				\
	  << ", len1=" << len1						\
	  << ", remove_count1=" << remove_count1			\
	  << ")\n";							\
	(log_file_stream).flush();					\
      }									\
    }									\
  } while(0)


#define LOG_FHM_REMOVENONE_STATE(log_file_stream, is_fuzzer_mode)	\
  do {									\
    if (!(log_file_stream)) {						\
      std::cerr << "Error: Unable to open log file." << "\n";		\
      exit(1);								\
    }									\
    if (!(is_fuzzer_mode)) {						\
      if ((log_file_stream).is_open()) {				\
	(log_file_stream)						\
	  << "(remove_none len=" << len					\
	  << ", remove_count=" << remove_count				\
	  << ", len1=" << len1						\
	  << ", remove_count1=" << remove_count1			\
	  << ")\n";							\
	(log_file_stream).flush();					\
      }									\
    }									\
  } while(0)


#define LOG_FHM_ERASE_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream)					\
	  << "(erase k=" << k					\
	  << ", len=" << len					\
	  << ", flag=" << flag					\
	  << ", len1=" << len1					\
	  << ", ret1=" << ret1					\
	  << ")\n";						\
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


// flathashmap has the same interface as that unordered_map but is a
// more performant hybrid version.
class FlatHashMap{
private:
  std::unordered_map<int, int> fhm;

public:
  void insert(int key, int value){
    fhm.emplace(key, value);
  }

  int erase(int key) {
    size_t elements_erased = fhm.erase(key);

    if (elements_erased > 0) {
      return key;
    } else {
      return MIN;
    }
  }

  int erase(int key, int flag) {
    if (flag == 1) {
      if (fhm.erase(key) > 0) {
	return key;
      }
    }
    return MIN;
  }

  int contains(int k){
    return fhm.contains(k);
  }

  void remove_all(){
    fhm.clear();
  }

  int remove_none(){
    return 0;
  }

  int len(){
    return fhm.size();
  }

  int minKey(){
    if(fhm.empty()){
      return MIN;
    }
    auto min_key = std::min_element(fhm.begin(), fhm.end(), [](const auto &a, const auto &b){ // first , second
      return a.first < b.first; // assume first is smallest, and if
      // second (new element) is smaller
      // than smallest (first) then update
    });
    return min_key->first;
  }

  int maxKey(){
    if(fhm.empty()){
      return MAX;
    }
    auto max_key = std::max_element(fhm.begin(), fhm.end(), [](const auto &a, const auto &b){// first, second
      return a.first < b.first; // assume first is largest, and if
      // second (new element) is larger than
      // largest (first) then update
    });
    return max_key->first;    
  }
};

constexpr uint8_t CMD_INSERT = 0x01;
constexpr uint8_t CMD_ERASE = 0x02;
constexpr uint8_t CMD_REMOVEALL = 0x03;
constexpr uint8_t CMD_REMOVENONE = 0x04;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0];
  return static_cast<uint32_t>(u);
}

void init (FlatHashMap &fhm, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen;i++) {
    uint8_t command = buf[i] % 5;
    int32_t k, v, flag;

    switch (command) {
    case CMD_INSERT: {
      if ((i+2+1) > initLen) {
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, k);
      READ_INT8_FROM_FUZZBUF(buf, i+2, v);
      fhm.insert(k, v);
      i +=2;
      break;
    }
    case CMD_ERASE: {
      if ((i+2+1) > initLen) {
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+2, flag);
      READ_INT8_FROM_FUZZBUF(buf, i+1, k);
      flag = flag % 2;

      fhm.erase(k, flag);
      i +=2;
      break;
    }
    case CMD_REMOVEALL: {
      fhm.remove_all();
      break;
    }
    case CMD_REMOVENONE: {
      fhm.remove_none();
      break;
    }
    default:
      break;
    }
  }
}
