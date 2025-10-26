# Adivina Quién: Mitología de la Antigua Grecia

## Breve Descripción / Eslogan

**Piensa en un dios, héroe o monstruo. ¡Rétame a adivinarlo!**
Un sistema experto que juega "Adivina Quién" y aprende de tus respuestas.

---

## Descripción Extendida del Proyecto

"Adivina Quién: Mitología de la Antigua Grecia" es un juego interactivo que desafía a una Inteligencia Artificial a adivinar personajes (dioses, héroes, monstruos) de la mitología griega en los que el usuario está pensando. Lo más notable de este proyecto es su capacidad de **aprendizaje**: si la IA falla, el usuario puede enseñarle nuevos personajes y preguntas distintivas, expandiendo así la base de conocimiento del sistema de forma persistente.

Este proyecto sirve como una implementación práctica y funcional de un **sistema experto** básico, utilizando un árbol de decisión para el motor de inferencia y la capacidad de aprendizaje para modificar dinámicamente su base de conocimiento.

## Características

* **Juego Interactivo:** Adivina tu personaje mitológico a través de preguntas de "Sí" o "No".
* **Sistema Experto con Aprendizaje:** La IA mejora su conocimiento cada vez que falla y el usuario le enseña una nueva entrada, haciendo que el juego sea cada vez más "inteligente".
* **Persistencia de Datos:** El árbol de conocimiento se guarda automáticamente en un archivo `.pkl`, por lo que la IA "recuerda" lo aprendido entre sesiones.
* **Visualización del Árbol de Conocimiento:** Genera y visualiza un gráfico del árbol de decisión actual, permitiendo entender la lógica interna del sistema (requiere Graphviz instalado).
* **Interfaz de Usuario Agradable:** Desarrollado con CustomTkinter para un look and feel moderno, intuitivo y adaptable al tamaño de la ventana.
* **Multiplataforma:** Empaquetable como ejecutable para sistemas operativos como Windows, macOS y Linux.

## 🚀 Instalación y Ejecución

### Requisitos Previos

Asegúrate de tener **Python 3.x** instalado en tu sistema.

### Instalación de Dependencias

1.  **Clona este repositorio** o descarga el código fuente:
    ```bash
    git clone [https://github.com/Joriksal/Adivina_Quien-Mitologia_de_la_Antigua_Grecia]
    cd AdivinaQuienMitologia
    ```

2.  **Instala las librerías necesarias** usando pip:
    ```bash
    pip install customtkinter Pillow graphviz
    ```

### Instalación Opcional: Graphviz (para visualización del árbol)

Para poder usar la función "Ver Árbol de Conocimiento" dentro del juego, necesitas instalar Graphviz en tu sistema y asegurarte de que el ejecutable `dot` esté en tu PATH.

* **Windows:**
    1.  Descarga e instala desde [graphviz.org/download](https://graphviz.org/download/).
    2.  **¡Importante!** Durante la instalación, asegúrate de marcar la opción para añadirlo al PATH del sistema.
* **macOS (usando Homebrew):**
    ```bash
    brew install graphviz
    ```
* **Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get install graphviz
    ```

### Ejecución del Juego

Una vez que todas las dependencias estén instaladas y (opcionalmente) Graphviz, puedes ejecutar el script principal:

```bash
python adivina_quien-mitologia_de_la_antigua_grecia.py 
```

## Cómo Jugar

1.  **Piensa en un personaje:** Elige cualquier dios, diosa, héroe, heroína o criatura de la mitología griega en tu mente.
2.  **Responde las preguntas:** La IA te hará preguntas de "Sí" o "No". Responde honestamente según el personaje que elegiste.
3.  **Adivinanza de la IA:** Cuando la IA crea saber la respuesta, te hará una suposición final.
    * Si acierta, ¡felicidades! La IA ha ganado. Puedes elegir "Jugar de Nuevo" o "Salir".
    * Si falla, se activará el **modo de aprendizaje**.
4.  **Enseñar a la IA (Modo de Aprendizaje):**
    * Introduce el nombre del personaje real en el que estabas pensando.
    * Crea una **pregunta nueva** que sea **VERDADERA (Sí)** para tu personaje y **FALSA (No)** para el personaje que la IA supuso incorrectamente. Esto le permite a la IA aprender a diferenciarlos en futuras partidas.

## Fundamentos Teóricos (Sistema Experto)

Este juego es una implementación práctica de un sistema experto básico, utilizando los siguientes conceptos:

* **Base de Conocimiento:** El conocimiento sobre los personajes y sus atributos se almacena en una estructura de **árbol de decisión** compuesta por objetos `Nodo`. Cada nodo representa una pregunta o una conclusión (un personaje).
* **Motor de Inferencia:** La lógica del juego opera bajo un principio de **encadenamiento hacia adelante (forward chaining)**. A partir de los "hechos" (las respuestas "Sí" o "No" del usuario), el sistema navega progresivamente por el árbol, aplicando "reglas" implícitas en cada bifurcación para deducir el personaje correcto.
* **Reglas y Casos:** Cada pregunta y la dirección resultante ("Sí" o "No") actúan como una regla de producción. Un "caso" es el personaje específico que el usuario ha elegido. El sistema busca una secuencia de reglas que satisfagan los hechos del caso para llegar a una conclusión.
* **Aprendizaje Dinámico:** Cuando la IA no logra adivinar, el módulo de aprendizaje entra en acción. El usuario introduce nueva información (el personaje correcto y una pregunta diferenciadora), lo que permite al sistema modificar su base de conocimiento, dividiendo un nodo incorrecto y creando nuevas reglas para mejorar su rendimiento futuro.
