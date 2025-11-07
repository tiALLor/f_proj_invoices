from tkinter import Tk, Entry, END
from typing import List, Tuple, Any, Union


class Table:
    def __init__(self, root: Tk, data: List[Tuple[Any, ...]]) -> None:
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


def show_table(
    header: Tuple[str, ...],
    lines: Union[List[Tuple[Any, ...]], int] = 0,
    title: Union[str, int] = 0,
) -> None:
    if title == 0:
        display_title = "Showing data of purchased items"
    else:
        display_title = str(title)

    tab: List[Tuple[Any, ...]] = [header]

    if lines != 0 and isinstance(lines, list):
        tab = tab + lines
    root: Tk = Tk()
    root.title(display_title)
    # Check if data exists before creating the table
    if len(tab) > 1 or (len(tab) == 1 and tab[0]):
        _ = Table(root, tab)
    else:
        # Display a message if no data is available
        import tkinter.messagebox as mb

        mb.showinfo("No Data", "No data to display in the table.")
    root.mainloop()
