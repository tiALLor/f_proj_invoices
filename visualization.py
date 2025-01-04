from tkinter import *


class Table:
    def __init__(self, root, data) -> None:
        total_rows = len(data)
        total_columns = len(data[0])

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(
                    root,
                    width=15,
                    fg="black",
                    font=(
                        "Arial",
                        12,
                    ),
                )
                # font=('Arial',16,'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, data[i][j])


def show_table(header, lines=0, title=0) -> None:
    if title == 0:
        title = f"Showing data of purchased items"
    if lines == 0:
        tab = header
    else:
        tab = header + lines
    root = Tk()
    root.title(title)
    t = Table(root, tab)
    root.mainloop()
