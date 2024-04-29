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

# 安装Vue依赖
cd /root/frontend
npm install

# 安装golang依赖
cd /root/backend/metting-room-server
go mod download

# 安装Django依赖
pip3 install -r /root/backend/business-server/requirements.txt

# 等待数据库启动完成
until [ -e "/var/run/mysqld/mysqld.sock" ]
do
    sleep 0.1
done

# 数据库迁移
python3.7 /root/backend/business-server/manage.py migrate

echo "环境初始化完成。"

wait
