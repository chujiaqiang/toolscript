#/bin/sh

# Name: install_nginx_sh
# This scripts use to installl nginx on ubuntu, It will download gninx and related packages first
# and then install them automatically.
#

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

WORK_PATH='/fmt'

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to install this shell script"
    exit 1
fi

groupadd www
useradd -s /sbin/nologin -g www www

rm -Rf ${WORK_PATH}
mkdir -p ${WORK_PATH}
mkdir -p ${WORK_PATH}/packages
mkdir -p ${WORK_PATH}/data
mkdir -p ${WORK_PATH}/server
mkdir -p ${WORK_PATH}/log

cd ${WORK_PATH}/packages

URL_PCRE=ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.37.tar.gz
URL_ZLIB=http://zlib.net/zlib-1.2.8.tar.gz
URL_OPENSSL=http://www.openssl.org/source/openssl-1.0.2e.tar.gz
URL_NGINX=http://nginx.org/download/nginx-1.8.0.tar.gz

#refere to https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/

#the PCRE library – required for the Core and Rewrite modules and provides support for regular expressions:
wget $URL_PCRE
tar -zxf pcre-8.37.tar.gz
cd pcre-8.37
./configure
make && make install
cd ..


#the zlib library – required by the Gzip module for headers compression:
wget $URL_ZLIB
tar -zxf zlib-1.2.8.tar.gz
cd zlib-1.2.8
./configure
make && make install
cd ..


#the OpenSSL library – required the SSL module to support the HTTPS protocol:
wget $URL_OPENSSL
tar zxvf openssl-1.0.2e.tar.gz
cd openssl-1.0.2e
./config
make && make install
cd ..

#install the Nignx
wget $URL_NGINX
tar zxvf nginx-1.8.0.tar.gz
cd nginx-1.8.0

./configure \
        --user=www \
        --group=www \
        --prefix=${WORK_PATH}/server/nginx \
        --conf-path=${WORK_PATH}/server/nginx/nginx.conf \
        --pid-path=${WORK_PATH}/server/nginx/run/nginx.pid \
        --lock-path=${WORK_PATH}/server/nginx/run/nginx.lock \
        --sbin-path=${WORK_PATH}/server/nginx/sbin/nginx \
        --error-log-path=${WORK_PATH}/log/nginx/error.log \
        --http-log-path=${WORK_PATH}/log/nginx/access.log \
        --with-http_gzip_static_module \
        --with-http_ssl_module \
        --with-ipv6 \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-pcre \
        --http-client-body-temp-path=/var/cache/nginx/client_temp \
        --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=/var/cache/nginx/scgi_temp

make && make install

cd ..

mkdir -p /var/cache/nginx/client_temp
mkdir -p /var/cache/nginx/proxy_temp
mkdir -p /var/cache/nginx/fastcgi_temp
mkdir -p /var/cache/nginx/uwsgi_temp
mkdir -p /var/cache/nginx/scgi_temp

cd ${WORK_PATH}/server/nginx/sbin/
./nginx -c ${WORK_PATH}/server/nginx/nginx.conf


#http://nginx.org/en/linux_packages.html?_ga=1.138264499.2092786214.1447975135

#Configuration summary
#  + using system PCRE library
#  + using system OpenSSL library
#  + md5: using OpenSSL library
#  + sha1: using OpenSSL library
#  + using system zlib library
#
#  nginx path prefix: "${WORK_PATH}/server/nginx"
#  nginx binary file: "${WORK_PATH}/server/nginx/sbin/nginx"
#  nginx configuration prefix: "${WORK_PATH}/server/nginx"
#  nginx configuration file: "${WORK_PATH}/server/nginx/nginx.conf"
#  nginx pid file: "${WORK_PATH}/server/nginx/run/nginx.pid"
#  nginx error log file: "${WORK_PATH}/log/nginx/error.log"
#  nginx http access log file: "${WORK_PATH}/log/nginx/access.log"
#  nginx http client request body temporary files: "/var/cache/nginx/client_temp"
#  nginx http proxy temporary files: "/var/cache/nginx/proxy_temp"
#  nginx http fastcgi temporary files: "/var/cache/nginx/fastcgi_temp"
#  nginx http uwsgi temporary files: "/var/cache/nginx/uwsgi_temp"
#  nginx http scgi temporary files: "/var/cache/nginx/scgi_temp"


#issue
#root@ECS/etc/init.d/> ./nginx -s reload
#nginx: [error] open() "${WORK_PATH}/server/nginx/run/nginx.pid" failed (2: No such file or directory)
#Solution:
#Use: ${WORK_PATH}/server/nginx/sbin/nginx -c ${WORK_PATH}/server/nginx/nginx.conf

