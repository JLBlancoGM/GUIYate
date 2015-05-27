# NOGYserver
Not only a graphical user interfaz for Yate server. 

NOGYserver es una interfaz gráfica de usuario para el servidor sip Yate y  que también permite configurar
un servidor DHCP y uno NTP. Incluye otras funcionalidades como la de manejar una base de datos para
la gestión  REGISTER del servidor SIP, ofrecer información sobre el estado de los servidores, de los usuarios
registrados y otras funcionalidades. El propósito de NOGYserver es disponer  de un entorno completo de laboratorio
que permita, en asuencia de una NGN real, realizar pruebas en dispositivos de VoIP (ATAs, centralitas, terminales VoIP,
etc...).       



NOGYserver add some extra functionalities:
- Configure and management the Yate SIP server.
- Register users.
- Configure and management DHCT and NTP server.
- Others capacities related with service quality.

This software is thinking to be executed in a linux system. Next will be described
the installation of a Debian/Ubuntu distribution.

Pre-requisites:

1) Python 2.7

2) Mysql:
   apt-get install mysql-client-5.5
   apt-get install mysql-server-5.5
   apt-get install libmysqlclient-dev
   apt-get install mysql-workbench
   apt-get install python-mysqldb

4) Django:
   install pip: apt-get install python-pip
   install django: pip install django
   install python-mysql: pat-get install python-mysqldb


3) Yate - Yet Another Telephony Engine (YATE)
   Download yate: http://yate.null.ro/tarballs/yate5/yate-5.4.2-1.tar.gz
   Decompress: tar -xzvf yate-5.4.2-1.tar.gz
   Install g++: apt-get install g++
   Install make: apt-get install make
   Move to yate dir: cd yate
   Configure and make: ./configure
                        make

4) DHCP Server
   Create dhcp-server in /opt
   Download dhcp-server: https://www.isc.org/downloads/
   Descompress:sudo tar -xzvf dhcp-4.2.8.tar.gz
   Go to dhcp source code: cd dhcp-4.2.8
   Configure:./configure --prefix=/opt/dhcp-server
   Make: make
   Install: make install
   Go to dhcp-server directory and make db directory: mkdir db
   Create in db the dhcpd.leases file: cd db
                                       touch dhcpd.leases
   Create and edit dhcpd.conf in etc directory.
   Run:
	./dhcpd -cf ../etc/dhcpd.conf -lf ../db/dhcpd.less

5)NTP Server
   Create dhcp-server in /opt
   Download ntp-server http://www.ntp.org/downloads.html
   Descompress:sudo tar -xzvf ntp-4.2.8p2.tar.gz 
   Go to ntp source code:cd ntp-4.2.8p2
   Configure:sudo ./configure --prefix=/opt/ntp-serve
   Make: make
   Install: make install


6)Database:
   Configure database:
        - root pass: rootdatabase
   Create database:
        mysql> CREATE DATABASE IF NOT EXISTS registerdb;
   Create user:
        mysql> CREATE USER 'sipserver'@'localhost' IDENTIFIED BY 'admin';
   Grant privileges:
        mysql> GRANT ALL PRIVILEGES ON registerdb.* TO 'sipserver'@'localhost';
   Create usertable:
        mysql> CREATE TABLE users ( username VARCHAR(128) UNIQUE, password VARCHAR(128), inuse INTEGER, location VARCHAR(1024), expires TIMESTAMP NULL DEFAULT NULL, type VARCHAR(20) NULL DEFAULT NULL)
