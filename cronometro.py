import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
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

        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.save_button = tk.Button(self.top_frame, text="Guardar Tabla",
                                     command=self.guardar_tabla, font=("Helvetica", 12), padx=10, pady=5)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.open_button = tk.Button(self.top_frame, text="Abrir Tabla",
                                     command=self.abrir_tabla, font=("Helvetica", 12), padx=10, pady=5)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.file_label = tk.Label(
            root, text=f"Archivo actual: {self.current_file}", font=("Helvetica", 14))
        self.file_label.pack(pady=10)

        self.time_label = tk.Label(root, text="00:00:00", font=(
            "Helvetica", 48), bg="black", fg="white", padx=20)
        self.time_label.pack(pady=20)

        self.control_frame_top = tk.Frame(root)
        self.control_frame_top.pack()

        self.control_frame_bottom = tk.Frame(root)
        self.control_frame_bottom.pack()

        self.start_button = tk.Button(self.control_frame_top, text="Iniciar", command=self.iniciar_cronometro, font=(
            "Helvetica", 12), bg="green", fg="white", padx=10, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.pause_button = tk.Button(self.control_frame_top, text="Pausar", command=self.pausar_cronometro, font=(
            "Helvetica", 12), bg="orange", fg="white", padx=10, pady=5)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_button = tk.Button(self.control_frame_bottom, text="Finalizar", command=self.finalizar_cronometro, font=(
            "Helvetica", 12), bg="red", fg="white", padx=10, pady=5)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.control_frame_bottom, text="Reiniciar", command=self.reiniciar_cronometro, font=(
            "Helvetica", 12), bg="blue", fg="white", padx=10, pady=5)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.tree_frame = tk.Frame(root, padx=20)
        self.tree_frame.pack(pady=20)

        self.tree = ttk.Treeview(self.tree_frame, columns=(
            "Fecha", "Hora Inicio", "Hora Fin", "Tiempo Trabajado", "Comentarios"), show="headings")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora Inicio", text="Hora Inicio")
        self.tree.heading("Hora Fin", text="Hora Fin")
        self.tree.heading("Tiempo Trabajado", text="Tiempo Trabajado")
        self.tree.heading("Comentarios", text="Comentarios")
        self.tree.pack()

        self.tree.bind("<Double-1>", self.agregar_comentario)
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)

        self.menu_contextual = tk.Menu(self.tree, tearoff=0)
        self.menu_contextual.add_command(
            label="Borrar Fila", command=self.borrar_fila)

        self.total_label = tk.Label(
            root, text="Tiempo Total Trabajado: 00:00:00", font=("Helvetica", 16))
        self.total_label.pack(pady=10)

        self.clear_button = tk.Button(root, text="Borrar Tabla", command=self.borrar_tabla, font=(
            "Helvetica", 12), bg="red", fg="white", padx=10, pady=5)
        self.clear_button.pack(pady=20, side=tk.RIGHT, anchor="e", padx=10)

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
            tiempo_trabajado = (
                datetime.now() - self.start_time).total_seconds()  # Cambiado aquí
            fecha_actual = self.start_time.strftime("%Y-%m-%d")
            hora_inicio = self.start_time.strftime("%H:%M:%S")
            hora_fin = datetime.now().strftime("%H:%M:%S")
            tiempo_trabajado_str = self.formato_tiempo(tiempo_trabajado)

            self.tree.insert("", "end", values=(
                fecha_actual, hora_inicio, hora_fin, tiempo_trabajado_str, ""))
            self.total_time += timedelta(seconds=tiempo_trabajado)
            self.actualizar_tiempo_total()

            self.reiniciar_cronometro()

    def reiniciar_cronometro(self):
        self.elapsed_time = 0
        self.paused_time = 0
        self.time_label.config(text="00:00:00", fg="white")
        self.running = False
        self.paused = False

    def borrar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

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
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            with open(archivo, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Fecha", "Hora Inicio", "Hora Fin", "Tiempo Trabajado"])
                for row in self.tree.get_children():
                    writer.writerow(self.tree.item(row)["values"])
            self.current_file = os.path.basename(archivo).rsplit('.', 1)[0]
            self.file_label.config(text=f"Archivo actual: {self.current_file}")

    def agregar_comentario(self, event):
        selected_item = self.tree.selection()[0]
        comentario_actual = self.tree.item(selected_item, "values")[4]
        nuevo_comentario = simpledialog.askstring(
            "Agregar Comentario", "Ingrese un comentario:", initialvalue=comentario_actual)

        if nuevo_comentario is not None:
            valores = list(self.tree.item(selected_item, "values"))
            valores[4] = nuevo_comentario

            self.tree.item(selected_item, values=valores)

    def abrir_tabla(self):
        archivo = filedialog.askopenfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            self.borrar_tabla()
            with open(archivo, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Omitir la cabecera
                for row in reader:
                    self.tree.insert("", "end", values=row)
            self.current_file = os.path.basename(archivo).rsplit('.', 1)[0]
            self.file_label.config(text=f"Archivo actual: {self.current_file}")
            self.calcular_tiempo_total_desde_tabla()

    def mostrar_menu_contextual(self, event):
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            self.tree.selection_set(selected_item)
            self.menu_contextual.post(event.x_root, event.y_root)

    def borrar_fila(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def calcular_tiempo_total_desde_tabla(self):
        total_segundos = 0
        for row in self.tree.get_children():
            tiempo_trabajado = self.tree.item(
                row)["values"][3]
            h, m, s = map(int, tiempo_trabajado.split(':'))
            total_segundos += h * 3600 + m * 60 + s
        self.total_time = timedelta(seconds=total_segundos)
        self.actualizar_tiempo_total()


if __name__ == "__main__":
    root = tk.Tk()
    app = CronometroApp(root)
    root.mainloop()
