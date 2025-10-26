import sys
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
try:
    from PIL import Image
    # from PIL import ImageTk # Ya no es necesario
except ImportError:
    messagebox.showerror("Error de Dependencia", "Se requiere la librería 'Pillow' para mostrar imágenes.\n\nPor favor, instálala usando: pip install pillow")
    exit() # Salir si PIL no está
import graphviz
import os
import pickle
import shutil

# --- MODIFICACIÓN: Definir ruta absoluta para los archivos ---
# Obtener la ruta del directorio donde se encuentra el script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Crear la ruta completa para el archivo del árbol
ARCHIVO_ARBOL = os.path.join(SCRIPT_DIR, "arbol_conocimiento_antiguo.pkl")
# Nombre del archivo de la imagen de fondo
NOMBRE_IMAGEN_FONDO = "fondo_griego.png"
RUTA_IMAGEN_FONDO = os.path.join(SCRIPT_DIR, NOMBRE_IMAGEN_FONDO)
# --- FIN MODIFICACIÓN ---

# --- Clase para representar un Nodo en el árbol de decisión ---
class Nodo:
    """
    Representa un punto en nuestro árbol dedecision.
    Puede ser una pregunta o una respuesta final (un personaje).
    """
    def __init__(self, pregunta=None, personaje=None):
        self.pregunta = pregunta
        self.personaje = personaje
        self.si = None
        self.no = None

    def es_hoja(self):
        return self.personaje is not None

# --- Funciones para guardar y cargar el árbol ---
def guardar_arbol(nodo, nombre_archivo):
    """Guarda el árbol de Nodos en un archivo usando pickle."""
    try:
        with open(nombre_archivo, 'wb') as f:
            pickle.dump(nodo, f)
        print(f"Árbol de conocimiento guardado en '{nombre_archivo}'.")
    except Exception as e:
        messagebox.showerror(title="Error al Guardar", message=f"No se pudo guardar el árbol: {e}")

def cargar_o_inicializar_arbol(nombre_archivo, func_crear_base_inicial):
    """
    Intenta cargar el árbol. Si falla o no existe, crea uno nuevo.
    """
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            messagebox.showwarning(title="Error al Cargar", message=f"Archivo de conocimiento corrupto. Se creará una nueva base.")
    
    nueva_raiz = func_crear_base_inicial()
    guardar_arbol(nueva_raiz, nombre_archivo)
    return nueva_raiz

# --- Clase principal de la Aplicación ---
class AdivinaQuienApp(ctk.CTk):
    def __init__(self, raiz_nodo):
        super().__init__()
        
        # --- CORRECCIÓN CRASH: Flag para evitar bucle de recursión ---
        self._resizing = False
        
        # --- CAMBIO: INICIAR MAXIMIZADO ---
        self.state('zoomed')
        
        # Obtener dimensiones de la pantalla para la imagen de fondo
        self.update_idletasks() # Asegurarse de que la ventana esté renderizada
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # --- CORRECCIÓN CRASH: Inicializar last_width/height ANTES ---
        self.last_width = screen_width
        self.last_height = screen_height
        # --- FIN CORRECCIÓN ---

        # --- Paleta de Colores "Antigua Grecia" ---
        self.COLOR_FONDO_FRAME = "#2B2B2B" # Un gris oscuro, como piedra
        self.COLOR_FONDO_FRAME_VISIBLE = "#3C3C3C" # Un gris un poco más claro para contraste
        self.COLOR_TEXTO_TITULO = "#EAE0C8" # Un blanco "marmol" o papiro
        self.COLOR_ACENTO_PRINCIPAL = "#B8860B" # Dorado/Bronce oscuro
        self.COLOR_ACENTO_HOVER = "#D4AF37" # Dorado/Bronze más claro
        self.COLOR_CORRECTO = "#556B2F" # Verde Oliva
        self.COLOR_CORRECTO_HOVER = "#6B8E23" # Verde Oliva más claro
        self.COLOR_INCORRECTO = "#B22222" # Rojo Terracota/Ladrillo
        self.COLOR_INCORRECTO_HOVER = "#CD5C5C" # Rojo Indio
        self.COLOR_NEUTRAL = "#565B5E" # Gris
        self.COLOR_NEUTRAL_HOVER = "#6E7376"
        # --- Fin Paleta ---

        # --- CORRECCIONES DE VENTANA Y CONTRASTE ---
        self.title("Adivina Quién")
        
        self.minsize(800, 600)   # Se mantiene como tamaño mínimo (ligeramente más alto)
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.COLOR_FONDO_FRAME) # Este será el color si no se carga la imagen
        # --- FIN CORRECCIONES ---

        # --- CARGAR IMAGEN DE FONDO (CORREGIDO) ---
        try:
            self.bg_image_data = Image.open(RUTA_IMAGEN_FONDO) 
            
            self.bg_image = ctk.CTkImage(light_image=self.bg_image_data,
                                         dark_image=self.bg_image_data,
                                         size=(screen_width, screen_height))
            
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.image = self.bg_image   # <- AÑADIDO (para evitar garbage collection)
            # self.bg_label.lower() # <- ¡YA NO ES NECESARIO ENVIAR AL FONDO!

            
        except FileNotFoundError:
            print(f"Advertencia: No se encontró la imagen de fondo en la ruta:\n{RUTA_IMAGEN_FONDO}\nSe usará un color sólido.")
            self.configure(fg_color=self.COLOR_FONDO_FRAME)
            # Si no hay imagen, crear un bg_label falso para que el app no crashee
            self.bg_label = ctk.CTkFrame(self, fg_color=self.COLOR_FONDO_FRAME)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error al cargar imagen de fondo: {e}")
            self.configure(fg_color=self.COLOR_FONDO_FRAME)
            # Si hay error, crear un bg_label falso para que el app no crashee
            self.bg_label = ctk.CTkFrame(self, fg_color=self.COLOR_FONDO_FRAME)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # --- FIN IMAGEN DE FONDO ---

        # --- ASIGNACIÓN DE NODOS (CORRECCIÓN) ---
        self.raiz_nodo = raiz_nodo
        self.nodo_actual = self.raiz_nodo
        # --- FIN CORRECCIÓN ---

        # --- ELIMINADO EL grid_columnconfigure de 'self' ---
        # La ventana principal ('self') ya no usa grid
        # --- FIN ELIMINACIÓN ---

        # --- CAMBIO DE TÍTULO (AHORA CON .place() ) ---
        
        # *** ARREGLO FINAL ***
        # El padre ahora es self.bg_label
        self.frame_titulo = ctk.CTkFrame(self.bg_label, fg_color=self.COLOR_FONDO_FRAME_VISIBLE, corner_radius=15)
        
        self.frame_titulo.place(relx=0.5, rely=0.05, relwidth=0.6, anchor='n') # 5% desde arriba, 60% ancho
        
        self.label_titulo = ctk.CTkLabel(self.frame_titulo, text="Mitología de la Antigua Grecia", font=("Helvetica", 28, "bold"), text_color=self.COLOR_TEXTO_TITULO, fg_color="transparent", wraplength=screen_width * 0.55) # wraplength ajustado
        self.label_titulo.grid(row=0, column=0, padx=30, pady=10, sticky="ew")
        self.frame_titulo.grid_columnconfigure(0, weight=1) # El frame interno SÍ usa grid
        # --- FIN CAMBIO TÍTULO ---
        
        self.current_visible_frame = None # Variable para rastrear el frame activo
        self._crear_widgets()

        self.reiniciar_juego()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # --- CORRECCIÓN: Vincular evento de redimensionar ---
        self.bind("<Configure>", self._on_resize)
        # self.last_width = screen_width  <-- Movido arriba
        # self.last_height = screen_height <-- Movido arriba
        # --- FIN CORRECCIÓN ---
        
    def _crear_widgets(self):
        """Crea y configura todos los frames y widgets de la aplicación."""
        
        # --- CAMBIO: AHORA EN 'self', SIN .grid() ---
        
        # *** ARREGLO FINAL ***
        # El padre ahora es self.bg_label
        self.frame_juego = ctk.CTkFrame(self.bg_label, fg_color=self.COLOR_FONDO_FRAME_VISIBLE, corner_radius=15)
        
        # --- SOLUCIÓN BOTONES CORTADOS: Añadir peso a las filas ---
        self.frame_juego.grid_columnconfigure(0, weight=1) # Columna interna del frame
        self.frame_juego.grid_rowconfigure(0, weight=1)    # Fila 0 (pregunta)
        self.frame_juego.grid_rowconfigure(1, weight=1)    # Fila 1 (botones)
        # --- FIN CAMBIO ---

        self.label_pregunta = ctk.CTkLabel(self.frame_juego, text="", wraplength=self.winfo_screenwidth()*0.55, font=("Helvetica", 22), text_color=self.COLOR_TEXTO_TITULO)
        self.label_pregunta.grid(row=0, column=0, padx=30, pady=30, sticky="ew")

        self.frame_botones_respuesta = ctk.CTkFrame(self.frame_juego, fg_color="transparent")
        self.frame_botones_respuesta.grid(row=1, column=0, padx=20, pady=20, sticky="nsew") # nsew para que se estire
        self.frame_botones_respuesta.grid_columnconfigure((0, 1), weight=1)

        self.boton_si = ctk.CTkButton(self.frame_botones_respuesta, text="Sí", command=lambda: self.procesar_respuesta("si"), height=55, font=("Helvetica", 18), fg_color=self.COLOR_ACENTO_PRINCIPAL, hover_color=self.COLOR_ACENTO_HOVER, corner_radius=10)
        self.boton_no = ctk.CTkButton(self.frame_botones_respuesta, text="No", command=lambda: self.procesar_respuesta("no"), height=55, font=("Helvetica", 18), fg_color=self.COLOR_ACENTO_PRINCIPAL, hover_color=self.COLOR_ACENTO_HOVER, corner_radius=10)
        self.boton_correcto = ctk.CTkButton(self.frame_botones_respuesta, text="¡Sí, es ese!", command=self.respuesta_correcta, height=55, font=("Helvetica", 18), fg_color=self.COLOR_CORRECTO, hover_color=self.COLOR_CORRECTO_HOVER, corner_radius=10)
        self.boton_incorrecto = ctk.CTkButton(self.frame_botones_respuesta, text="No, te equivocaste", command=self.respuesta_incorrecta, height=55, font=("Helvetica", 18), fg_color=self.COLOR_INCORRECTO, hover_color=self.COLOR_INCORRECTO_HOVER, corner_radius=10)
        
        self.frame_controles_finales = ctk.CTkFrame(self.frame_juego, fg_color="transparent")
        self.frame_controles_finales.grid(row=1, column=0, padx=20, pady=20, sticky="nsew") # nsew para que se estire
        self.frame_controles_finales.grid_columnconfigure((0,1), weight=1)
        self.frame_controles_finales.grid_rowconfigure((0,1), weight=1) # <-- SOLUCIÓN BOTONES CORTADOS
        
        # --- CORRECCIÓN: AÑADIDO command=self.reiniciar_juego ---
        self.boton_reinicio = ctk.CTkButton(self.frame_controles_finales, text="Jugar de Nuevo", command=self.reiniciar_juego, height=55, font=("Helvetica", 16), fg_color=self.COLOR_ACENTO_PRINCIPAL, hover_color=self.COLOR_ACENTO_HOVER, corner_radius=10)
        self.boton_reinicio.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.boton_salir = ctk.CTkButton(self.frame_controles_finales, text="Salir del Juego", command=self.on_closing, height=55, font=("Helvetica", 16), fg_color=self.COLOR_NEUTRAL, hover_color=self.COLOR_NEUTRAL_HOVER, corner_radius=10)
        self.boton_salir.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        self.boton_arbol_final = ctk.CTkButton(self.frame_controles_finales, text="Ver Árbol de Conocimiento", command=self.generar_grafico_arbol, height=45, font=("Helvetica", 16), fg_color=self.COLOR_NEUTRAL, hover_color=self.COLOR_NEUTRAL_HOVER, corner_radius=10)
        self.boton_arbol_final.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        # --- CAMBIO: AHORA EN 'self', SIN .grid() ---
        
        # *** ARREGLO FINAL ***
        # El padre ahora es self.bg_label
        self.frame_aprendizaje = ctk.CTkFrame(self.bg_label, fg_color=self.COLOR_FONDO_FRAME_VISIBLE, corner_radius=15)
        
        # --- SOLUCIÓN BOTONES CORTADOS: Añadir peso a las filas ---
        self.frame_aprendizaje.grid_columnconfigure(0, weight=1) # Columna interna
        self.frame_aprendizaje.grid_rowconfigure(1, weight=1) # Fila (label)
        self.frame_aprendizaje.grid_rowconfigure(6, weight=1) # Fila (botones)
        # --- FIN CAMBIO ---
        
        ctk.CTkLabel(self.frame_aprendizaje, text="¡Ayúdame a Aprender!", font=("Helvetica", 22, "bold"), text_color=self.COLOR_TEXTO_TITULO).grid(row=0, column=0, padx=20, pady=(20,10))
        self.label_aprendizaje = ctk.CTkLabel(self.frame_aprendizaje, text="", font=("Helvetica", 18), wraplength=self.winfo_screenwidth()*0.55, text_color=self.COLOR_TEXTO_TITULO)
        self.label_aprendizaje.grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.frame_aprendizaje, text="1. ¿En qué personaje correcto estabas pensando?", font=("Helvetica", 16), text_color=self.COLOR_TEXTO_TITULO).grid(row=2, column=0, pady=(10, 0), padx=40, sticky="w")
        
        self.entry_personaje = ctk.CTkEntry(self.frame_aprendizaje, placeholder_text="Ej: Aquiles", width=350, height=40, font=("Helvetica", 14), corner_radius=10)
        self.entry_personaje.grid(row=3, column=0, pady=(5, 10), padx=40)
        self.label_pregunta_aprender = ctk.CTkLabel(self.frame_aprendizaje, text="2. Crea una pregunta que lo diferencie (respuesta 'Sí' para tu personaje):", font=("Helvetica", 16), wraplength=self.winfo_screenwidth()*0.55, text_color=self.COLOR_TEXTO_TITULO)
        self.label_pregunta_aprender.grid(row=4, column=0, pady=(10, 0), padx=40, sticky="w")
        self.entry_pregunta = ctk.CTkEntry(self.frame_aprendizaje, placeholder_text="Ej: ¿Fue el guerrero más grande de los aqueos?", width=350, height=40, font=("Helvetica", 14), corner_radius=10)
        self.entry_pregunta.grid(row=5, column=0, pady=(5, 10), padx=40)
        
        self.frame_botones_aprender = ctk.CTkFrame(self.frame_aprendizaje, fg_color="transparent")
        self.frame_botones_aprender.grid(row=6, column=0, pady=20, sticky="nsew") # nsew para que se estire
        self.frame_botones_aprender.grid_columnconfigure((0, 1), weight=1)
        self.frame_botones_aprender.grid_rowconfigure((0,1), weight=1) # <-- SOLUCIÓN BOTONES CORTADOS

        self.boton_aprender = ctk.CTkButton(self.frame_botones_aprender, text="Enseñar al sistema", command=self.aprender, height=45, font=("Helvetica", 16), fg_color=self.COLOR_CORRECTO, hover_color=self.COLOR_CORRECTO_HOVER, corner_radius=10)
        self.boton_aprender.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.boton_salir_aprender = ctk.CTkButton(self.frame_botones_aprender, text="Salir del Juego", command=self.on_closing, height=45, font=("Helvetica", 16), fg_color=self.COLOR_NEUTRAL, hover_color=self.COLOR_NEUTRAL_HOVER, corner_radius=10)
        self.boton_salir_aprender.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.boton_arbol_aprender = ctk.CTkButton(self.frame_botones_aprender, text="Ver Árbol de Conocimiento", command=self.generar_grafico_arbol, height=45, font=("Helvetica", 16), fg_color=self.COLOR_NEUTRAL, hover_color=self.COLOR_NEUTRAL_HOVER, corner_radius=10)
        self.boton_arbol_aprender.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro? Se guardará el progreso."):
            guardar_arbol(self.raiz_nodo, ARCHIVO_ARBOL)
            self.destroy()

    def _mostrar_frame(self, frame_a_mostrar):
        """Oculta todos los frames principales y muestra solo el especificado."""
        # --- CAMBIO: AHORA USA .place_forget() ---
        self.frame_juego.place_forget()
        self.frame_aprendizaje.place_forget()
        
        self.current_visible_frame = frame_a_mostrar
        
        # --- CAMBIO: AHORA USA .place() ---
        # relwidth=0.6 -> 60% del ancho de la ventana
        # relx=0.5, rely=0.5, anchor='center' -> Centrado
        frame_a_mostrar.place(relx=0.5, rely=0.5, relwidth=0.6, anchor='center')


    def actualizar_display(self):
        """Muestra la pregunta o la suposición actual en la pantalla."""
        
        self.boton_si.grid_forget()
        self.boton_no.grid_forget()
        self.boton_correcto.grid_forget()
        self.boton_incorrecto.grid_forget()

        if self.nodo_actual.es_hoja():
            self.label_pregunta.configure(text=f"Mi suposición es...\n¿Estás pensando en {self.nodo_actual.personaje}?", font=("Helvetica", 24, "italic"))
            self.boton_correcto.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
            self.boton_incorrecto.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        else:
            self.label_pregunta.configure(text=self.nodo_actual.pregunta, font=("Helvetica", 22))
            self.boton_si.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
            self.boton_no.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
            
    def procesar_respuesta(self, respuesta):
        self.nodo_actual = self.nodo_actual.si if respuesta == "si" else self.nodo_actual.no
        self.actualizar_display()
    
    def respuesta_correcta(self):
        # --- CAMBIO DE TEXTO ---
        self.label_pregunta.configure(text="¡He ganado! Soy un genio de la mitología antigua.", font=("Helvetica", 26, "bold"))
        self.mostrar_controles_finales()

    def respuesta_incorrecta(self):
        self.iniciar_aprendizaje()

    def iniciar_aprendizaje(self):
        self._mostrar_frame(self.frame_aprendizaje)
        self.label_aprendizaje.configure(text=f"Fallé. El personaje que supuse fue '{self.nodo_actual.personaje}'.")
        self.entry_personaje.delete(0, ctk.END)
        self.entry_pregunta.delete(0, ctk.END)
        self.entry_personaje.focus()

    def aprender(self):
        personaje_real = self.entry_personaje.get().strip()
        pregunta_nueva_texto = self.entry_pregunta.get().strip()

        if not personaje_real or not pregunta_nueva_texto:
            messagebox.showwarning(title="Error", message="Por favor, rellena ambos campos para aprender.")
            return

        personaje_antiguo = self.nodo_actual.personaje
        self.nodo_actual.pregunta = pregunta_nueva_texto
        self.nodo_actual.personaje = None 
        self.nodo_actual.si = Nodo(personaje=personaje_real)
        self.nodo_actual.no = Nodo(personaje=personaje_antiguo)
        
        self._mostrar_frame(self.frame_juego)
        self.label_pregunta.configure(text=f"¡Gracias! He aprendido a reconocer a {personaje_real}.", font=("Helvetica", 22))
        
        guardar_arbol(self.raiz_nodo, ARCHIVO_ARBOL)
        self.mostrar_controles_finales()

    def reiniciar_juego(self):
        self.nodo_actual = self.raiz_nodo
        self._mostrar_frame(self.frame_juego)
        self.frame_controles_finales.grid_forget()
        self.frame_botones_respuesta.grid(row=1, column=0, padx=20, pady=20, sticky="nsew") # nsew
        self.actualizar_display()

    def mostrar_controles_finales(self):
        self.frame_botones_respuesta.grid_forget()
        self.frame_controles_finales.grid(row=1, column=0, padx=20, pady=20, sticky="nsew") # nsew
        
    # --- MÉTODO AÑADIDO PARA MANEJAR REDIMENSIÓN ---
    def _on_resize(self, event):
        """Maneja el evento de redimensionar la ventana para reescalar el fondo y reposicionar los widgets."""
        
        # Ignorar eventos de redimensión si vienen del bg_label
        if event.widget != self:
             return

        if self._resizing:
            return
        self._resizing = True
        
        width = self.winfo_width()
        height = self.winfo_height()
        
        if hasattr(self, 'bg_image_data') and (width != self.last_width or height != self.last_height):
            
            if width < 100 or height < 100:
                 self._resizing = False
                 return 

            self.last_width = width
            self.last_height = height
            
            # Reconfigurar el tamaño de la CTkImage
            if hasattr(self, 'bg_image'):
                self.bg_image.configure(size=(width, height))
            
            # --- CORRECCIÓN TEXTO CORTADO ---
            # Re-configurar el wraplength de todas las etiquetas de texto
            new_wrap = width * 0.55 # 55% del ancho de la ventana
            if hasattr(self, 'label_titulo'):
                self.label_titulo.configure(wraplength=new_wrap)
            if hasattr(self, 'label_pregunta'):
                self.label_pregunta.configure(wraplength=new_wrap)
            if hasattr(self, 'label_aprendizaje'):
                self.label_aprendizaje.configure(wraplength=new_wrap)
            if hasattr(self, 'label_pregunta_aprender'):
                self.label_pregunta_aprender.configure(wraplength=new_wrap)
            # --- FIN CORRECCIÓN ---
        
        self._resizing = False
    # --- FIN MÉTODO AÑADIDO ---

    def generar_grafico_arbol(self):
        if shutil.which('dot') is None:
            messagebox.showerror(title="Error: Graphviz no encontrado", message="No se encontró la instalación de Graphviz en el sistema.\n\nPor favor, instálalo desde graphviz.org y asegúrate de que esté en el PATH del sistema.")
            return

        dot = graphviz.Digraph('ArbolAdivinaQuien', node_attr={'shape': 'box', 'style': 'filled', 'fontname': 'Helvetica'})
        
        dot.attr(rankdir='TB', size='12,12', bgcolor=self.COLOR_FONDO_FRAME, fontcolor=self.COLOR_TEXTO_TITULO, dpi='600')
        dot.edge_attr.update(fontname='Helvetica', fontcolor=self.COLOR_TEXTO_TITULO, color=self.COLOR_TEXTO_TITULO)

        def add_nodes_edges(node):
            node_id = str(id(node))
            if node.es_hoja():
                dot.node(node_id, node.personaje, shape='ellipse', color=self.COLOR_CORRECTO, fontcolor=self.COLOR_TEXTO_TITULO)
            else:
                dot.node(node_id, node.pregunta, shape='diamond', color=self.COLOR_ACENTO_PRINCIPAL, fontcolor=self.COLOR_FONDO_FRAME_VISIBLE)
            
            if node.si:
                dot.edge(node_id, str(id(node.si)), label="Sí")
                add_nodes_edges(node.si)
            if node.no:
                dot.edge(node_id, str(id(node.no)), label="No")
                add_nodes_edges(node.no)

        add_nodes_edges(self.raiz_nodo)

        try:
            filename = os.path.join(SCRIPT_DIR, 'arbol_conocimiento')
            dot.render(filename, format='png', view=True, cleanup=True) 
        except Exception as e:
            messagebox.showerror(title="Error al Graficar", message=f"Hubo un error al generar el gráfico: {e}")

    def mostrar_acerca_de(self):
        messagebox.showinfo(
            "Acerca de Adivina Quién",
            "Adivina Quién: Mitología de la Antigua Grecia\n\n"
            "Versión: 3.0 (Estilo Clásico)\n"
            "Una aplicación que adivina personajes y aprende de ti."
        )

# --- Función para CONSTRUIR la base de conocimiento inicial ---
def crear_base_conocimiento_inicial():
    """Crea y devuelve la estructura inicial del árbol de conocimiento."""
    # (El contenido de esta función no ha cambiado)
    raiz = Nodo(pregunta="¿Tu personaje es un dios/diosa del Olimpo?")
    dioses_rama = Nodo(pregunta="¿Tu personaje es hombre?")
    raiz.si = dioses_rama
    diosas_mujeres_rama = Nodo(pregunta="¿Se le representa a menudo con armas (arco, lanza, escudo)?")
    dioses_rama.no = diosas_mujeres_rama
    dioses_hombres_rama = Nodo(pregunta="¿Se le representa con barba?")
    dioses_rama.si = dioses_hombres_rama
    dh_con_barba_rama = Nodo(pregunta="¿Es el rey de los dioses y su símbolo es un rayo?")
    dioses_hombres_rama.si = dh_con_barba_rama
    dh_con_barba_rama.si = Nodo(personaje="Zeus")
    dh_no_zeus = Nodo(pregunta="¿Gobierna el mar y lleva un tridente?")
    dh_con_barba_rama.no = dh_no_zeus
    dh_no_zeus.si = Nodo(personaje="Poseidón")
    dh_no_poseidon = Nodo(pregunta="¿Gobierna el inframundo?")
    dh_no_zeus.no = dh_no_poseidon
    dh_no_poseidon.si = Nodo(personaje="Hades")
    dh_no_poseidon.no = Nodo(personaje="Hefesto")
    dh_sin_barba_rama = Nodo(pregunta="¿Su arma principal es un arco y flechas Y está asociado a la música?")
    dioses_hombres_rama.no = dh_sin_barba_rama
    dh_sin_barba_rama.si = Nodo(personaje="Apolo")
    dh_no_apolo = Nodo(pregunta="¿Es el mensajero de los dioses, con sandalias o casco alado?")
    dh_sin_barba_rama.no = dh_no_apolo
    dh_no_apolo.si = Nodo(personaje="Hermes")
    dh_no_hermes = Nodo(pregunta="¿Es el dios de la guerra, representado con armadura y casco?")
    dh_no_apolo.no = dh_no_hermes
    dh_no_hermes.si = Nodo(personaje="Ares")
    dh_no_hermes.no = Nodo(personaje="Dionisio")
    dm_con_armas_rama = Nodo(pregunta="¿Su arma principal es un arco y flechas y está asociada a la luna y la caza?")
    diosas_mujeres_rama.si = dm_con_armas_rama
    dm_con_armas_rama.si = Nodo(personaje="Artemisa")
    dm_con_armas_rama.no = Nodo(personaje="Atenea")
    dm_sin_armas_rama = Nodo(pregunta="¿Es una reina?")
    # --- CORRECCIÓN DE TYPO (NameError) ---
    diosas_mujeres_rama.no = dm_sin_armas_rama
    # --- FIN CORRECCIÓN ---
    dm_es_reina = Nodo(pregunta="¿Es la reina del Olimpo, esposa de Zeus y diosa del matrimonio?")
    dm_sin_armas_rama.si = dm_es_reina
    dm_es_reina.si = Nodo(personaje="Hera")
    dm_es_reina.no = Nodo(personaje="Perséfone")
    dm_no_reina = Nodo(pregunta="¿Es la diosa del amor y la belleza?")
    dm_sin_armas_rama.no = dm_no_reina
    dm_no_reina.si = Nodo(personaje="Afrodita")
    dm_no_afrodita = Nodo(pregunta="¿Es la diosa de la agricultura y las cosechas?")
    dm_no_reina.no = dm_no_afrodita
    dm_no_afrodita.si = Nodo(personaje="Deméter")
    dm_no_afrodita.no = Nodo(personaje="Hestia")
    no_dioses_rama = Nodo(pregunta="¿Tu personaje es un héroe/heroína (un humano con habilidades extraordinarias)?")
    raiz.no = no_dioses_rama
    heroes_rama = Nodo(pregunta="¿Tu personaje es hombre?")
    no_dioses_rama.si = heroes_rama
    heroes_hombres_rama = Nodo(pregunta="¿Es conocido por su fuerza sobrehumana y haber completado 12 trabajos?")
    heroes_rama.si = heroes_hombres_rama
    heroes_hombres_rama.si = Nodo(personaje="Heracles")
    heroes_hombres_rama.no = Nodo(personaje="Teseo")
    heroes_rama.no = Nodo(personaje="Atalanta")
    monstruos_genero_rama = Nodo(pregunta="¿Tu personaje monstruo es de naturaleza masculina?")
    no_dioses_rama.no = monstruos_genero_rama
    monstruos_masculinos_rama = Nodo(pregunta="¿Tiene múltiples cabezas o cuerpos?")
    monstruos_genero_rama.si = monstruos_masculinos_rama
    monstruos_masculinos_rama.si = Nodo(personaje="Hidra de Lerna")
    mm_no_multiples = Nodo(pregunta="¿Es un toro con cabeza de hombre que vive en un laberinto?")
    monstruos_masculinos_rama.no = mm_no_multiples
    mm_no_multiples.si = Nodo(personaje="Minotauro")
    mm_no_multiples.no = Nodo(personaje="Cerbero")
    monstruos_femeninos_rama = Nodo(pregunta="¿Su mirada puede convertir a las personas en piedra?")
    monstruos_genero_rama.no = monstruos_femeninos_rama
    monstruos_femeninos_rama.si = Nodo(personaje="Medusa")
    monstruos_femeninos_rama.no = Nodo(personaje="Arpía")
    return raiz

# --- Bloque principal para inicializar la aplicación ---
if __name__ == "__main__":
    # --- MODIFICACIÓN: Usa la ruta absoluta definida al inicio ---
    arbol_actual = cargar_o_inicializar_arbol(ARCHIVO_ARBOL, crear_base_conocimiento_inicial)
    app = AdivinaQuienApp(raiz_nodo=arbol_actual)
    app.mainloop()