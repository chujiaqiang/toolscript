#bin/ksh

#uninstal nginx
#sudo apt-get --purge remove nginx
#rm -Rf /usr/local/nginx
#rm -Rf /var/log/nginx/

#依赖的目录
work_dir=/fmt
src_base_dir=${work_dir}/packages
src_openssl_dir=${src_base_dir}/openssl-1.0.2e
src_pcre_dir=${src_base_dir}/pcre-8.37
src_nginx_dir=${src_base_dir}/nginx-1.8.0


#refere to https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/

#the PCRE library – required for the Core and Rewrite modules and provides support for regular expressions:
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.37.tar.gz
tar -zxf pcre-8.37.tar.gz
cd pcre-8.37
./configure
make
sudo make install

#the zlib library – required by the Gzip module for headers compression:
wget http://zlib.net/zlib-1.2.8.tar.gz
tar -zxf zlib-1.2.8.tar.gz
cd zlib-1.2.8
./configure
make
sudo make install

#the OpenSSL library – required the SSL module to support the HTTPS protocol:
wget http://www.openssl.org/source/openssl-1.0.2e.tar.gz
tar zxvf openssl-1.0.2e.tar.gz
cd openssl-1.0.2e
./configure darwin64-x86_64-cc --prefix=/usr
make
sudo make install

#Installing NGINX Open Source
nginx_version=
rm -Rf nginx-${nginx_version}

wget http://nginx.org/download/nginx-1.8.0.tar.gz
tar zxvf nginx-1.8.0.tar.gz
cd nginx-1.8.0



 
#=============================================================================
#目标的目录
dest_base_dir=${work_dir}/release
dest_nginx_dir=${dest_base_dir}/nginx

rm -Rf $dest_nginx_dir
mkdir $dest_nginx_dir


cd nginx-1.8.0

#./configure --with-http_stub_status_module --with-http_ssl_module --with-openssl=$src_openssl_dir --with-pcre=$src_pcre_dir --prefix=$dest_nginx_dir

./configure \
    --user=www \
    --group=www \
    --prefix=/fmt/se/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --pid-path=/usr/local/nginx/nginx.pid \
    --sbin-path=/usr/local/bin\
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \

    --with-http_ssl_module \
#    --with-openssl=../openssl-1.0.2e \
#    --with-pcre=../pcre-8.37 \
#    --with-zlib=../zlib-1.2.8 \

make 
sudo make install


#http://nginx.org/en/linux_packages.html?_ga=1.138264499.2092786214.1447975135
#
#Configure arguments common for nginx binaries from pre-built packages for stable version:
#--prefix=/etc/nginx
#--sbin-path=/usr/sbin/nginx
#--conf-path=/etc/nginx/nginx.conf
#--error-log-path=/var/log/nginx/error.log
#--http-log-path=/var/log/nginx/access.log
#--pid-path=/var/run/nginx.pid
#--lock-path=/var/run/nginx.lock
#--http-client-body-temp-path=/var/cache/nginx/client_temp
#--http-proxy-temp-path=/var/cache/nginx/proxy_temp
#--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp
#--http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp
#--http-scgi-temp-path=/var/cache/nginx/scgi_temp
#--user=nginx
#--group=nginx
#--with-http_ssl_module
#--with-http_realip_module
#--with-http_addition_module
#--with-http_sub_module
#--with-http_dav_module
#--with-http_flv_module
#--with-http_mp4_module
#--with-http_gunzip_module
#--with-http_gzip_static_module
#--with-http_random_index_module
#--with-http_secure_link_module
#--with-http_stub_status_module
#--with-http_auth_request_module
#--with-mail
#--with-mail_ssl_module
#--with-file-aio
#--with-http_spdy_module
#--with-ipv6







