# Instrucciones para realizar el setup

## 1. Asegurarse de tener instalado Python 3 en su sistema. 
Puedes verificarlo ejecutando el siguiente comando:
```python
python --version
```
## 2. Crear un entorno virtual.
- Abre una terminal o símbolo del sistema y navega a la carpeta donde tienes tus archivos `producer.py` y `consumer.py`.
- Crea un entorno virtual con el siguiente comando:
```python
python -m venv .venv
```

## 3. Activa el entorno virtual.
- En Windows:
```python
.venv\Scripts\activate
```
  - En macOS:
```python
source .venv/bin/activate
```
Una vez activado el entorno, debes ver el prefijo `(venv)` al inicio de tu terminal.

## 4. Instalar librerías.
- Con el entorno virtual activado, instala las librerías `pika` y `pyserial` con los siguientes comandos:
```python
pip install pika pyserial
```
Eso instalará ambas librerías.

## 5. Ejecutar el archivo `producer.py`.
- Abre una terminal o símbolo del sistema en la misma carpeta y asegúrate de activar el entorno virtual.
- Ejecuta `producer.py` para enviar una operación matemática al queue en CloudAMQP:
```python
python producer.py
```
- El programa pedirá que ingreses una operación matemática (por ejemplo, 5+3). Al enviarla, `consumer.py` recibirá el mensaje, procesará el cálculo y enviará el resultado a la ESP32.