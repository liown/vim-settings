#!/bin/bash

GUACAMOLE_HOME=/etc/guacamole

sudo apt-get install libcairo2-dev -y
sudo apt-get install libossp-uuid-dev -y
sudo apt-get install libfreerdp-dev -y
sudo apt-get install libpango1.0-dev -y
sudo apt-get install libavcodec-dev -y
sudo apt-get install libavutil-dev -y
sudo apt-get install libswscale-dev -y
sudo apt-get install libssh2-1-dev -y
sudo apt-get install libtelnet-dev -y
sudo apt-get install libssl-dev -y
sudo apt-get install libwebp-dev -y
sudo apt-get install libvorbis-dev -y
sudo apt-get install libpulse-dev -y
sudo apt-get install libvncserver-dev -y

tar -xvf guacamole-server-0.9.13-incubating.tar.gz
if [$? -ne 0];then
    echo "uncompression guacamole server failed"
    exit
fi
cd guacamole-server-0.9.13-incubating
if [$? -ne 0];then
    echo "into guacamole server directory failed"
    exit
fi
./configure --with-init-dir=/etc/init.d
sudo make && sudo make install
if [$? -ne 0];then
    echo "install guacamole server failed"
    exit
fi
cd -
if [$? -ne 0];then
    echo "leaving directory failed"
    exit
fi
if [ `ps -ef | grep tomcat | grep -v grep |wc -l` -eq 0 ];then
    sudo apt-get install tomcat8 -y
fi
TOMCAT=`ps -ef | grep tomcat | grep -v grep | awk '{print $1}'`
sudo cp guacamole.war /var/lib/$TOMCAT/webapps/
if [ ! -d "$GUACAMOLE_HOME" ];then
    sudo mkdir "$GUACAMOLE_HOME"
fi
sudo ln -s -f "$GUACAMOLE_HOME" /usr/share/$TOMCAT/.guacamole
sudo cp noauth-config.xml guacamole.properties "$GUACAMOLE_HOME"
sudo mkdir "$GUACAMOLE_HOME/extensions"
sudo cp guacamole-auth-noauth*.jar "$GUACAMOLE_HOME/extensions"
sudo /etc/init.d/$TOMCAT restart
sudo /etc/init.d/guacd restart
