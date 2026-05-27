# 1. Imagen base: Usamos una versión ligera (alpine) de Node.js 18
FROM node:18-alpine

# 2. Directorio de trabajo: Carpeta interna donde vivirá el código en el contenedor
WORKDIR /usr/src/app

# 3. Instalación de dependencias: 
# Copiamos primero los archivos de paquetes para aprovechar la caché de Docker
COPY package*.json ./

# Ejecutamos la instalación de las dependencias definidas en tu package.json
RUN npm install

# 4. Copiado de código: Pasamos todo el contenido de la carpeta 'src' al contenedor
COPY . .

# 5. Puerto: Informamos que el contenedor escuchará en el puerto 3000
EXPOSE 3000

# 6. Comando de arranque: Ejecutamos el servidor
# Asegúrate de que en tu package.json el "main" apunte a "src/server.js"
CMD ["node", "src/server.js"]