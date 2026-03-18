#include <iostream>
#include <cassert>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <unistd.h>
#include <cstdint>
#include <climits>

#define MIN -129
#define MAX 128

#define DECLARE_STACK_PUSH_STATE_VARS()		\
  short N;					\
  int sl;					\
  int sl1;

#define DECLARE_STACK_POP_STATE_VARS()		\
  int sl;					\
  int sl1;

#define STACK_PUSH_WITH_STATE(st_obj, key_param)	\
  do {							\
    sl = (st_obj).len();				\
    (st_obj).push(key_param);				\
    sl1 = (st_obj).len();				\
  } while(0)

#define STACK_POP_WITH_STATE(st_obj)			\
  do {							\
    sl = (st_obj).len();				\
    if (sl > 0) { /* Added safety check */		\
        (st_obj).pop();				\
    }							\
    sl1 = (st_obj).len();				\
  } while(0)

#define LOG_STACK_PUSH_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(pu N = " << N			\
			  << ", sl = " << sl			\
			  << ", sl1 = " << sl1			\
			  << ")\n";				\
	(log_file_stream).flush();				\
      }								\
    }								\
  } while(0)

#define LOG_STACK_POP_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(po sl = " << sl			\
			  << ", sl1 = " << sl1			\
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

class Stack {
private:
  std::vector<int> stack;

public:
  Stack() = default;

  Stack(const std::vector<int> elements) : stack(elements) {}

  void push(int key) {
    stack.push_back(key);
  }

  void pop() {
    if (!stack.empty()) {
        stack.pop_back();
    }
  }

  int len() const {
    return stack.size();
  }
};

constexpr uint8_t CMD_PUSH = 0x01;
constexpr uint8_t CMD_POP = 0x02;

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

void init(Stack &st, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 3; // 0=default, 1=push, 2=pop
    short v;

    switch (command) {
    case CMD_PUSH: {
      if ((i+1+1) > initLen) {
	i = initLen;
	break;
      }
      READ_INT8_FROM_FUZZBUF(buf, i+1, v);
      st.push(v);
      i += 1;
      break;
    }
    case CMD_POP: {
      if (st.len() > 0) {
	st.pop();
      }
      break;
    }

    default:
      break;
    }
  }
}
