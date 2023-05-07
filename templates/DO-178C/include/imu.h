#include <stdint.h>

/**
 * Defines ARINC 429 word bitfield
 **/
typedef struct {
  /** parity bit **/
  uint32_t parity : 1;
  /** functional status **/
  uint32_t ssm : 2;
  /** data **/
  uint32_t data : 19;
  /** sender identifier **/
  uint32_t sdi : 2;
  /** message identifier **/
  uint32_t label : 8;
} a429_t;

/**
 * Defines IMU input record
 **/
typedef struct {
  /** acceleration x axis **/
  a429_t acc_x;
  /** acceleration y axis **/
  a429_t acc_y;
  /** acceleration z axis **/
  a429_t acc_z;
} imu_t;

/**
 *  process IMU input
 *  @input sensor input
 *  @return processing status 0: no error, else error code
 **/
int32_t imu(imu_t input);
