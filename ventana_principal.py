import tkinter as tk
from tkinter import messagebox, ttk
from ordenes_servicio import OrdenesDeServicio
from formulario_ordenes import FormularioOrdenes


class VentanaPrincipal(tk.Tk):
    def __init__(self, ordenes_servicio):
        super().__init__()
        self.ordenes_servicio = ordenes_servicio
        self.title("Gestión de Órdenes de Servicio")
        self.geometry("800x400")

        self.create_widgets()
        self.cargar_ordenes()

    def create_widgets(self):
        self.treeview = ttk.Treeview(self, columns=(
        "ID", "Fecha de la orden", "Cliente", "Equipo", "Problema", "Trabajo", "Técnico", "Estado",
        "Fecha estimada de fin", "Costo", "Notas"), show='headings')
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Fecha de la orden", text="Fecha de la orden")
        self.treeview.heading("Cliente", text="Cliente")
        self.treeview.heading("Equipo", text="Equipo")
        self.treeview.heading("Problema", text="Problema")
        self.treeview.heading("Trabajo", text="Trabajo a realizar")
        self.treeview.heading("Técnico", text="Técnico asignado")
        self.treeview.heading("Estado", text="Estado de la orden")
        self.treeview.heading("Fecha estimada de fin", text="Fecha estimada de fin")
        self.treeview.heading("Costo", text="Costo")
        self.treeview.heading("Notas", text="Notas adicionales")

        self.treeview.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self, text="Agregar Nueva Orden", command=self.mostrar_formulario)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.finalize_button = tk.Button(self, text="Finalizar Orden", command=self.mostrar_formulario_finalizar)
        self.finalize_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def cargar_ordenes(self):
        for row in self.ordenes_servicio.obtener_ordenes():
            self.treeview.insert("", tk.END, values=row)

    def mostrar_formulario(self):
        FormularioOrdenes(self, self.ordenes_servicio, self.actualizar_treeview)

    def mostrar_formulario_finalizar(self):
        selected_item = self.treeview.selection()
        if selected_item:
            item = self.treeview.item(selected_item)
            orden_id = item['values'][0]
            FormularioOrdenes(self, self.ordenes_servicio, self.actualizar_treeview, orden_id)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una orden para finalizar")

    def actualizar_treeview(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        self.cargar_ordenes()


if __name__ == "__main__":
    db = OrdenesDeServicio()
    app = VentanaPrincipal(db)
    app.mainloop()
