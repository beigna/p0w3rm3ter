# PowerMeter

## Ejecución
El projecto está armado para ser ejecutado con Docker, tanto para probarlo como para continuar su desarollo (el Dockerfile.dev que adjunto no está pensado para producción).
Por otro lado utilizo un esquema modular en el projecto Django propiamente dicho, con requerimientos en cascada según dónde se vaya a utilizar (producción, testing o desarrollo local).

Se requiere tener instalado Docker y make, detallo los pasos a continuación:

`make docker-build-dev`: Crea la imagen de Docker con Python, las dependencias del proyecto y lo monta. Esto permite editar el projecto sin tener que rehacer la imagen.

`make docker-shell`: Instancia un contenedor y nos sitúa en el raíz del repo.

`make docker-start`: Ejecuta las migraciones de Django y luego runserver.

## Tarea 1
Se utilizó DRF para los puntos solicitados, sin mucho que agregar más que el caso del consumo negativo: el mismo se descarta sin lanzar excepciones aunque con un status code 204.

Las URLs son:

`api/v1/devices/` device-list

`api/v1/devices/<pk>/` device-detail

`api/v1/devices/<pk>/avg_consumption/` device-avg-consumption

`api/v1/devices/<pk>/max_consumption/` device-max-consumption

`api/v1/devices/<pk>/min_consumption/` device-min-consumption

`api/v1/devices/<pk>/total_consumption/` device-total-consumption

`api/v1/meterings/` metering-list

`api/v1/meterings/<pk>/` metering-detail
