from tkinter import *
import tkinter.messagebox as mb
import numpy as np
from matplotlib import pyplot as plt


window = Tk()
window.title("Метод половинного деления")
window.geometry("800x500")




coefs = []
start_root = 0
end_root = 0
accuracy = 0


def check_good_input():  # checking that all parameters for root calculation are entered and correct
    try:
        global start_root, end_root, accuracy
        coefs.clear()
        coefs_dict.clear()
        for i in inputCoefs.get().split():
            coefs.append(int(i))
        for i in range(0, len(coefs)):
            coefs_dict[len(coefs) - i - 1] = coefs[i]
        start_root = int(x_start_root.get())
        end_root = int(x_end_root.get())
        accuracy = float(accuracy_in.get())
        return True
    except:
        coefs.clear()
        coefs_dict.clear()
        result.config(text="")
        return False


coefs_dict = {}


def print_equation():  # printing equation
    equa = "y = "
    for k, v in coefs_dict.items():
        el = ""
        if v == 0:
            continue
        elif v == 1 and k != len(coefs_dict) - 1 and k != 0:
            el += "+"
        elif v == -1 and k != 0:
            el += "-"
        elif v > 0 and k != len(coefs_dict) - 1 and k != 0:
            el += f"+{v}"
        elif v < 0 and k != 0:
            el += f"{v}"

        if k > 1:
            el += f"x^{k}"
        elif k == 1:
            el += "x"
        elif k == 0:
            if v < 0:
                el += f"{v}"
            else:
                el += f"+{v}"

        equa += el + " "
    finalEquation.config(text=equa)


def count_root():  # method for counting roots
    x_start = start_root
    x_end = end_root

    x_start_num = 0
    x_end_num = 0
    coefs.reverse()

    for i in range(len(coefs)):
        x_start_num += coefs[i] * (x_start ** i)
        x_end_num += coefs[i] * (x_end ** i)
    if (x_start_num > 0 and x_end_num > 0) or (x_start_num < 0 and x_end_num < 0):
        mb.showwarning("!!!", "На указанном диапазоне корень отсутствует, или их больше, чем 1")
        return
    if x_start_num == 0:
        mb.showwarning("Корень найден", f"Значение корня = {x_start}")
        return
    if x_end_num == 0:
        mb.showwarning("Корень найден", f"Значение корня = {x_end}")
        return

    while x_end - x_start > accuracy / 2:  # cycle for the method of half division up to the specified accuracy
        x_mid = (x_start + x_end) / 2
        x_mid_num = 0
        for i in range(len(coefs)):
            x_mid_num += coefs[i] * (x_mid ** i)

        if x_start_num > 0 and x_mid_num > 0 or x_start_num < 0 and x_mid_num < 0:
            x_start_num = x_mid_num
            x_start = x_mid
        else:
            x_end_num = x_mid_num
            x_end = x_mid

    result.config(text=f"Приближенное значение корня = {x_end}")
    mb.showwarning("!!!", f"Приближенное значение корня на указанном диапазоне ({start_root};{end_root}) "
                          f"при точности {accuracy} = {x_end}")


########################## CHECKS FOR X AND ACCURACY


start_graph = 0
end_graph = 0


def check_input():  # checking that all parameters for plotting are entered and correct
    try:
        global start_graph, end_graph
        start_graph = int(x_start_graph.get())
        end_graph = int(x_end_graph.get())
        return True
    except:
        mb.showwarning("!!!", "Убедитесь, что все значения введены верно")
        return False


######################### GRAPH

def show_graph():  # plotting
    if not check_input():
        mb.showerror("Убедитесь, что значения введены верно")
        return
    try:
        coefs.clear()
        for i in inputCoefs.get().split():
            coefs.append(int(i))

        coefs.reverse()

        x = np.linspace(start_graph, end_graph, 100)
        y = np.array([np.sum(np.array([coefs[i] * (j ** i) for i in range(len(coefs))])) for j in x])

        plt.plot(x, y)

        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')

        plt.title(finalEquation.cget("text"))
        plt.grid(visible=True)

        plt.show()
    except:
        mb.showerror("Убедитесь, что значения введены верно")



window.mainloop()
