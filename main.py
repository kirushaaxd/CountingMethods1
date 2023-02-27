from tkinter import *
import tkinter.messagebox as mb
import numpy as np
from matplotlib import pyplot as plt

window = Tk()
window.title("Метод половинного деления")
window.geometry("800x500")


def is_valid(value):
    return value[-1] in "0123456789- "


def count_click():
    if check_good_input():
        print_equation()
        count_root()
    else:
        mb.showerror("Неверно введены значения", "Пожалуйста, вводите корректные числовые значения")


coefs = []
start_root = 0
end_root = 0
accuracy = 0


def check_good_input():
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


def print_equation():
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


def count_root():
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

    while x_end - x_start > accuracy:
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


def check_x(value):
    return value[-1] in "-1234567890" and len(value) < 5


check2 = (window.register(check_x), "%P")


def check_accuracy(value):
    return value[-1] in "-1234567890."


check3 = (window.register(check_accuracy), "%P")


start_graph = 0
end_graph = 0


def check_input():
    try:
        global start_graph, end_graph
        start_graph = int(x_start_graph.get())
        end_graph = int(x_end_graph.get())
        return True
    except:
        return False


######################### GRAPH

def show_graph():
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


########################## ELEMENTS

check = (window.register(is_valid), "%P")

label1 = Label(window, text="Вводите коэффициенты через пробел", font=("Calibri", 20), fg="white")
label1.grid(column=0, row=0, columnspan=5)

inputCoefs = Entry(window, font=("Calibri", 26), validate="key", validatecommand=check, width=40)
inputCoefs.grid(column=0, row=1, columnspan=5)

label2 = Label(window, text="Ваше уравнение:", font=("Calibri", 22), fg="white")
label2.grid(column=0, row=3, pady=30, columnspan=5)

finalEquation = Label(window, font=("Calibri", 30), fg="gray")
finalEquation.grid(column=0, row=4, columnspan=5)


########################### ROOTS

label3 = Label(window, text="X старт (интервал):", font=("Calibri", 20), fg="white")
label3.grid(column=0, row=6, pady=5, padx=10, sticky=W)

x_start_root = Entry(window, font=("Calibri", 23), validate="key", validatecommand=check2, width=7)
x_start_root.grid(column=1, row=6, sticky=W)

label4 = Label(window, text="Х конечное (интервал):", font=("Calibri", 20), fg="white")
label4.grid(column=0, row=7, padx=10, sticky=W)

x_end_root = Entry(window, font=("Calibri", 23), validate="key", validatecommand=check2, width=7)
x_end_root.grid(column=1, row=7, sticky=W)

label4 = Label(window, text="Заданная точность:", font=("Calibri", 20), fg="white")
label4.grid(column=0, row=8, padx=10, sticky=W)

accuracy_in = Entry(window, font=("Calibri", 23), validate="key", validatecommand=check3, width=7)
accuracy_in.grid(column=1, row=8, sticky=W)

countButton = Button(text="Рассчитать корни", width=16, font=("Calibri", 16), command=count_click)
countButton.grid(column=0, row=9, padx=25, pady=15, columnspan=2)



############################ GRAPH

label3 = Label(window, text="X старт (график):", font=("Calibri", 20), fg="white")
label3.grid(column=3, row=6, pady=5, sticky=W)

x_start_graph = Entry(window, font=("Calibri", 23), validate="key", validatecommand=check2, width=7)
x_start_graph.grid(column=4, row=6, sticky=W)

label4 = Label(window, text="Х конечное (график):", font=("Calibri", 20), fg="white")
label4.grid(column=3, row=7, pady=5, sticky=W)

x_end_graph = Entry(window, font=("Calibri", 23), validate="key", validatecommand=check2, width=7)
x_end_graph.grid(column=4, row=7, sticky=W)

showGraph = Button(text="Построить график", width=16, font=("Calibri", 16), command=show_graph)
showGraph.grid(column=3, columnspan=2, row=8, pady=15)

l = Label(width=10)
l.grid(column=2, row=5)


result = Label(window, font=("Calibri", 20), fg="white")
result.grid(column=0, row=10, columnspan=5, padx=10, sticky=W)

window.mainloop()
