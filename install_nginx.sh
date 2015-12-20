
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to install this shell script"
    exit 1
fi

groupadd www
useradd -s /sbin/nologin -g www www

rm -Rf /fmt
mkdir /fmt
mkdir /fmt/packages
mkdir /fmt/data
mkdir /fmt/server
mkdir /fmt/log


cd /fmt/packages


#refere to https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/

#the PCRE library – required for the Core and Rewrite modules and provides support for regular expressions:
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.37.tar.gz
tar -zxf pcre-8.37.tar.gz
cd pcre-8.37
./configure
make && make install

cd ..


#the zlib library – required by the Gzip module for headers compression:
wget http://zlib.net/zlib-1.2.8.tar.gz
tar -zxf zlib-1.2.8.tar.gz
cd zlib-1.2.8
./configure
make && make install

cd ..


#the OpenSSL library – required the SSL module to support the HTTPS protocol:
wget http://www.openssl.org/source/openssl-1.0.2e.tar.gz
tar zxvf openssl-1.0.2e.tar.gz
cd openssl-1.0.2e
./config
make && make install

cd ..

#install the Nignx
wget http://nginx.org/download/nginx-1.8.0.tar.gz
tar zxvf nginx-1.8.0.tar.gz
cd nginx-1.8.0

./configure \
        --user=www \
        --group=www \
        --prefix=/fmt/server/nginx \
        --conf-path=/fmt/server/nginx/nginx.conf \
        --pid-path=/fmt/server/nginx/run/nginx.pid \
        --lock-path=/fmt/server/nginx/run/nginx.lock \
        --sbin-path=/fmt/server/nginx/sbin/nginx \
        --error-log-path=/fmt/log/nginx/error.log \
        --http-log-path=/fmt/log/nginx/access.log \
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

cd /fmt/server/nginx/sbin/
./nginx -c /fmt/server/nginx/nginx.conf


#http://nginx.org/en/linux_packages.html?_ga=1.138264499.2092786214.1447975135
		
#Configuration summary
#  + using system PCRE library
#  + using system OpenSSL library
#  + md5: using OpenSSL library
#  + sha1: using OpenSSL library
#  + using system zlib library
#
#  nginx path prefix: "/fmt/server/nginx"
#  nginx binary file: "/fmt/server/nginx/sbin/nginx"
#  nginx configuration prefix: "/fmt/server/nginx"
#  nginx configuration file: "/fmt/server/nginx/nginx.conf"
#  nginx pid file: "/fmt/server/nginx/run/nginx.pid"
#  nginx error log file: "/fmt/log/nginx/error.log"
#  nginx http access log file: "/fmt/log/nginx/access.log"
#  nginx http client request body temporary files: "/var/cache/nginx/client_temp"
#  nginx http proxy temporary files: "/var/cache/nginx/proxy_temp"
#  nginx http fastcgi temporary files: "/var/cache/nginx/fastcgi_temp"
#  nginx http uwsgi temporary files: "/var/cache/nginx/uwsgi_temp"
#  nginx http scgi temporary files: "/var/cache/nginx/scgi_temp"


#issue
#root@ECS/etc/init.d/> ./nginx -s reload
#nginx: [error] open() "/fmt/server/nginx/run/nginx.pid" failed (2: No such file or directory)
#Solution:
#Use: /fmt/server/nginx/sbin/nginx -c /fmt/server/nginx/nginx.conf

