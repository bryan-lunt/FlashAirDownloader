
from BackupDaemon import BackupDaemon

db_path = "/tmp/testdatabasebd.db"
command_file = "/tmp/foofile"
base_dir = "/tmp/base"
tmp_dir = "/tmp/mytmp"

D = BackupDaemon(command_file, db_path, base_dir, tmp_dir)
D.run()
