#! /usr/bin/env python
# From https://gist.github.com/achimnol/3021995

from __future__ import print_function
import sys, ctypes
from ctypes.util import find_library

SQLITE_OK = 0
SQLITE_ERROR = 1
SQLITE_BUSY = 5
SQLITE_LOCKED = 6

SQLITE_OPEN_READONLY = 1
SQLITE_OPEN_READWRITE = 2
SQLITE_OPEN_CREATE = 4

sqlite = ctypes.CDLL(find_library('sqlite3'))
sqlite.sqlite3_backup_init.restype = ctypes.c_void_p

if __name__ == '__main__':
  p_src_db = ctypes.c_void_p(None)
  p_dst_db = ctypes.c_void_p(None)
  null_ptr = ctypes.c_void_p(None)

  ret = sqlite.sqlite3_open_v2(sys.argv[1], ctypes.byref(p_src_db), SQLITE_OPEN_READONLY, null_ptr)
  assert ret == SQLITE_OK
  assert p_src_db.value is not None
  ret = sqlite.sqlite3_open_v2(sys.argv[2], ctypes.byref(p_dst_db), SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE, null_ptr)
  assert ret == SQLITE_OK
  assert p_dst_db.value is not None

  print('starting backup...')
  p_backup = sqlite.sqlite3_backup_init(p_dst_db, 'main', p_src_db, 'main')
  print('  backup handler: {0:#08x}'.format(p_backup))
  assert p_backup is not None

  while True:
    ret = sqlite.sqlite3_backup_step(p_backup, 20)
    remaining = sqlite.sqlite3_backup_remaining(p_backup)
    pagecount = sqlite.sqlite3_backup_pagecount(p_backup)
    amt = int((pagecount - remaining) / float(pagecount) * 100)
    sys.stdout.write('\rbackup in progress: %d%% %s' % (amt, "|" + (amt) * "#" + (100 - amt) * " " + "|"))
    sys.stdout.flush()
    if remaining == 0:
      break
    if ret in (SQLITE_OK, SQLITE_BUSY, SQLITE_LOCKED):
      sqlite.sqlite3_sleep(100)

  sqlite.sqlite3_backup_finish(p_backup)

  sqlite.sqlite3_close(p_dst_db)
  sqlite.sqlite3_close(p_src_db)
