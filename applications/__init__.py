import os

if os.getenv("dockerrun", "no") == "yes":
    from gevent import monkey

    from component.mysql_pool import patch_mysql

    monkey.patch_all(thread=False)
    patch_mysql()
