#include <list>
#include <unordered_map>
#include <utility>
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <unistd.h>
#include <cassert>

#define MIN -129
#define MAX 128

#define DECLARE_LRU_INSERTORASSIGN_STATE_VARS()	\
  int32_t k, v, N;				\
  int len, mru, size, containsmru, kveq;	\
  int len1, mru1, ret1, containsmru1, kveq1;


#define DECLARE_LRU_FIND_STATE_VARS()		\
  int32_t k;					\
  int containsk, kveq;				\
  int ret, mru1;


#define LRU_INSERTORASSIGN_WITH_STATE(lru_obj, key_param, val_param)	\
  do{									\
    k = key_param;							\
    v = val_param;							\
    len = (lru_obj).len();						\
    kveq = (lru_obj).kveq();						\
    mru = (lru_obj).getMru();						\
    size = (lru_obj).getCapacity();					\
    containsmru = (lru_obj).contains(mru);				\
    (lru_obj).insert_or_assign(k, v);					\
    ret1 = 0;								\
    len1 = (lru_obj).len();						\
    kveq1 = (lru_obj).kveq();						\
    mru1 = (lru_obj).getMru();						\
    containsmru1 = (lru_obj).contains(mru1);				\
  }while(0)


#define LRU_FIND_WITH_STATE(lru_obj, key_param)	\
  do{						\
    k = key_param;				\
    containsk = (lru_obj).contains(k);		\
    ret = (lru_obj).find(k);			\
    kveq = (lru_obj).kveq();			\
    mru1 = ret;					\
  }while(0)


#define LOG_LRU_INSERTORASSIGN_STATE(log_file_stream, is_fuzzer_mode)	\
  do {									\
    if (!(log_file_stream)) {						\
      std::cerr << "Error: Unable to open log file." << "\n";		\
      exit(1);								\
    }									\
    if (!(is_fuzzer_mode)) {						\
      if ((log_file_stream).is_open()) {				\
	(log_file_stream)						\
	  << "(insert_or_assign k=" << k				\
	  << ", v=" << v						\
	  << ", len=" << len						\
	  << ", mru=" << mru						\
	  << ", size=" << size						\
	  << ", containsmru=" << containsmru				\
	  << ", len1=" << len1						\
	  << ", mru1=" << mru1						\
	  << ", containsmru1=" << containsmru1				\
	  << ", ret1=" << ret1						\
	  << ")\n";							\
	(log_file_stream).flush();					\
      }									\
    }									\
  } while(0)

#define LOG_LRU_FIND_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream)					\
	  << "(find k=" << k					\
	  << ", containsk=" << containsk			\
	  << ", mru1=" << mru1					\
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


class LRUCache {
private:
  int capacity;
  std::list<std::pair<int, int>> cache_list;
  std::unordered_map<int, std::list<std::pair<int, int>>::iterator> cache_map;

public:
  LRUCache () : capacity(1) {}
  
  LRUCache(int capacity) : capacity(capacity) {
    if (capacity < 1) {
      this->capacity = 1;
    }
  }

  int getCapacity(){
    return capacity;
  }

  int len(){
    return cache_list.size();
  }
  
  void insert_or_assign(int key, int value) {
    auto it = cache_map.find(key);
    if (it != cache_map.end()) {
      it->second->second = value;
      cache_list.splice(cache_list.begin(), cache_list, it->second); // moving the it->value to the beginning of the list in cache_list
      return;
    }
    if (cache_map.size() == capacity) {
      int key_to_evict = cache_list.back().first;
      cache_map.erase(key_to_evict);
      cache_list.pop_back();
    }
    cache_list.push_front({key, value});
    cache_map[key] = cache_list.begin();
  }

  int find(int key) {
    auto it = cache_map.find(key);
    if (it == cache_map.end()) {
      return MAX; // returning sentinel values
    }
    cache_list.splice(cache_list.begin(), cache_list, it->second);
    return it->second->second;
  }

  bool kveq() {
    for (const auto& pair : cache_list) {
      if (pair.first != pair.second) {
	return false;
      }
    }
    return true;
  }

  int contains(int key) {// does not change the order, only get/put
			 // does.
    return cache_map.count(key) > 0 ? 1 : 0;
  }

  int getMru() {
    if (cache_list.empty()) {
      return MAX; // returning sentinel value
    }
    return cache_list.front().second;
  }

  int getLru() {
    if (cache_list.empty()) {
      return MAX; // returning sentinel value
    }
    return cache_list.back().second;
  }
};

// --- Injected Fuzzer Utilities (from AHM example) ---

#include <tuple> // Required for std::tuple

constexpr uint8_t CMD_INSERTORASSIGN = 0x01;
constexpr uint8_t CMD_FIND = 0x02;
constexpr uint8_t CMD_GETMRU = 0x03;

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

void init (LRUCache &lru, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; ++i) {
    uint8_t command = buf[i] % 4; // 0=default, 1=insert, 2=find, 3=getmru
    int k, v;

    switch (command) {
    case CMD_INSERTORASSIGN: {
      if ((i+2+1) > initLen) { // Need 2 param bytes
	i = initLen;
	break;
      }

      READ_INT8_FROM_FUZZBUF(buf, i+1, k);
      READ_INT8_FROM_FUZZBUF(buf, i+2, v);
      lru.insert_or_assign(k, v);
      i += 2;
      break;
    }
    case CMD_FIND: {
      if ((i+1+1) > initLen) { // Need 1 param byte
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, k);
      lru.find(k);
      i += 1;
      break;
    }
    case CMD_GETMRU: {
      lru.getMru();
      break;
    }
    default:
      break;
    }
  }
}
