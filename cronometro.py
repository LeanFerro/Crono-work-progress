import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime, timedelta
import csv
import os


class CronometroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronómetro de Trabajo")

        self.start_time = None
        self.running = False
        self.paused = False
        self.paused_time = 0
        self.elapsed_time = 0
        self.total_time = timedelta(0)
        self.current_file = "Sin archivo"

        # Frame para los botones "Abrir" y "Guardar"
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        # Botón para guardar la tabla (al lado de abrir)
        self.save_button = tk.Button(self.top_frame, text="Guardar Tabla",
                                     command=self.guardar_tabla, font=("Helvetica", 12), padx=10, pady=5)
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Botón para abrir una tabla guardada (al lado de guardar)
        self.open_button = tk.Button(self.top_frame, text="Abrir Tabla",
                                     command=self.abrir_tabla, font=("Helvetica", 12), padx=10, pady=5)
        self.open_button.pack(side=tk.LEFT, padx=10)

        # Etiqueta que muestra el archivo actual
        self.file_label = tk.Label(
            root, text=f"Archivo actual: {self.current_file}", font=("Helvetica", 14))
        self.file_label.pack(pady=10)

        # Label para mostrar el cronómetro
        self.time_label = tk.Label(root, text="00:00:00", font=(
            "Helvetica", 48), bg="black", fg="white", padx=20)
        self.time_label.pack(pady=20)

        # Frame para los botones de control
        self.control_frame_top = tk.Frame(root)
        self.control_frame_top.pack()

        self.control_frame_bottom = tk.Frame(root)
        self.control_frame_bottom.pack()

        # Botones de Iniciar y Pausar
        self.start_button = tk.Button(self.control_frame_top, text="Iniciar", command=self.iniciar_cronometro, font=(
            "Helvetica", 12), bg="green", fg="white", padx=10, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.pause_button = tk.Button(self.control_frame_top, text="Pausar", command=self.pausar_cronometro, font=(
            "Helvetica", 12), bg="orange", fg="white", padx=10, pady=5)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Botones de Finalizar y Reiniciar (debajo de los de Iniciar y Pausar)
        self.stop_button = tk.Button(self.control_frame_bottom, text="Finalizar", command=self.finalizar_cronometro, font=(
            "Helvetica", 12), bg="red", fg="white", padx=10, pady=5)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.control_frame_bottom, text="Reiniciar", command=self.reiniciar_cronometro, font=(
            "Helvetica", 12), bg="blue", fg="white", padx=10, pady=5)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Tabla para registrar el tiempo trabajado con margen a la derecha
        self.tree_frame = tk.Frame(root, padx=20)  # Frame con margen derecho
        self.tree_frame.pack(pady=20)

        self.tree = ttk.Treeview(self.tree_frame, columns=(
            "Fecha", "Hora Inicio", "Hora Fin", "Tiempo Trabajado"), show="headings")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora Inicio", text="Hora Inicio")
        self.tree.heading("Hora Fin", text="Hora Fin")
        self.tree.heading("Tiempo Trabajado", text="Tiempo Trabajado")
        self.tree.pack()

        # Label para el tiempo total trabajado
        self.total_label = tk.Label(
            root, text="Tiempo Total Trabajado: 00:00:00", font=("Helvetica", 16))
        self.total_label.pack(pady=10)

        # Botón para borrar toda la tabla, ahora con padx=20 y color rojo
        self.clear_button = tk.Button(root, text="Borrar Tabla", command=self.borrar_tabla, font=(
            "Helvetica", 12), bg="red", fg="white", padx=10, pady=5)
        self.clear_button.pack(pady=20, side=tk.RIGHT, anchor="e", padx=10)

        # Actualiza el cronómetro
        self.actualizar_cronometro()

    def iniciar_cronometro(self):
        if not self.running:
            self.start_time = datetime.now() - timedelta(seconds=self.paused_time)
            self.running = True
            self.paused = False
            self.time_label.config(fg="lightgreen")

    def pausar_cronometro(self):
        if self.running:
            self.paused_time = (
                datetime.now() - self.start_time).total_seconds()
            self.running = False
            self.paused = True
            self.time_label.config(fg="orange")

    def finalizar_cronometro(self):
        if self.running or self.paused:
            self.running = False
            tiempo_trabajado = self.elapsed_time + \
                (datetime.now(
                ) - self.start_time).total_seconds() if not self.paused else self.paused_time
            fecha_actual = self.start_time.strftime("%Y-%m-%d")
            hora_inicio = self.start_time.strftime("%H:%M:%S")
            hora_fin = datetime.now().strftime("%H:%M:%S")
            tiempo_trabajado_str = self.formato_tiempo(tiempo_trabajado)

            # Insertar en la tabla
            self.tree.insert("", "end", values=(
                fecha_actual, hora_inicio, hora_fin, tiempo_trabajado_str))

            # Acumular el tiempo total trabajado
            self.total_time += timedelta(seconds=tiempo_trabajado)
            self.actualizar_tiempo_total()

            # Reiniciar cronómetro a 0
            self.reiniciar_cronometro()

    def reiniciar_cronometro(self):
        self.elapsed_time = 0
        self.paused_time = 0
        self.time_label.config(text="00:00:00", fg="white")
        self.running = False
        self.paused = False

    def borrar_tabla(self):
        # Limpiar todos los registros de la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Reiniciar el tiempo total trabajado
        self.total_time = timedelta(0)
        self.actualizar_tiempo_total()

    def actualizar_cronometro(self):
        if self.running:
            tiempo_transcurrido = (
                datetime.now() - self.start_time).total_seconds()
            self.elapsed_time = tiempo_transcurrido
            self.time_label.config(
                text=self.formato_tiempo(tiempo_transcurrido))
        self.root.after(1000, self.actualizar_cronometro)

    def formato_tiempo(self, segundos):
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos = int(segundos % 60)
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    def actualizar_tiempo_total(self):
        total_segundos = self.total_time.total_seconds()
        self.total_label.config(
            text=f"Tiempo Total Trabajado: {self.formato_tiempo(total_segundos)}")

    def guardar_tabla(self):
        # Pedir al usuario un archivo para guardar
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            with open(archivo, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Fecha", "Hora Inicio", "Hora Fin", "Tiempo Trabajado"])
                for row in self.tree.get_children():
                    writer.writerow(self.tree.item(row)["values"])
            # Actualizar el nombre del archivo sin la extensión
            self.current_file = os.path.basename(archivo).rsplit('.', 1)[0]
            self.file_label.config(text=f"Archivo actual: {self.current_file}")

    def abrir_tabla(self):
        # Pedir al usuario un archivo para abrir
        archivo = filedialog.askopenfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            # Limpiar la tabla antes de cargar los nuevos datos
            self.borrar_tabla()
            with open(archivo, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Omitir la cabecera
                for row in reader:
                    self.tree.insert("", "end", values=row)
            # Actualizar el nombre del archivo sin la extensión
            self.current_file = os.path.basename(archivo).rsplit('.', 1)[0]
            self.file_label.config(text=f"Archivo actual: {self.current_file}")

            # Calcular el nuevo tiempo total desde los datos cargados
            self.calcular_tiempo_total_desde_tabla()

    def calcular_tiempo_total_desde_tabla(self):
        total_segundos = 0
        for row in self.tree.get_children():
            tiempo_trabajado = self.tree.item(
                row)["values"][3]  # Columna "Tiempo Trabajado"
            h, m, s = map(int, tiempo_trabajado.split(':'))
            total_segundos += h * 3600 + m * 60 + s
        self.total_time = timedelta(seconds=total_segundos)
        self.actualizar_tiempo_total()


if __name__ == "__main__":
    root = tk.Tk()
    app = CronometroApp(root)
    root.mainloop()
