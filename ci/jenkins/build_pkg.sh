#!/bin/sh

echo "Continuous Integration PKG Build Script"

script_location=$(cd $(dirname "$0") && pwd -P)
. ${script_location}/common.sh

if [ $# -ne 1 ]; then
  echo "USAGE: $0 <source tarball>"
  exit 1
fi

# collect information about the package to be built
source_tarball="$1"

export PATH=/usr/local/bin:$PATH
export DYLD_LIBRARY_PATH=/usr/local/lib:$DYLD_LIBRARY_PATH
cp $source_tarball $[workdir]/src/cvmfs.tar.gz
cd $[workdir]/src
tar xvfz cvmfs.tar.gz
cd $[workdir]/src/$[build_tag]
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SERVER=no -DBUILD_UNITTESTS=no .
make

cd $[workdir]/tmp/packaging/mac
./build_pkg.sh -b $[workdir]/src/$[build_tag]
mv cvmfs.pkg $[build_tag].pkg
