#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <filesystem>
#include <cstdint>
#include <unistd.h>
#include <string>
#include <cassert>

using namespace std;

#define MIN 0
#define MAX 128

#define DECLARE_TB_GENERATETOKENS_STATE_VARS()	\
  int b_size;					\
  int avai_tokens;				\
  int avai_tokens1;

#define DECLARE_TB_CONSUME_STATE_VARS()		\
  int b_size;					\
  int c_rate;					\
  bool success;					\
  int avai_tokens1;				\
  int avai_tokens;

#define TB_GENERATETOKENS_WITH_STATE(tb_obj, b_size_param)	\
  do {								\
    b_size = b_size_param;					\
    avai_tokens = (tb_obj).getAvailableTokens();		\
    (tb_obj).generateTokens(b_size);				\
    avai_tokens1 = (tb_obj).getAvailableTokens();		\
  } while(0)
    
#define TB_CONSUME_WITH_STATE(tb_obj, c_rate_param, b_size_param)	\
  do {									\
    c_rate = c_rate_param;						\
    b_size = b_size_param;						\
    (tb_obj).generateTokens(b_size);					\
    avai_tokens = (tb_obj).getAvailableTokens();			\
    success = (tb_obj).consume(c_rate);					\
    avai_tokens1 = (tb_obj).getAvailableTokens();			\
  } while(0)

#define TB_CONSUME1_WITH_STATE(tb_obj, c_rate_param)			\
  do {									\
    c_rate = c_rate_param;						\
    avai_tokens = (tb_obj).getAvailableTokens();			\
    success = (tb_obj).consume(c_rate);					\
    avai_tokens1 = (tb_obj).getAvailableTokens();			\
  } while(0)

#define LOG_TB_GENERATETOKENS_STATE(log_file_stream, is_fuzzer_mode)	\
  do {									\
    if (!(log_file_stream)) {						\
      std::cerr << "Error: Unable to open log file." << "\n";		\
      exit(1);								\
    }									\
    if (!(is_fuzzer_mode)) {						\
      if ((log_file_stream).is_open()) {				\
	(log_file_stream) << "(generateTokens b_size=" << b_size	\
			  << ", avai_tokens1=" << avai_tokens1		\
			  << ")\n";					\
	(log_file_stream).flush();					\
      }									\
    }									\
  } while(0)

#define LOG_TB_CONSUME_STATE(log_file_stream, is_fuzzer_mode)	\
  do {								\
    if (!(log_file_stream)) {					\
      std::cerr << "Error: Unable to open log file." << "\n";	\
      exit(1);							\
    }								\
    if (!(is_fuzzer_mode)) {					\
      if ((log_file_stream).is_open()) {			\
	(log_file_stream) << "(consume c_rate=" << c_rate	\
			  << ", avai_tokens=" << avai_tokens	\
			  << ", avai_tokens1=" << avai_tokens1	\
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


class TokenBucket {
private:
  int current_tokens_;

public:
  TokenBucket() : current_tokens_(0) {} // Added default constructor
  
  TokenBucket(int initial_tokens) : current_tokens_(initial_tokens) {}

  void generateTokens( int burst_size) {
    int new_tokens = burst_size;
    int current_tokens = current_tokens_;
    int total_tokens = current_tokens + new_tokens;
        
    current_tokens_ = std::min(burst_size, total_tokens);
  }

  bool consume(int consume_rate) {
    if (current_tokens_ >= consume_rate) {
      current_tokens_ -= consume_rate;
      return true;
    }
    return false;
  }

  int getAvailableTokens() const {
    return current_tokens_;
  }
};

constexpr uint8_t CMD_GENERATE = 0x01;
constexpr uint8_t CMD_CONSUME = 0x02;

static int32_t read_int8(const uint8_t *b) {
  int8_t u = (int8_t)b[0];
  return static_cast<int32_t>(u);
}

static uint32_t read_uint8(const uint8_t *b) {
  uint8_t u = (uint8_t)b[0];
  return static_cast<uint32_t>(u);
}

void init(TokenBucket &tb, std::vector<uint8_t>& buf, ssize_t initLen){
  for (ssize_t i = 0; i < initLen; i++) {
    uint8_t command = buf[i] % 3; 
    int v; 

    switch (command) {
    case CMD_GENERATE: {
      if ((i+1+1) > initLen) { 
	i = buf.size();
	break;
      }
      READ_UINT8_FROM_FUZZBUF(buf, i+1, v);
      tb.generateTokens(v);
      i += 1;
      break;
    }

    case CMD_CONSUME: {
      if ((i+1+1) > initLen) {
	i = buf.size();
	break;
      }
      READ_UINT8_FROM_FUZZBUF(buf, i+1, v);
      tb.consume(v);
      i += 1;
      break;
    }

    default:
      break;
    }
  }
}
