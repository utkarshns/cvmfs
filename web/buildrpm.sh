#!/bin/sh

DEST_DIR=dist
PACKAGE_NAME=    # will be figured out later based on the
PACKAGE_VERSION= # naming conventions of the source tar ball
PACKAGE_PREFIX=/opt
PACKAGE_EPOCH=1
PACKAGE_ITERATION=1
SETUP_PY=$(readlink -f setup.py)

die() {
  local msg="$1"
  echo "$msg"
  exit 1
}

q() {
  local query="$1"
  local prevdir=$(pwd)
  cd $(dirname $SETUP_PY)
  python $SETUP_PY --$query || die "query $query failed"
  cd $prevdir
}

# do some sanity checks first
[ -d $DEST_DIR ]           && die "directory dist already exists"
which fpm > /dev/null 2>&1 || die "please install fpm first (gem install fpm)"


echo -n "building source tar ball... "
python $SETUP_PY sdist > /dev/null || die "fail!"
SOURCE_TAR="$(ls $DEST_DIR)"
cd $DEST_DIR
echo "done ($SOURCE_TAR)"

echo -n "extracting source tar ball and rename directory... "
tar xzf $SOURCE_TAR > /dev/null               || die "fail! (tar)"
SOURCE_DIR="$(q 'name')"
mv "$(q 'name')-$(q 'version')" "$SOURCE_DIR" || die "fail! (mv)"
echo "done"

echo -n "building rpm package... "
fpm -s dir -t rpm                                                 \
    --name          "$(q 'name')"                                 \
    --package       .                                             \
    --prefix        $PACKAGE_PREFIX                               \
    --version       "$(q 'version')"                              \
    --license       "$(q 'license')"                              \
    --iteration     $PACKAGE_ITERATION                            \
    --epoch         $PACKAGE_EPOCH                                \
    --architecture  all                                           \
    --vendor        "$(q 'author') <$(q 'author-email')>"         \
    --maintainer    "$(q 'contact') <$(q 'contact-email')>"       \
    --description   "$(q 'description')\n$(q 'long-description')" \
    --url           "$(q 'url')"                                  \
    --exclude       '*/MANIFEST.in'                               \
    --exclude       '*/PKG-INFO'                                  \
    --exclude       '*/setup.*'                                   \
    --exclude       '*.egg-info'                                  \
    --depends       'cvmfsutils   >= 0.1.0'                       \
    --depends       'Django14     >= 1.4'                         \
    --depends       'Django-south >= 0.7.5'                       \
    ${SOURCE_DIR} > /dev/null
[ $? -eq 0 ] || die "fail!"
echo "done"

echo -n "remove source directory... "
rm -fR "$SOURCE_DIR" || die "fail!"
echo "done"
