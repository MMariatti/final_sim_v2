import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from django.http import HttpResponse
from django.shortcuts import render
from .utils import funcion_logistica, funcion_logistica_inversa, aproximar_combustible_euler


def get_ejercicio(request):
    return render(request, 'ejercicio.html')


# Función para obtener la resolución
def get_resolucion(request):
    # Datos proporcionados
    combustible = [0.005, 0.015, 0.02, 0.025]
    rpm = [1200, 3500, 4400, 5000]

    # Ajuste de la curva logística
    params, _ = curve_fit(funcion_logistica, combustible, rpm, p0=[8000, 0, np.mean(combustible)], maxfev=10000)

    # Parámetros del ajuste
    L, k, x0 = params

    # L = cantidad maxima de revoluciones por minuto
    # k = velocidad maxima a la que llegara el motor
    # x0 = cantidad de combustible aproximadamente por minuto

    # combustible inyectado aprox para L
    combustible_aprox = aproximar_combustible_euler(L, k, x0, L)

    # metodo alternativo
    # np.interp(L, rpm, combustible)

    # b. Revoluciones por minuto para otros valores de combustible inyectado
    combustible_valores_especificos = np.array([0.03, 0.05, 0.065, 0.1])
    combustible_predicciones = np.linspace(min(combustible), max(combustible), 100)
    rpm_valores_especificos = funcion_logistica(combustible_valores_especificos, L, k, x0)

    # Valores para la gráfica
    combustible_grafica = np.linspace(0, 0.1, 100)  # Valores de combustible para la gráfica
    rpm_grafica = funcion_logistica(combustible_grafica, L, k, x0)

    # Graficar
    plt.figure(figsize=(8, 6))
    plt.scatter(combustible, rpm, label='Datos', color='blue')
    plt.plot(combustible_grafica, rpm_grafica, 'r', label='Curva Logística Ajustada', linewidth=2)

    # Agregar puntos para valores específicos de combustible y RPM correspondientes
    plt.scatter(combustible_valores_especificos, rpm_valores_especificos, c='green', marker='o',
                label='Valores Específicos')

    plt.xlabel('Cantidad de Combustible Inyectado (mm^3 por minuto)')
    plt.ylabel('Revoluciones por Minuto (RPM)')
    plt.title('Relación entre Combustible y RPM')
    plt.legend()
    plt.grid(True)

    # Guardar la imagen en un archivo en la carpeta static
    plt.savefig('ejercicio/static/resolucion_plot.png')

    contexto = {'resultado_a': round(L, 4),
                'combustible_aprox': format(combustible_aprox, '.4f'),
                'resultado_b_03': format(rpm_valores_especificos[0], '.4f'),
                'resultado_b_05': format(rpm_valores_especificos[1], '.4f'),
                'resultado_b_065': format(rpm_valores_especificos[2], '.4f'),
                'resultado_b_1': format(rpm_valores_especificos[3], '.4f'),
                }

    return render(request, 'resolucion.html', context=contexto)


def resolucion_parametrizable(request):
    # válido el metodo de la request
    if request.method == 'GET':
        context = {'renderizar': False}
        return render(request, 'resolucion_parametrizable.html', context=context)
    elif request.method == 'POST':

        query_dict = request.POST
        data_dict = {key: value for key, value in query_dict.items()}
        if all(data_dict.values()):

            lista_combustible = data_dict['combustible'].split(',')
            lista_rpm = data_dict['rpm'].split(',')
            if len(lista_combustible) != len(lista_rpm):
                context = {'renderizar': False, 'datos_incompletos': True}
                return render(request, 'resolucion_parametrizable.html', context=context)

            # Obtengo la lista numerica de combustible
            valores_combustible = [float(i) for i in lista_combustible]

            # Obtengo la lista numerica de rpm
            valores_rpm = [int(i) for i in lista_rpm]

            # Obtengo la lista numerica de p0
            lista_p0 = data_dict['p0'].split(',')
            valores_p0 = [float(i) for i in lista_p0]

            # Obtengo la lista numerica de los valores de combustible para los que se quiere saber la rpm
            lista_combustible_b = data_dict['combustible_b'].split(',')
            valores_combustible_b = [float(i) for i in lista_combustible_b]

            # Ajuste de la curva logística
            params, _ = curve_fit(funcion_logistica, valores_combustible, valores_rpm, p0=valores_p0, maxfev=10000)

            # Parámetros del ajuste
            L, k, x0 = params

            combustible_aprox_max_rpm = aproximar_combustible_euler(L, k, x0, L)
            # metodo alternativo
            # np.interp(L, valores_rpm, valores_combustible)

            # Calculo de los valores de rpm para los valores de combustible especificados en el punto b
            rpm_valores_especificos = funcion_logistica(valores_combustible_b, L, k, x0)

            # formateo valores_especificos a 4 decimales
            rpm_valores_especificos_formateados = [format(i, '.4f') for i in rpm_valores_especificos]

            # Junto los 2 arrays de combustibles para graficar
            maximo_grafica = max(valores_combustible + valores_combustible_b)
            print(maximo_grafica)

            combustible_grafica = np.linspace(0, maximo_grafica, 100)  # Valores de combustible para la
            # gráfica
            rpm_grafica = funcion_logistica(combustible_grafica, L, k, x0)

            # Graficar
            plt.figure(figsize=(8, 6))
            plt.scatter(valores_combustible, valores_rpm, label='Datos', color='blue')
            plt.plot(combustible_grafica, rpm_grafica, 'r', label='Curva Logística Ajustada', linewidth=2)

            # Agregar puntos para valores específicos de combustible y RPM correspondientes
            plt.scatter(valores_combustible_b, rpm_valores_especificos, c='green', marker='o',
                        label='Valores Específicos')

            plt.xlabel('Cantidad de Combustible Inyectado (mm^3 por minuto)')
            plt.ylabel('Revoluciones por Minuto (RPM)')
            plt.title('Relación entre Combustible y RPM')
            plt.legend()
            plt.grid(True)

            # Guardar la imagen en un archivo en la carpeta static
            plt.savefig('ejercicio/static/resolucion_param_plot.png')

            # Convertimos valores?rpm y valores?combustibles a una lista de tuplas
            tupla_tabla = list(zip(valores_rpm, valores_combustible))
            tupla_punto_b = list(zip(valores_combustible_b, rpm_valores_especificos_formateados))

            context = {'renderizar': True,
                       'datos_incompletos': False,
                       'tupla_tabla': tupla_tabla,
                       'valores_combustible': valores_combustible,
                       'resultado_a': round(L, 4),
                       'combustible_aprox': format(combustible_aprox_max_rpm, '.4f'),
                       'tupla_punto_b': tupla_punto_b,
                       }
            return render(request, 'resolucion_parametrizable.html', context=context)
        else:
            context = {'renderizar': False, 'datos_incompletos': True}
            return render(request, 'resolucion_parametrizable.html', context=context)
