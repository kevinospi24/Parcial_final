
import random
import pandas as pd
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import matplotlib.pyplot as plt

class registro():
    def __init__(self):
        self.datos = {}

    def pedir_unidades(self, tipo_pan):
        while True:
            try:
                cantidad = sd.askinteger("Cantidad", f"Ingrese unidades de {tipo_pan} (0 - 500):")
                if cantidad is None:
                    return None
                if 0 <= cantidad <= 500:
                    return cantidad
                else:
                    mb.showwarning("Rango inválido", "Debe estar entre 0 y 500.")
            except ValueError:
                mb.showerror("Error", "Entrada inválida. Debe ser un número entero.")

    def registrar(self):
        nombre = sd.askstring("Operario", "Nombre del operario:")
        if not nombre:
            mb.showwarning("Entrada inválida", "Debe ingresar un operario para iniciar")
            return None

        unidad_pan_f = self.pedir_unidades("Pan francés")
        if unidad_pan_f is None:
            return None
        unidad_pan_q = self.pedir_unidades("Pan queso")
        if unidad_pan_q is None:
            return None
        unidad_pan_c = self.pedir_unidades("Croissant")
        if unidad_pan_c is None:
            return None

        complejidades = []
        total_complejidades = 0
        total_ponderado = 0
        for producto in [unidad_pan_c, unidad_pan_f, unidad_pan_q]:
            complejidad = round(random.uniform(1.0, 1.5), 2)
            complejidades.append(complejidad)
            total_ponderado += producto * complejidad
            total_complejidades += complejidad

        eficiencia = total_ponderado / total_complejidades

        estado = "Cumple" if eficiencia >= 300 else "No cumple"
        print(estado)

        self.datos[nombre] = {
            "Cantidades": {
                "Frances": unidad_pan_f,
                "Queso": unidad_pan_q,
                "Croissant": unidad_pan_c
            },
            "Complejidades": {
                "Francés": complejidades[1],
                "Queso": complejidades[2],
                "Croissant": complejidades[0]
            },
            "eficiencia": round(eficiencia),
            "estado": estado
        }

        mb.showinfo("Registro completado", f"Operario: {nombre}\nEficiencia: {eficiencia:.2f} ({estado})")
        return pd.DataFrame.from_dict(self.datos, orient='index')


class ReporteGeneral:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def mostrar_resumen(self):
        if self.df.empty:
            print("No hay datos para mostrar.")
            return

        resumen = self.df[["operario", "eficiencia", "estado"]]
        print(resumen)

        print("\nEstadísticas:")
        print(self.df["eficiencia"].describe())

        promedio = self.df["eficiencia"].mean()
        print(f"\nPromedio del grupo: {promedio:.2f}")

    def graficar(self):
        if self.df.empty:
            print("No hay datos para graficar.")
            return

        self.df["estado"].value_counts().plot.pie(autopct='%1.1f%%', title="Cumplimiento de Meta")
        plt.show()

        correlacion = self.df[["pan_frances", "pan_queso", "croissants"]].corr()
        print("\nCorrelación entre productos:")
        print(correlacion)

        correlacion.plot(kind='bar', title="Correlación entre productos")
        plt.tight_layout()
        plt.show()


class ReporteIndividual:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def mostrar_por_operario(self, nombre):
        df_op = self.df[self.df["operario"].str.lower() == nombre.strip().lower()]
        if df_op.empty:
            print(f"No se encontró información para el operario '{nombre}'.")
            return

        registro = df_op.iloc[0]
        print(f"Operario: {registro['operario']}")
        print(f"Eficiencia: {registro['eficiencia']}")
        print(f"Estado: {registro['estado']}")

        cantidades = [registro["pan_frances"], registro["pan_queso"], registro["croissants"]]
        complejidades = [registro["complejidad_frances"], registro["complejidad_queso"], registro["complejidad_croissant"]]
        eficiencia_ponderada = [cantidades[i] * complejidades[i] for i in range(3)]
        productos = ["Pan francés", "Pan de queso", "Croissants"]

        plt.bar(productos, cantidades)
        plt.title("Producción por tipo de pan")
        plt.show()

        plt.bar(productos, complejidades)
        plt.title("Complejidad por tipo de pan")
        plt.show()

        plt.bar(productos, eficiencia_ponderada)
        plt.title("Eficiencia ponderada por tipo de pan")
        plt.show()
