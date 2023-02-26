import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

def obtener_robots_txt(url):
    return requests.get(url + '/robots.txt')

def extraer_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return re.findall('(?:href=")(.*?)"', str(soup))

def escaneo(url):
    response = requests.get(url)
    if response.status_code == 200:
        print('[+] El sitio web está activo')
        robots = obtener_robots_txt(url)
        print(f'[+] El archivo robots.txt se ha obtenido: \n{robots.text}')
        links = extraer_links(url)
        for link in links:
            href = urllib.parse.urljoin(url, str(link))
            print(f'[+] Se encontró el enlace: {href}')
    else:
        print('[-] El sitio web no está activo')

def escaneo_subdominios(dominio):
    url = f'https://www.google.com/search?q=site:*.{dominio}&num=100'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    subdominios = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('/url?q=') and not href.startswith('/url?q=https://www.google.com'):
            subdominio = re.findall(r'/url\?q=(.*?)&', href)[0]
            subdominios.append(subdominio)
    subdominios = list(set(subdominios))
    for subdominio in subdominios:
        print(f'[+] Subdominio encontrado: {subdominio}')

def escaneo_aplicaciones_web(url):
    dir_list = ['/admin', '/login', '/wp-admin', '/wp-login', '/administrator', '/phpmyadmin', '/joomla/administrator', '/admin.php', '/index.php/admin', '/admin/index.php', '/admin/login.php', '/admin/login.aspx', '/user/login', '/admin/index.aspx', '/admin/index.asp', '/admin/index.php/login']
    for d in dir_list:
        r = requests.get(url + d)
        if r.status_code == 200:
            print(f'[+] Se encontró el directorio: {url + d}')

def escaneo_ftp(dominio, usuario, contrasena):
    servidor_ftp = dominio
    try:
        ftp = FTP(servidor_ftp)
        ftp.login(usuario, contrasena)
        print(f'[+] Se pudo iniciar sesión en el servidor FTP: {servidor_ftp}')
        ftp.quit()
    except:
        print(f'[-] No se pudo iniciar sesión en el servidor FTP: {servidor_ftp}')

def escaneo_smtp(servidor, usuario, contrasena):
    try:
        server = smtplib.SMTP(servidor, 587)
        server.starttls()
        server.login(usuario, contrasena)
        print(f'[+] Se pudo iniciar sesión en el servidor SMTP: {servidor}')
        server.quit()
    except:
        print(f'[-
