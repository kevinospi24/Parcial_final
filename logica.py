import random
import pandas
import tkinter as tk


class registro():
    
    def __init__(self):
        self.datos = {}
        
    def pedir_unidades(self, tipo_pan):
        while True:
            try:
                cantidad = int(input(f"Ingrese unidades de {tipo_pan} (0 - 500): "))
                if 0 <= cantidad <= 500:
                    return cantidad
                else:
                    print(" Debe estar entre 0 y 500.")
            except ValueError:
                print(" Entrada inválida. Debe ser un número entero.")
                
    def registrar(self):
        nombre = input("Nombre del operario:\n")
        unidad_pan_f = self.pedir_unidades("Pan francés")
        unidad_pan_q = self.pedir_unidades("Pan queso")
        unidad_pan_c = self.pedir_unidades("Croissant")
        
        complejidades = []
        total_complejidades = 0
        total_ponderado = 0
        for producto in [unidad_pan_c , unidad_pan_f , unidad_pan_q]:
            complejidad = round(random.uniform(1.0 , 1.5) , 2)
            complejidades.append(complejidad)
            total_ponderado += producto * complejidad 
            total_complejidades += complejidad
            
        eficiencia = total_ponderado / total_complejidades
        
        if eficiencia >= 300:
            estado = "Cumple"
            print(estado)
        else:
            estado = "No cumple"
            print(estado)
            
        self.datos[nombre] = {
            "Cantidades" : {
                "Frances" : unidad_pan_f ,
                "Queso" : unidad_pan_q , 
                "Croissant" : unidad_pan_c
            } ,
            "Complejidades" : {
                "Croissant" : complejidades[0] ,
                "Francés" : complejidades[1] ,
                "Queso" : complejidades[2]
            } , 
            "eficiencia": eficiencia,
            "estado": estado
        }

        print(f"Registro completado para {nombre} - Eficiencia: {eficiencia} ({estado})")
           
    
        
    
registro().registrar()



    
    
    
    
    

        
        

        
        
        
        
        

        
    
    
    
    
    
