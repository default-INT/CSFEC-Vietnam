import math
from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk   
from tkinter import messagebox

class GUI(tk.Frame):
    active_color_text = 'black'
    active_color = 'gray'
    button_color = 'blue'
    text_button = '#ffffff'
    back_color = '#f5f5f5'
    text_color = 'black'

    def __init__(self, root):
        super().__init__(root)
        self.main_window()

    def main_window(self):
        create_button = tk.Button(root, text = 'Ввести данные', font = "Arial 12", activebackground = self.active_color,
                                  command = self.input_window, bg = self.button_color, fg = self.text_button,
                                   activeforeground = self.active_color_text, bd=0, compound = tk.TOP)
        create_button.grid(row = 0, column = 0, ipadx = 50, ipady=10 , padx = 5, pady = 5)

        save_button = tk.Button(root, text = 'Сохранить данные', font = "Arial 12", activebackground = self.active_color,
                                  command = self.input_window, bg = self.button_color, fg = self.text_button,
                                   activeforeground = self.active_color_text, bd=0, compound = tk.TOP)
        save_button.grid(row = 0, column = 1, ipadx = 50, ipady=10 , padx = 5, pady = 5)

    def input_window(self):
        data = self.ChildWindow([self.active_color_text, self.active_color,
                                self.button_color, self.back_color, self.text_color]).read_window()

    class ChildWindow(tk.Toplevel):
        active_color_text = None
        active_color = None
        button_color = None
        back_color = None
        text_color = None

        def __init__(self, colors):
            super().__init__()
            self.active_color_text = colors[0]
            self.active_color = colors[1]
            self.button_color = colors[2]
            self.back_color = colors[3]
            self.text_color = colors[4]

        def read_window(self):
            for widget in self.winfo_children():
                widget.destroy()
            
            self.title('Ввод исходных данных')
            self.geometry('500x350+345+90')
            self.resizable(False, False)
            self.config(bg = self.back_color)
            self.grab_set()
            self.focus_set()

            title_lable = tk.Label(self, text="Введите значения", bg = self.back_color,
                                    fg = self.text_color, font = "Arial 16")
            title_lable.grid(row = 0, column = 1, padx = 5, pady = 5)

            length_lable = tk.Label(self, text="Введите длину (м):", bg = self.back_color,
                                    fg = self.text_color, font = "Arial 14")
            length_lable.grid(row = 1, column = 0, padx = 5, pady = 5)
            self.length_input = tk.Entry(self, width = 30, bg = 'white', fg = self.text_color)
            self.length_input.grid(row = 1, column = 1, padx = 5, pady = 5)

            d_cut_lable = tk.Label(self, text="Введите диаметр сечения (м):", bg = self.back_color,
                                    fg = self.text_color, font = "Arial 14")
            d_cut_lable.grid(row = 2, column = 0, padx = 5, pady = 5)
            self.d_cut_input = tk.Entry(self, width = 30, bg = 'white', fg = self.text_color)
            self.d_cut_input.grid(row = 2, column = 1, padx = 5, pady = 5)

            material_lable = tk.Label(self, text="Выберите материал:", bg = self.back_color,
                                    fg = self.text_color, font = "Arial 14")
            material_lable.grid(row = 3, column = 0, padx = 5, pady = 5)
            self.material_combo = ttk.Combobox(self)
            self.material_combo['values'] = ('Метал', 'Олово')
            self.material_combo.grid(row = 3, column = 1, padx = 5, pady = 5)

            accept_button = tk.Button(self, text = 'Ввести данные', font = "Arial 12", activebackground = self.active_color,
                                  command = self.accept, bg = 'green', fg = 'white',
                                   activeforeground = self.active_color_text, bd=0, compound = tk.TOP)
            accept_button.grid(row = 4, column = 0, ipadx = 50, ipady=10 , padx = 5, pady = 5)

        def accept(self):
            try:
                data = [float(self.length_input.get()), float(self.d_cut_input.get()), self.material_combo.get()]
                return data
            except:
                messagebox.showerror('Ошибка', 'Неверно введены значения.')

if __name__ == "__main__":
    root=tk.Tk()
    root.geometry('800x420+140+90')
    root.config(bg='#ffffff')
    root.title('Лабараторная работа №1. Современные численные методы решения граничных задач')
    GUI(root)
    root.resizable(False, False) 
    root.mainloop()