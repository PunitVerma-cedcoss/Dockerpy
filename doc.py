import subprocess
import time
docker_compose = """
version: "3.7"
services:
  web-server:
    build:
      dockerfile: php.Dockerfile
      context: .
    restart: always
    volumes:
      - "./src/:/var/www/html/"
    ports:
      - "8080:80"
  mysql-server:
    image: mysql:8.0.19
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - mysql-data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin/phpmyadmin:5.0.1
    restart: always
    environment:
      PMA_HOST: mysql-server
      PMA_USER: root
      PMA_PASSWORD: secret
    ports:
      - "5000:80"
volumes:
  mysql-data:
""".strip()
dockerphp = """
FROM php:7.4.3-apache
RUN docker-php-ext-install mysqli pdo pdo_mysql
""".strip()
def pprint(msg,color=""):
    if color == 'green':
      print(f"\033[32m{msg}\033[0m")
    else:
      print(f"\033[35m{msg}\033[0m")
pprint("""
       ______ _____ _____  _   __ ___________________   __     
       |  _  \  _  /  __ \| | / /|  ___| ___ \ ___ \ \ / /     
 ______| | | | | | | /  \/| |/ / | |__ | |_/ / |_/ /\ V /_____ 
|______| | | | | | | |    |    \ |  __||    /|  __/  \ /______|
       | |/ /\ \_/ / \__/\| |\  \| |___| |\ \| |     | |       
       |___/  \___/ \____/\_| \_/\____/\_| \_\_|     \_/by PUNIT VERMA       
                                                               
                                                                                                        
""")
p = subprocess.Popen('pwd', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
res = p.stdout.readlines()
pwd = res[0].decode('utf-8').replace("\n",'')
folder_name = input(" >> ").strip()
if folder_name.count(" ") > 0:
    folder_name = '_'.join(folder_name.split(" "))
pprint("[+] "+pwd+"/"+folder_name)
subprocess.Popen('mkdir '+pwd+"/"+folder_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
new_dir = pwd+"/"+folder_name + "/"
pprint("[+] dir created")
pprint("[+] creating src dir ")
subprocess.Popen('mkdir '+pwd+"/"+folder_name+"/src", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pprint("[+] moving docker files ")
time.sleep(1)
with open(pwd+"/"+folder_name+"/docker-compose.yml","w") as file:
    file.write(docker_compose)
with open(pwd+"/"+folder_name+"/php.Dockerfile","w") as file:
    file.write(dockerphp)
pprint("[+] docker files created successfully - ")
subprocess.Popen('code '+pwd+"/"+folder_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pprint("[+] vscode started")
ch = input('stop docker containers >> ').lower()
if ch == 'y' or ch == 'yes':
  pprint("killing docker")
  subprocess.Popen('docker kill $(docker ps -q)', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  pprint("docker stopped successfully")