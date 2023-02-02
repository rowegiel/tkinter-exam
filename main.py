from tkinter import Tk, Button, Frame, Label, filedialog
import time, csv, sys


class CSVReader(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.frame = Frame(self)
        self.frame.configure(width=100, height=100)
        self.frame.pack(fill="both", expand=False)
        self.file_label = Label(self, text="Choose File")
        self.select_file = Button(self, text="Browse", command=self.browse_files)
        self.execute = Button(self, text="Execute", command=self.execute)
        self.file_label.pack(in_=self.frame)
        self.select_file.pack(in_=self.frame)
        self.execute.pack(in_=self.frame)

    def browse_files(self):
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*")),
        )
        # Change label contents
        self.file_label.configure(text=filename, fg="white")

    def analyze_file(self, data, card_type={}):
        if len(data) > 0:
            current_row = data.pop(0)
            if len(current_row) > 0:
                try:
                    if "Credit Card Type" in current_row:
                        return self.analyze_file(data, card_type)
                    else:
                        credit_card_type = current_row[1]
                        amount = float(current_row[4])
                        current_total = card_type.get("credit_card_total", 0)
                        if credit_card_type in card_type:
                            current_amount = card_type.get(credit_card_type, 0)
                            card_type.update()
                            card_type[credit_card_type] = current_amount + amount
                        else:
                            card_type.update({credit_card_type: amount})
                        card_type["credit_card_total"] = current_total + amount
                        return self.analyze_file(data, card_type)
                except RecursionError:
                    # catch recursion limit error and add current recursion limit by the default number.
                    current_recursion_limit = sys.getrecursionlimit()
                    current_recursion_limit += 1000  # default recursion limit
                    sys.setrecursionlimit(current_recursion_limit)
                    current_row = data.pop(0)
                    if "Credit Card Type" in current_row:
                        return self.analyze_file(data, card_type)
                    else:
                        credit_card_type = current_row[1]
                        amount = float(current_row[4])
                        current_total = card_type.get("credit_card_total", 0)
                        if credit_card_type in card_type:
                            current_amount = card_type.get(credit_card_type, 0)
                            card_type.update()
                            card_type[credit_card_type] = current_amount + amount
                        else:
                            card_type.update({credit_card_type: amount})
                        card_type["credit_card_total"] = current_total + amount
                        return self.analyze_file(data, card_type)
            else:
                return self.analyze_file(data, card_type)
        else:
            return card_type

    def execute(self):
        file = self.file_label.cget("text")
        if file == "Choose File":
            self.file_label.configure(text="Please select a file.", fg="red")
        else:
            try:
                with open(file, "r") as content:
                    csvreader = csv.reader(content)
                    # convert csv reader to list
                    data_list = list(csvreader)
                    credit_card_report = self.analyze_file(data_list, card_type={})
                    self.file_label.update_idletasks()
                    self.write_to_file(credit_card_report)
            except FileNotFoundError:
                # catch file not found error
                self.file_label.configure(text="Please select a file.", fg="red")

    def write_to_file(self, data):
        time.sleep(2)
        credit_card_total = data.pop("credit_card_total", None)
        with open("credit_card.txt", "w") as f:
            f.writelines(["Credit Card Type ", "Cumulative Amount ", "Percentage\n"])
            for key, value in data.items():
                percentage = (value / credit_card_total) * 100 if credit_card_total else 0
                f.writelines([f"{key} ", f"{round(value, 2)} ", f"{round(percentage, 2)}% \n"])
            f.close()
        self.file_label.configure(text="Report Generation Done...", fg="green")


def main():
    app = CSVReader()
    app.eval("tk::PlaceWindow . center")
    app.mainloop()
    return 0


if __name__ == "__main__":
    main()
