#include <gtest/gtest.h>

#include <pthread.h>
#include <string>

#include "../../cvmfs/util.h"

class T_Base64 : public ::testing::Test {
 protected:
  virtual void SetUp() {
  }

 protected:
  std::string enc;
};


TEST_F(T_Base64, Basics) {
  enc = Base64("Man");
  EXPECT_EQ (enc, "TWFu");

  enc = Base64("any carnal pleasure.");
  EXPECT_EQ (enc, "YW55IGNhcm5hbCBwbGVhc3VyZS4=");

  enc = Base64("any carnal pleasure");
  EXPECT_EQ (enc, "YW55IGNhcm5hbCBwbGVhc3VyZQ==");

  enc = Base64("any carnal pleasur");
  EXPECT_EQ (enc, "YW55IGNhcm5hbCBwbGVhc3Vy");

  enc = Base64("any carnal pleasu");
  EXPECT_EQ (enc, "YW55IGNhcm5hbCBwbGVhc3U=");

  enc = Base64("any carnal pleas");
  EXPECT_EQ (enc, "YW55IGNhcm5hbCBwbGVhcw==");
}


TEST_F(T_Base64, MoreBasics) {
  enc = Base64(
    "Man is distinguished, not only by his reason, but by this singular passion from "
    "other animals, which is a lust of the mind, that by a perseverance of delight "
    "in the continued and indefatigable generation of knowledge, exceeds the short "
    "vehemence of any carnal pleasure.");
  EXPECT_EQ (enc,
    "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCBieSB0aGlz"
    "IHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxzLCB3aGljaCBpcyBhIGx1c3Qgb2Yg"
    "dGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZXZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGlu"
    "dWVkIGFuZCBpbmRlZmF0aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRo"
    "ZSBzaG9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4=");
}
