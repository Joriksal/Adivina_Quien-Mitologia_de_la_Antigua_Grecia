# Adivina Quién: Mitología de la Antigua Grecia

## Descripción del Proyecto

"Adivina Quién: Mitología de la Antigua Grecia" es un juego interactivo que desafía a una Inteligencia Artificial a adivinar personajes (dioses, héroes, monstruos) de la mitología griega en los que el usuario está pensando. Lo más notable de este proyecto es su capacidad de **aprendizaje**: si la IA falla, el usuario puede enseñarle nuevos personajes y preguntas distintivas, expandiendo así la base de conocimiento del sistema de forma persistente.

Este proyecto sirve como una implementación práctica y funcional de un **sistema experto** básico, utilizando un árbol de decisión para el motor de inferencia y la capacidad de aprendizaje para modificar dinámicamente su base de conocimiento.

## Características

* **Juego Interactivo:** Adivina tu personaje mitológico a través de preguntas de "Sí" o "No".
* **Sistema Experto con Aprendizaje:** La IA mejora su conocimiento cada vez que falla y el usuario le enseña una nueva entrada.
* **Persistencia de Datos:** El árbol de conocimiento se guarda automáticamente, por lo que la IA "recuerda" lo aprendido entre sesiones.
* **Visualización del Árbol:** Genera y visualiza un gráfico del árbol de decisión actual (requiere Graphviz).
* **Interfaz de Usuario Agradable:** Desarrollado con CustomTkinter para un look and feel moderno y adaptable.
* **Multiplataforma:** Empaquetable como ejecutable para Windows, macOS y Linux.

## 🚀 Instalación y Ejecución

### Requisitos Previos

Asegúrate de tener Python 3.x instalado en tu sistema.

### Instalación de Dependencias

1.  Clona este repositorio o descarga el código fuente:
    ```bash
    git clone [https://github.com/TuUsuario/AdivinaQuienMitologia.git](https://github.com/TuUsuario/AdivinaQuienMitologia.git)
    cd AdivinaQuienMitologia
    ```
2.  Instala las librerías necesarias usando pip:
    ```bash
    pip install customtkinter Pillow graphviz
    ```

### Instalación Opcional: Graphviz (para visualización del árbol)

Para poder usar la función "Ver Árbol de Conocimiento", necesitas instalar Graphviz en tu sistema y asegurarte de que el ejecutable `dot` esté en tu PATH:

* **Windows:** Descarga e instala desde [graphviz.org/download](https://graphviz.org/download/). Asegúrate de marcar la opción para añadirlo al PATH durante la instalación.
* **macOS (usando Homebrew):** `brew install graphviz`
* **Linux (Debian/Ubuntu):** `sudo apt-get install graphviz`

### Ejecución del Juego

Una vez instaladas las dependencias y (opcionalmente) Graphviz, puedes ejecutar el script principal:

```bash
python tu_script_principal.py # Asegúrate de usar el nombre correcto de tu archivo Python