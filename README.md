 AWS Cloud URL Shortener

Un acortador de enlaces Full-Stack desplegado completamente en Amazon Web Services (AWS). Este proyecto demuestra una integración nativa entre servicios de almacenamiento estático, cómputo escalable y bases de datos NoSQL, garantizando alta disponibilidad y baja latencia.

 Arquitectura del Proyecto

La aplicación está diseñada en tres capas principales:

Frontend (Amazon S3): Interfaz moderna con Glassmorphism alojada como Static Website Hosting.

Backend (Amazon EC2): API RESTful construida con FastAPI (Python), ejecutada mediante un servicio systemd y expuesta a través de un proxy inverso con Nginx.

Base de Datos (Amazon DynamoDB): Almacenamiento rápido y flexible de enlaces utilizando la clave de partición generada (UUID). La conexión se realiza de forma segura mediante un IAM Role, sin credenciales quemadas en código.

 Guía de Despliegue

Para replicar este proyecto y que funcione perfectamente, sigue estos pasos:

1. Preparar la Base de Datos (DynamoDB)

Ve a la consola de AWS y abre DynamoDB.

Crea una tabla con las siguientes especificaciones:

Table name: url-shortener-links

Partition key: short_code (Tipo: String)

Capacity mode: On-demand (para evitar costos innecesarios).

2. Configurar el Servidor (EC2)

Lanza una instancia Ubuntu Server 24.04 LTS (t2.micro).

Importante: Crea y asígnale un IAM Role a la instancia con permisos de lectura/escritura (AmazonDynamoDBFullAccess o políticas personalizadas) para que pueda interactuar con la tabla url-shortener-links.

Abre los puertos 80 (HTTP) y 22 (SSH) en el Security Group.

3. Despliegue del Backend (FastAPI + Nginx)

Conéctate por SSH a tu instancia EC2:

ssh -i "tu-llave.pem" ubuntu@<TU_IP_PUBLICA>


Clona este repositorio, crea el entorno virtual e instala las dependencias:

sudo apt update && sudo apt install python3-venv nginx -y
git clone <TU_URL_DEL_REPOSITORIO>
cd Acortador-de-enlaces-AWS/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Configurar Variables de Entorno: Crea un archivo .env en la carpeta backend y añade tu IP pública:

BASE_URL=http://<TU_IP_PUBLICA>


Configurar Nginx (Proxy Inverso): Edita el archivo de configuración por defecto:

sudo nano /etc/nginx/sites-available/default


Asegúrate de configurar la redirección del tráfico a FastAPI:

server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


Reinicia Nginx: sudo systemctl restart nginx

Crear el servicio de FastAPI en segundo plano:
Inicia tu aplicación en el puerto 8000 (o configúrala como servicio systemd para que arranque sola).

4. Despliegue del Frontend (Amazon S3)

Abre el archivo frontend/js/app.js localmente.

Modifica la variable API_BASE en la primera línea con la IP de tu EC2:

const API_BASE = "http://<TU_IP_PUBLICA>"; // Ej: http://3.93.175.66


Ve a Amazon S3 y crea un Bucket público.

Activa la opción de Static website hosting (alojamiento de sitios web estáticos).

Sube el contenido de la carpeta frontend/ (archivos index.html, carpeta css/ y js/).

Configura la Bucket Policy para permitir lectura pública (s3:GetObject).

 Solución de Problemas Comunes

Error 405 Method Not Allowed: Ocurre si pruebas el frontend localmente con Live Server o si la variable API_BASE en app.js apunta al lugar equivocado. Asegúrate de probar desde la URL pública de S3 y de que apunte a la IP correcta del EC2.

Enlaces cortos inalcanzables (localhost): Si el enlace generado redirige a localhost, es porque olvidaste crear o configurar correctamente el archivo .env con la variable BASE_URL en tu servidor EC2.

Error 500 al acortar: Verifica que la instancia EC2 tenga el IAM Role adjunto para acceder a DynamoDB.

 Autor

Emilio Granda

Estudiante de Ingeniería en Sistemas de la Información - UIDE.

Proyecto final para demostración de despliegue Cloud (Frontend, Backend, Database).