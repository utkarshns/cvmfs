/**
 * This file is part of the CernVM File System.
 */

#include <gtest/gtest.h>

#include "../../cvmfs/smalloc.h"

TEST(T_Smalloc, 1byteAllocation) {
  void *mem = smalloc(1);
  EXPECT_TRUE(NULL != mem);
  free(mem);
}

TEST(T_Smalloc, 2gBAllocation) {
  void* mem = smalloc(2147483648);
  EXPECT_TRUE(NULL != mem);
  free(mem);
}

TEST(T_Smalloc, ZeroAllocation) {
  void* mem = smalloc(0);
  EXPECT_TRUE(NULL != mem);
  free(mem);
}

TEST(T_Srealloc, GrowNULL) {
  void* mem = NULL;
  mem = srealloc(mem, 512);
  EXPECT_TRUE(NULL != mem);
  free(mem);
}

TEST(T_Srealloc, reAlloc) {
  void* mem = smalloc(1024);
  EXPECT_TRUE(NULL != mem);
  mem = srealloc(mem, 2048);
  EXPECT_TRUE(NULL != mem);
  mem = srealloc(mem, 512);
  EXPECT_TRUE(NULL != mem);
  free(mem);
}

TEST(T_Scalloc, calloc) {
  int* mem = static_cast<int*>(scalloc(16, 32));
  ASSERT_TRUE(NULL != mem);
  for (const int* ptr = mem; ptr < mem+16; ptr++) {
    EXPECT_EQ(0, *ptr);
  }
  free(mem);
}

TEST(T_Smmap, map_alloc) {
  size_t size = 1024;
  char* mem = static_cast<char*>(smmap(size));
  char* pg = mem - 2*sizeof(size_t);
  EXPECT_TRUE(MAP_FAILED != mem);
  EXPECT_TRUE(*(reinterpret_cast<size_t*>(pg))==0xaaaaaaaa);
  size_t pages = ((size + 2 * sizeof(size_t)) + 4095) / 4096;
  EXPECT_TRUE(*(reinterpret_cast<size_t*>(pg) + 1)==pages);
}

