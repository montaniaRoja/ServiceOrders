import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from ordenes_servicio import OrdenesDeServicio


class FormularioOrdenes(tk.Toplevel):
    def __init__(self, master, ordenes_servicio, actualizar_treeview_callback, orden_id=None):
        super().__init__(master)
        self.ordenes_servicio = ordenes_servicio
        self.actualizar_treeview_callback = actualizar_treeview_callback
        self.orden_id = orden_id
        self.title("Formulario de Órdenes de Servicio")
        self.geometry("400x500")
        self.create_widgets()

        if orden_id:
            self.cargar_datos_orden()

    def create_widgets(self):
        # Crear etiquetas y campos de entrada
        self.labels = [
            "Fecha de la orden", "Cliente", "Equipo", "Problema", "Trabajo a realizar",
            "Técnico asignado", "Estado de la orden", "Fecha estimada de fin", "Costo", "Notas adicionales"
        ]
        self.entries = {}

        for i, label_text in enumerate(self.labels):
            label = tk.Label(self, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)
            if label_text in ["Fecha de la orden", "Fecha estimada de fin"]:
                entry = DateEntry(self, date_pattern='yyyy-mm-dd')
            else:
                entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        # Botón para agregar orden
        self.add_button = tk.Button(self, text="Agregar", command=self.agregar_orden)
        self.add_button.grid(row=len(self.labels), columnspan=2, pady=10)

        # Botón para finalizar orden
        self.finalize_button = tk.Button(self, text="Finalizar", command=self.finalizar_orden)
        self.finalize_button.grid(row=len(self.labels) + 1, columnspan=2, pady=10)

    def cargar_datos_orden(self):
        orden = self.ordenes_servicio.obtener_orden_por_id(self.orden_id)
        if orden:
            for i, label_text in enumerate(self.labels):
                self.entries[label_text].delete(0, tk.END)
                self.entries[label_text].insert(0, orden[i + 1])
                if label_text == "Estado de la orden":
                    self.entries[label_text].config(state='readonly')
                    if orden[i + 1] == "Finalizada":
                        self.finalize_button.config(state=tk.DISABLED)

    def agregar_orden(self):
        # Obtener valores de los campos de entrada
        valores = {label: entry.get() for label, entry in self.entries.items()}
        valores["Costo"] = float(valores["Costo"]) if valores["Costo"] else 0.0
        # Insertar en la base de datos
        try:
            self.ordenes_servicio.agregar_orden(
                valores["Fecha de la orden"],
                valores["Cliente"],
                valores["Equipo"],
                valores["Problema"],
                valores["Trabajo a realizar"],
                valores["Técnico asignado"],
                valores["Estado de la orden"],
                valores["Fecha estimada de fin"],
                valores["Costo"],
                valores["Notas adicionales"]
            )
            messagebox.showinfo("Éxito", "Orden de servicio agregada correctamente")
            self.actualizar_treeview_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la orden: {e}")

    def finalizar_orden(self):
        if self.orden_id:
            try:
                self.ordenes_servicio.actualizar_estado(self.orden_id, "Finalizada")
                messagebox.showinfo("Éxito", "Estado de la orden actualizado a 'Finalizada'")
                self.actualizar_treeview_callback()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el estado de la orden: {e}")
