#include <gtest/gtest.h>

#include <pthread.h>
#include <string>

#include "../../cvmfs/hash.h"

class T_Hmac : public ::testing::Test {
 protected:
  virtual void SetUp() {
    md5.algorithm = shash::kMd5;
    sha1.algorithm = shash::kSha1;
  }

 protected:
  shash::Any md5;
  shash::Any sha1;
};


TEST_F(T_Hmac, Sha1) {
  std::string key = "";
  std::string data = "";
  shash::Hmac(key, (unsigned char *)data.data(), data.length(), &sha1);
  EXPECT_EQ (sha1.ToString(), "fbdb1d1b18aa6c08324b7d64b71fb76370690e1d");

  key = "key";
  data = "The quick brown fox jumps over the lazy dog";
  shash::Hmac(key, (unsigned char *)data.data(), data.length(), &sha1);
  EXPECT_EQ (sha1.ToString(), "de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9");
}

TEST_F(T_Hmac, Md5) {
  std::string key = "";
  std::string data = "";
  shash::Hmac(key, (unsigned char *)data.data(), data.length(), &md5);
  EXPECT_EQ (md5.ToString(), "74e6f7298a9c2d168935f58c001bad88");

  key = "key";
  data = "The quick brown fox jumps over the lazy dog";
  shash::Hmac(key, (unsigned char *)data.data(), data.length(), &md5);
  EXPECT_EQ (md5.ToString(), "80070713463e7749b90c2dc24911e275");
}

