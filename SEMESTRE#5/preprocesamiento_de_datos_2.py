import pandas as pd

d = {"A":[1,2,3,4],
     "B":[3,4,1,None],
     "C":[3,5,7,9],
     "D":[None,3,5,6]
     }

ventas = pd.DataFrame(d)
#print(ventas)


ventas_ffill=ventas.ffill()
print("\n\n")

#print(ventas_ffill)

ventas_bfill = ventas.bfill()
#print(ventas_bfill)

#DATOS DUPLICADOS

duplicados = ventas.duplicated() #si existen datos duplicados

#subset revisa los dupliacados de columnas especificas
duplicados = ventas_bfill.duplicated(subset=["B","C"])
print(duplicados)


#ELIMINAR DUPLICADOS
eliminados = ventas.drop_duplicates()
print(eliminados)


#DATOS NULOS MIX
#concatenacion de metodos
mix = ventas.bfill().ffill()
mix1 = ventas.bfill().fillna(0)
print(mix)
print(mix1)

#ffill pa bajo
#bfill pa rriba

