# Microservicio de Productos hecho en Flask

## Configuración primera vez
1. Crear el entorno virtual (venv/env) y activarlo
2. instalar las dependencias/librerias con el comando pip install -r requirements.txt
3. Configurar las variables de entorno (.env.example)
    3.1 Configurar la base de datos local(No relacional) -> recomendación(MongoDb Compass)
        3.1.1 Aveces es necesario crear la colección "products"
    3.2 Configurar el contenedor de archivos

## Correr el servicio
* puedes modificar el app.run() para que este en debug *

```
app.run(debug=True)
```
finalmente solo se ejecuta por consola el comando 

```
flask run
```

