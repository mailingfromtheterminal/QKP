#--------------------------------------------------------Inicio del Lector---------------------------------------------------------#
import time

f = open("C:/Users/hijod/Desktop/QKP-main/QKP/Instances/Prueba.txt", "r")
f.readline()
v = int(f.readline())
#print(v)

Matriz = []

b = f.readline().split()
#print(b)

for x in f:
    a = x.split()
    Matriz.append(a)

c = 0
for row in Matriz:
    if len(row) < v:
        if c < len(b):
            #print(f"Agregando {b[c]} a la fila {row}")
            row.append(b[c])
            c += 1
        else:
            #print("No hay más elementos en b")
            break
    else:
        #print("Longitud de fila alcanzada")
        break

# Guardar las dos últimas filas en variables distintas
PxI = None
Pmax = None

for i in Matriz:
    #print(i)

    # Actualizar las variables de las últimas dos filas
    Pmax = PxI
    PxI = i

# Eliminar las dos últimas filas de la matriz
Matriz.pop()  # Eliminar la última fila
Matriz.pop()  # Eliminar la penúltima fila
Matriz.pop()  # Elimina la antepenúltima fila

#print(Matriz)

# Hacer una copia de la matriz llamada "MatrizTrabajo"
MatrizTrabajo = [list(fila) for fila in Matriz]

# Mostrar la matriz después de eliminar las dos últimas filas
#print("Matriz después de eliminar las dos últimas filas:")
#for i in Matriz:
    #print(i)

# Mostrar la copia de la matriz
#print("MatrizTrabajo:")
#for i in MatrizTrabajo:
    #print(i)

#----------------------------------------- Fin del lector--------------------------------------#
time.sleep(1)
#-----------------------------------Aplicacion de la heuristica--------------------------------#

AntEle = None
maximo_global = None
ubicacion_max_global = None
Pc = 0
Peso = int(Pmax[0])
sumatoria_max_global = 0
items_agregados = []  # Lista para almacenar los ítems agregados
Lista_Max = []
FilasMt = []
ListaUG = []

while Pc < Peso:
    AntEle = None
    maximo_global = None

    if ubicacion_max_global is not None:
        fila_anterior = ubicacion_max_global[0] - 1
        Matriz[fila_anterior][-1] = float('-inf')

    for i, fila in enumerate(Matriz):
        ultimo_elemento = float(fila[-1])

        if maximo_global is None or ultimo_elemento > maximo_global:
            maximo_global = ultimo_elemento
            ubicacion_max_global = (i + 1, len(fila))

        AntEle = ultimo_elemento

    #print(f"Máximo global: {maximo_global}")
    #print(f"Ubicación del máximo global: Fila {ubicacion_max_global[0]}, Columna {ubicacion_max_global[1]}")
    #print(PxI)

    aux=ubicacion_max_global[0]
    aux = aux-1
    aux2=ubicacion_max_global[1]
    aux2=aux2-1

    FilasMt.append(aux)
    #print("este fue el item agregado:")
    #print(aux)
    ListaUG.append(aux2)
    #print("este otro tambien se agrego:")
    #print(aux2)


    maximo_global = int(maximo_global)
    Lista_Max.append(maximo_global)
    sumatoria_max_global += maximo_global

    for i in range(len(PxI)):
        if i == ubicacion_max_global[1] - 1:
            item_agregado = PxI[i]
            items_agregados.append(item_agregado)
            #print(item_agregado)
            Pc += int(item_agregado)

    #print(f"Nueva Pc: {Pc}")

    if Pc > Peso:
        valor_eliminado = PxI[ubicacion_max_global[1] - 1]
        Pc -= int(valor_eliminado)
        items_agregados.remove(valor_eliminado)
        Lista_Max.remove(maximo_global)
        sumatoria_max_global -= maximo_global
        ListaUG.pop()
        FilasMt.pop()

        #print(f"Se ha superado el peso. Restaurando Pc a: {Pc}")
        #print(f"Se eliminó el item: {maximo_global}, que tiene valor de: {valor_eliminado}")
        #print(f"Ganancia individual total: {sumatoria_max_global}")
        #print(f"Lista de valores inndividuales agregados: {Lista_Max}")
        #print("Items agregados:", items_agregados)

        break

Ganancia_c=0
j = 0
index = 0
k = 1
ultima_k = 0
ListaCop = ListaUG.copy()
ListaUG.pop(0)
ListaUG.pop(1)
ListaUG=ListaCop.copy()
#print(ListaUG)
time.sleep(10)
ListaUG.pop(0)
Matriz = [list(fila) for fila in MatrizTrabajo]
AntEle = None
AuxList =Lista_Max.copy()
maximo_global = None
Lista_Max.pop(0)
j = 0
while j < len(ListaUG) + 1:
    for i, fila in enumerate(Matriz):
        ultimo_elemento = float(fila[-1])
        #print(f"Este es el ultimo elemento actualmente: {ultimo_elemento}")

        if len(Lista_Max) < 1:
            break

        encontrado = False
        for indice, valor in enumerate(Lista_Max):
            #print(f"Este es el ultimo elemento actualmente: {ultimo_elemento}")
            #print(f"este es valor: {valor}")
            if valor == ultimo_elemento:
                encontrado = True
                #print(f"Este elemento coincide con la lista de valores individuales: {ultimo_elemento} = {valor}")
                Lista_Max.pop(indice)
                ubicacion_max_global = (i, len(fila))
                #print(f"Esta es la ubicación global de: {ultimo_elemento} en fila {i + 1}, columna {len(fila)}")
                break

        #if not encontrado:
            #print(f"No se encontró coincidencia para el elemento: {ultimo_elemento}")
    
    if len(Lista_Max) > 0:
        # Si quedan elementos en Lista_Max, elimina el primero
        Lista_Max.pop(0)

    j += 1