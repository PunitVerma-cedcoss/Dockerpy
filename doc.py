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
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="main.css">
    <title>Document</title>
</head>
<body>
    
</body>
</html>
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
pprint("[\U0001f600] "+pwd+"/"+folder_name)
subprocess.Popen('mkdir '+pwd+"/"+folder_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
new_dir = pwd+"/"+folder_name + "/"
pprint("[+] dir created","green")
pprint("[+] creating src dir ")
subprocess.Popen('mkdir '+pwd+"/"+folder_name+"/src", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pprint("[+] generating default html setup")
time.sleep(1)
with open(pwd+"/"+folder_name+"/src/index.html","w") as file:
  file.write(html)
with open(pwd+"/"+folder_name+"/src/main.css","w") as file:
  file.write('')
pprint("[\U0001f929] default html setup generated","green")
pprint("[+] moving docker files ")
time.sleep(1)
with open(pwd+"/"+folder_name+"/docker-compose.yml","w") as file:
    file.write(docker_compose)
with open(pwd+"/"+folder_name+"/php.Dockerfile","w") as file:
    file.write(dockerphp)
pprint("[+] docker files created successfully \U0001f60e ","green")
subprocess.Popen('git init '+pwd+"/"+folder_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pprint("[+] git initlizied","green")
subprocess.Popen('code '+pwd+"/"+folder_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pprint("[+] vscode started","green")
ch = input('stop docker containers >> ').lower()
if ch == 'y' or ch == 'yes':
  pprint("killing docker")
  subprocess.Popen('docker kill $(docker ps -q)', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  pprint("docker stopped successfully","green")