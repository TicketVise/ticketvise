#! /bin/sh

# LINUX2 - shell script to set up a Postfix chroot jail for Linux
# Tested on SuSE Linux 5.3 (libc5) and 7.0 (glibc2.1)

# Other testers reported as working:
#
# 2001-01-15 Debian sid (unstable)
#            Christian Kurz <shorty@getuid.de>

# Copyright (c) 2000 - 2001 by Matthias Andree
# Redistributable unter the MIT-style license that follows:
# Abstract: "do whatever you want except hold somebody liable or change
# the copyright information".

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# 2000-09-29
# v0.1: initial release

# 2000-12-05
# v0.2: copy libdb.* for libnss_db.so
#       remove /etc/localtime in case it's a broken symlink
#       restrict find to maxdepth 1 (faster)

# Revision 1.4  2001/01/15 09:36:35  emma
# add note it was successfully tested on Debian sid
#
# 20060101 /lib64 support by Keith Owens.
#

CP="cp -pv"

cond_copy() {
  # find files as per pattern in $1
  # if any, copy to directory $2
  dir=`dirname "$1"`
  pat=`basename "$1"`
  lr=`find "$dir" -maxdepth 1 -name "$pat"`
  if test ! -d "$2" ; then exit 1 ; fi
  if test "x$lr" != "x" ; then $CP $1 "$2" ; fi
}

set -e
umask 022

POSTFIX_DIR=${POSTFIX_DIR-/var/spool/postfix}
cd ${POSTFIX_DIR}

mkdir -p etc lib usr/lib/zoneinfo
test -d /lib64 && mkdir -p lib64

# find localtime (SuSE 5.3 does not have /etc/localtime)
lt=/etc/localtime
if test ! -f $lt ; then lt=/usr/lib/zoneinfo/localtime ; fi
if test ! -f $lt ; then lt=/usr/share/zoneinfo/localtime ; fi
if test ! -f $lt ; then echo "cannot find localtime" ; exit 1 ; fi
rm -f etc/localtime

# copy localtime and some other system files into the chroot's etc
$CP -f $lt /etc/services /etc/resolv.conf /etc/nsswitch.conf etc
$CP -f /etc/host.conf /etc/hosts /etc/passwd etc
ln -s -f /etc/localtime usr/lib/zoneinfo

# copy required libraries into the chroot
cond_copy '/lib/x86_64-linux-gnu/libnss_*.so*' lib
cond_copy '/lib/x86_64-linux-gnu/libresolv.so*' lib
cond_copy '/lib/x86_64-linux-gnu/libdb.so*' lib
if test -d /lib64; then
  cond_copy '/lib64/ld-linux-x86-64.so*' lib64
fi

# enable tls if volume is attached
if test -d /etc/letsencrypt; then
  echo "Let's Encrypt volume attached, enabling TLS"
  postconf -e "smtpd_tls_cert_file = /etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
  postconf -e "smtpd_tls_key_file = /etc/letsencrypt/live/${DOMAIN}/privkey.pem"
  postconf -e "smtpd_tls_security_level=may"
fi

exec "$@"
