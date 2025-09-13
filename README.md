# Tetris casero

Este proyecto consiste en un Tetris desarrollado con la biblioteca de software libre **Pygame**.  
**Pygame** es una biblioteca orientada a la creación de videojuegos y aplicaciones multimedia interactivas utilizando el lenguaje de programación **Python**.

El juego cuenta con tres pantallas principales: **Inicio**, **Partida** y **Final**.

## 📑 Índice

- [🚀 Pantalla de Inicio](#-pantalla-de-inicio)
- [🎮 Pantalla de Juego](#-pantalla-de-juego)
- [🏁 Pantalla Final](#-pantalla-final)

---
## 🚀 Pantalla de Inicio

En la pantalla de **inicio** se muestran los modos de juego disponibles:

- **Modo Normal**  
- **Modo Rápido**  
- **Modo Obstáculos**

Además, se muestra:

- El **ranking** con las 5 mejores puntuaciones obtenidas en cualquiera de los modos.
- La **mejor puntuación personal** lograda en la versión actual del juego.

![imagen inicial](documentary_imagenes/Inicial.png)

Para seleccionar un modo de juego utiliza las teclas:

- **↑ (arriba)** y **↓ (abajo)** para desplazarte entre los modos.
- **Enter** para confirmar la selección.


## 🎮 Pantalla de Juego

Una vez elegido el modo, aparecerá la pantalla principal de juego:

![imagen juego](documentary_imagenes/Juego.png)

La interfaz se divide en dos partes:

- **Izquierda**: el tablero donde se desarrolla el Tetris.
- **Derecha**: información detallada de la partida actual.

### Controles

- **↑ (UP)**: Rotar la pieza.  
- **↓ (DOWN)**: Bajar más rápido la pieza (útil para ganar más puntos).  
- **← (LEFT)**: Mover la pieza a la izquierda.  
- **→ (RIGHT)**: Mover la pieza a la derecha.  

### Información mostrada

![info partida](documentary_imagenes/Info_Partida.png)

- Una **animación** que aparece al eliminar líneas.
- **Puntuación actual** de la partida.
- **Mejor puntuación personal** alcanzada.
- Las **2 siguientes piezas** que aparecerán.
- El **Top 5** de puntuaciones (con las 3 iniciales de cada jugador).

## 🏁 Pantalla Final

Cuando ya no se puedan colocar más piezas, aparecerá la pantalla final:

![info partida](documentary_imagenes/Final.png)

Aquí deberás **introducir tu nombre** para guardar la puntuación obtenida.  
Presiona **Enter** para confirmar.

- Si no introduces ningún nombre o decides salir, no se guardará la puntuación y volverás al menú principal.
- Es posible que existan varias puntuaciones almacenadas con el mismo nombre.

## Comando para ejecutable

Primero descargar dependencias a traves de este comando:
```bash
    pip freeze < requirements.txt
```
Después ejecutar este comando para descargar el ejecutable .exe:
```bash
    pyinstaller --onefile --windowed --icon=icon_tetris.ico --add-data "imagenes;imagenes" --add-data "other;other" main.py
```
 Este ejecutable se encuentra en la carpeta **dist**.