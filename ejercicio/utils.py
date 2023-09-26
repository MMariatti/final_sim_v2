import numpy as np


# Función logística
def funcion_logistica(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))


def funcion_logistica_inversa(L, k, x0, rpm):
    if L == rpm:
        print(rpm - 0.001)
        print(L)
        return x0 - (1 / k) * np.log(L / ((rpm + 0.001) - L))
    else:
        return x0 - (1 / k) * np.log(L / (rpm - L))


def aproximar_combustible_euler(L, k, x0, rpm_deseado, paso=0.001, tolerancia=0.01, max_iteraciones=1000):
    """
    Aproxima la cantidad de combustible inyectado para un valor de RPM deseado utilizando el método de Euler.

    Args:
        L (float): Capacidad máxima de RPM.
        k (float): Constante que afecta la pendiente de la curva logística.
        x0 (float): Valor de combustible en el que la curva alcanza la mitad de su capacidad máxima.
        rpm_deseado (float): RPM para el cual se desea calcular la cantidad de combustible.
        paso (float): Tamaño del paso en el método de Euler (opcional, por defecto 0.001).
        tolerancia (float): Tolerancia para la convergencia (opcional, por defecto 0.01).
        max_iteraciones (int): Número máximo de iteraciones (opcional, por defecto 100).

    Returns:
        float: Cantidad de combustible inyectado para el valor de RPM deseado, o None si no es alcanzable.
    """
    combustible_actual = np.mean(np.linspace(0, 0.2, 100))  # Valor inicial de combustible

    if L == rpm_deseado:
        rpm_deseado += 0.001

    for i in range(max_iteraciones):
        rpm_actual = funcion_logistica(combustible_actual, L, k, x0)

        # Comprobar si la aproximación es lo suficientemente cercana a L

        if abs(rpm_actual - rpm_deseado) < tolerancia:
            return combustible_actual

        # Calcular el cambio en el combustible_actual usando el método de Euler
        cambio_combustible = paso * (L - rpm_actual)  # Usando la derivada de la función logística

        # Actualizar el valor de combustible_actual
        combustible_actual += cambio_combustible

    # Si no se alcanza la convergencia, retornar None
    return None
