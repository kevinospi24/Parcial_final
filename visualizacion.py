import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from logica import registro as r
from logica import ReporteGeneral as rg
from logica import ReporteIndividual as ri


ventana = tk.Tk()  
ventana.title("Sistema de Registro de Producción")  
ventana.geometry("400x300")  


columnas = [
    "operario",
    "pan_frances",
    "pan_queso",
    "croissants",
    "complejidad_frances",
    "complejidad_queso",
    "complejidad_croissant",
    "eficiencia",
    "estado"
]


df = pd.DataFrame(columns=columnas)
registro_obj = r()  

def registrar_produccion():
    global df
    nuevo_df = registro_obj.registrar()
    if nuevo_df is not None:

        filas = []
        for nombre, datos in registro_obj.datos.items():
            fila = {
                "operario": nombre,
                "pan_frances": datos["Cantidades"]["Frances"],
                "pan_queso": datos["Cantidades"]["Queso"],
                "croissants": datos["Cantidades"]["Croissant"],
                "complejidad_frances": datos["Complejidades"]["Francés"],
                "complejidad_queso": datos["Complejidades"]["Queso"],
                "complejidad_croissant": datos["Complejidades"]["Croissant"],
                "eficiencia": round(datos["eficiencia"]),
                "estado": datos["estado"]
            }
            filas.append(fila)

        nuevo_df_formateado = pd.DataFrame(filas)

        
        df = df[~df["operario"].isin(nuevo_df_formateado["operario"])]

        
        df = pd.concat([df, nuevo_df_formateado], ignore_index=True)

        mb.showinfo("Éxito", "Datos registrados correctamente.")
    else:
        mb.showinfo("Cancelado", "Registro cancelado o inválido.")

def mostrar_reporte_general():
    if df.empty:
        mb.showwarning("Advertencia", "No hay datos registrados.")
        return
    reporte = rg(df)
    reporte.mostrar_resumen()
    reporte.graficar()

def mostrar_reporte_individual():
    if df.empty:
        mb.showwarning("Advertencia", "No hay datos registrados.")
        return

    nombre = sd.askstring("Reporte Individual", "Ingrese el nombre del operario:")
    if not nombre or nombre.strip() == "":
        mb.showwarning("Entrada inválida", "Debe ingresar un nombre válido.")
        return

    reporte_ind = ri(df)
    reporte_ind.mostrar_por_operario(nombre)


tk.Label(ventana, text="Seleccione una opción").pack(pady=20)

tk.Button(ventana, text="1. Registrar producción diaria", width=30, command=registrar_produccion).pack(pady=5)
tk.Button(ventana, text="2. Mostrar reporte general", width=30, command=mostrar_reporte_general).pack(pady=5)
tk.Button(ventana, text="3. Mostrar reporte individual", width=30, command=mostrar_reporte_individual).pack(pady=5)
tk.Button(ventana, text="4. Salir", width=30, command=ventana.quit).pack(pady=5)

ventana.mainloop()