#!/bin/bash

# 初始化数据库
mv /root/init-mysql.sh /init-mysql.sh
chmod 755 /init-mysql.sh
bash /init-mysql.sh mysqld
rm -f /init-mysql.sh

# 启动数据库
su - mysql -c "/usr/sbin/mysqld" &

# 启动Redis
service redis-server start

# 启动Nginx
service nginx start

# 等待数据库启动完成
until [ -e "/var/run/mysqld/mysqld.sock" ]
do
    sleep 0.1
done

# 数据库迁移
python3.7 /root/backend/business-server/manage.py migrate

# 启动服务
cd /root/backend/business-server
python3.7 manage.py runserver &

cd /root/backend/metting-room-server
go run main.go &

# 启动前端
cd /root/frontend
npm run serve

wait
