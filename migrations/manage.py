#!/usr/bin/env python
from migrate.versioning.shell import main
from xiaoli.config import setting

if __name__ == '__main__':
    database_url = setting.DATABASE_URL
    main(url=database_url, debug='False', repository='migrations')
