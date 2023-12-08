import numpy as np
import os
import customtkinter
import matplotlib.pyplot as plt
from customtkinter import *
from sympy import sympify, symbols, simplify, N, I, solve

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title("Ecuaciones de Cauchy")
root.geometry("500x550")

interFuncion = customtkinter.StringVar(root)
interRadio = customtkinter.StringVar(root)
interCentro = customtkinter.StringVar(root)

os.system("cls")

def fun(x,y):
  return y
x_0 = 0
y_0 = 1
# Tamaño de paso
h_ = .25
# Punto a aproximar
x_n = 1

def login():
    os.system("cls")
    funcion = interFuncion.get()
    try:
        # Convertir la entrada del usuario a una expresión simbólica
        z = symbols('z')

        # Reemplazar automáticamente "x" por "z" y permitir números complejos
        funcion = funcion.replace('x', '*z')
        funcion = funcion.replace('I', 'I*1.0')  # Agregar 1.0 para que I se interprete como complejo
        SympyFuncion = sympify(funcion)

        # Imprimir la función simplificada
        funcionSimplificada = simplify(SympyFuncion)
        print("\033[95mFunción simplificada: \033[0m")
        print(funcionSimplificada)

        # Verificar y manejar casos en los que la función puede ser indeterminada
        denominador = funcionSimplificada.as_numer_denom()[1]
        puntosIndeterminados = solve(denominador, z)

        print(f"\033[95m\nPuntos de indeterminación:\033[0m {puntosIndeterminados}")

    except Exception as e:
        print("Hubo un error al procesar la entrada:")
        print(e)

    # ---------------------------------------------------------------------------
    # Almacena los puntos de indeterminación en arreglos
    puntosX = []
    puntosY = []
    for solucion in puntosIndeterminados:
        print(f"\033[93mParte Real: \033[0m{solucion.as_real_imag()[0]}   \033[93mParte Imaginaria: \033[0m{solucion.as_real_imag()[1]}")
        auxReal, auxImg = solucion.as_real_imag()
        puntosX.append(auxReal)
        puntosY.append(auxImg)

    menorX=puntosX[0]
    mayorX=puntosX[0]
    for n in puntosX:
        if(n < menorX):
            menorX=n
        if(n > mayorX):
            mayorX=n
    menorY=puntosY[0]
    mayorY=puntosY[0]
    for n in puntosY:
        if(n < menorY):
            menorY=n
        if(n > mayorY):
            mayorY=n
    
    # ---------------------------------------------------------------------------
    # Convierte la entrada del centro y radio de la circunferencia
    centro = interCentro.get()
    try:
        # Convertir la entrada del usuario a una expresión simbólica
        z = symbols('z')
        # Reemplazar automáticamente "x" por "z" y permitir números complejos
        centro = centro.replace('x', '*z')
        centro = centro.replace('I', 'I*1.0')  # Agregar 1.0 para que I se interprete como complejo
        SympyCentro = sympify(centro)
    except Exception as e:
        print("\033[91mHubo un error al procesar la entrada: \033[0m")
        print(e)
    circulo_real, circulo_imaginaria = SympyCentro.as_real_imag()
    print("\033[95m\nCircunferencia\033[0m")
    print("\033[93mCentro: \033[0m",SympyCentro)
    radio = float(interRadio.get())
    print("\033[93mRadio: \033[0m",radio)

    if(circulo_real-radio < menorX):
        menorX=circulo_real-radio
    if(circulo_real+radio > mayorX):
        mayorX=circulo_real+radio

    if(circulo_imaginaria-radio < menorY):
        menorY=circulo_imaginaria-radio
    if(circulo_imaginaria+radio > mayorY):
        mayorY=circulo_imaginaria+radio

    print("Menor en X:", menorX)
    print("Mayor en X:", mayorX)
    print("Menor en Y:", menorY)
    print("Mayor en Y:", mayorY)

    LatexFuncion = interFuncion.get()
    tokens=[]
    estado=0
    lexema = ""
    i=0
    while(i<len(LatexFuncion)):
        if estado==0:
            if LatexFuncion[i]=='(':
                tokens.append('(')
                estado=0
            elif LatexFuncion[i]==')':
                tokens.append(')')
                estado=0
            elif LatexFuncion[i]=='z':
                tokens.append('z')
                estado=0
            elif LatexFuncion[i]=='I':
                tokens.append('i')
                estado=0
            elif LatexFuncion[i]=='*':
                estado=1
            elif LatexFuncion[i] in '0123456789':
                lexema+=LatexFuncion[i]
                estado=3
            elif LatexFuncion[i]=='+':
                tokens.append('+')
                estado=0
            elif LatexFuncion[i]=='-':
                tokens.append('-')
                estado=0
            elif LatexFuncion[i]=='/':
                tokens.append('/')
                estado=0
        elif estado==1:
            if LatexFuncion[i]=='*':
                tokens.append('^')
                estado=0
            else:
                tokens.append('*')
                estado=0
                i-=1
        elif estado==3:
            if LatexFuncion[i] in '0123456789':
                lexema+=LatexFuncion[i]
                estado=3
            else:
                tokens.append(lexema)
                lexema=""
                estado=0
                i-=1
        i+=1
    lat=""
    for t in tokens:
        print("token",t)


            

    # ---------------------------------------------------------------------------
    # GRAFICACIÓN
    PlotCirculo = plt.Circle((circulo_real, circulo_imaginaria), radio, color='b', fill=False)
    

    fig, ax = plt.subplots()
    
    ax.scatter(puntosX, puntosY, color='red', marker='o')
    ax.set_xlabel('Parte Real')
    ax.set_ylabel('Parte Imaginaria')
    ax.set_title('Contorno y puntos de indeterminación')
    ax.set_xlim(float(menorX-1), float(mayorX+1))
    ax.set_ylim(float(menorY-1), float(mayorY+1))
    ax.grid(True)
    ax.legend()
    ax.add_patch(PlotCirculo)

    plt.show()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Función a evaluar en términos de z")
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, textvariable=interFuncion)
entry1.pack(pady=12, padx=5)

label2 = customtkinter.CTkLabel(master=frame, text="Centro de la circunferencia")
label2.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, textvariable=interCentro)
entry2.pack(pady=12, padx=10)

label3 = customtkinter.CTkLabel(master=frame, text="Radio de la circunferencia")
label3.pack(pady=12, padx=10)

entry3 = customtkinter.CTkEntry(master=frame, textvariable=interRadio)
entry3.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Ejecutar", command=lambda: login())
button.pack(pady=12, padx=10)

root.mainloop()



def main():
    
    '''
    Este programa permite al usuario ingresar una función simbólica,
    la imprime de manera simplificada y luego le pide al usuario que
    ingrese un valor numérico (complejo) para evaluar la función en ese punto.
    También maneja casos en los que la función puede ser indeterminada.
    '''

    # Pedir al usuario que ingrese la función
    funcion = input("Ingresa la función en términos de z: ")

    try:
        # Convertir la entrada del usuario a una expresión simbólica
        z = symbols('z')

        # Reemplazar automáticamente "x" por "z" y permitir números complejos
        funcion = funcion.replace('x', '*z')
        funcion = funcion.replace('I', 'I*1.0')  # Agregar 1.0 para que I se interprete como complejo

        SympyFuncion = sympify(funcion)

        # Imprimir la función simplificada
        funcionSimplificada = simplify(SympyFuncion)
        print("La función que ingresaste simplificada es:")
        print(funcionSimplificada)

        # Verificar y manejar casos en los que la función puede ser indeterminada
        denominador = funcionSimplificada.as_numer_denom()[1]
        puntosIndeterminados = solve(denominador, z)

        
        print(f"La función es indeterminada en los siguientes puntos (denominador igual a cero): {puntosIndeterminados}")

    except Exception as e:
        print("Hubo un error al procesar la entrada:")
        print(e)

    print("Defina el contorno en el que se encuentra definida la funcion\n")

    z0_real = float(input("Ingrese la parte real del origen: "))  # Parte real del origen
    z0_imag = float(input("Ingrese la parte imaginaria del origen: "))  # Parte imaginaria del origen
    radius = float(input("Ingrese el radio del contorno: "))  # Radio del contorno circular


    """
    for term in puntosIndeterminados:
        if abs(term - (z0_real + z0_imag * 1j)) <= radius:
            # Raíz dentro del contorno
            print(f"La raíz {term} está dentro del contorno.")
            pc_input_z_cero = z - term
        else:
            # Raíz fuera del contorno, la integral es cero
            print(f"La raíz {term} está fuera del contorno.")
            print("La integral asociada a esta raíz es cero.")
            pc_input_z_normal = z - term

    pc_semi_final_input = funcionSimplificada.as_numer_denom()[0]
    print("El numerador o q_1(z) es: " + str(pc_semi_final_input))
    pc_final_input=pc_semi_final_input/pc_input_z_normal
    print("El f(z) es: " + str(pc_final_input))
    """
    


"""
if __name__ == "__main__":
    main()"""