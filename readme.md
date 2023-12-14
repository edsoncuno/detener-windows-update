# Detener Windows Update
[![menu.png](https://i.postimg.cc/K8kXbtLr/menu.png)](https://postimg.cc/VJ8ZBrKd)

## Proposito

Este programa sirve para detener la constante busqueda de actualizaciones de windows 10
Para utilizarlo, hay que ejecutar el archivo "main.py" como administrador.
O si se ha egenrador el .exe, hay que ejecutarlo como administrador.

## Dependencias

Recordar actualizar pip
```sh
python -m pip install --upgrade pip
```

## Generar .exe

El paquete que utiliza generar el .exe:
```sh
pip install auto-py-to-exe
```

Para usar auto-py-to-exe hay que abrir el PowerShell y ejecutar:
```sh
auto-py-to-exe
```
- Seleccionar el script que se quiere convertir a .exe
- Onefile: One File
- Console Window: Console Based
- CONVERT .PY TO .EXE

Recordar que el resultado esta dentro de la carpeta del script,
en la carpeta "output"
