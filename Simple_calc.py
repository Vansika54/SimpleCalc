import tkinter as tk

class SimpleCalc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")
        self.resizable(False, False)

        # State
        self.total = None           # running total (None until first number entered)
        self.current = ""           # current number being typed (string of digits)
        self.operator = None        # current operator: '+', '-', '*', '/'

        # Display
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(self, textvariable=self.display_var, font=("Arial", 24),
                           justify="right", bd=10, relief="sunken", state="readonly",
                           readonlybackground="white")
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=6, pady=6)

        # Buttons layout
        btn_text = [
            ("7","8","9","/"),
            ("4","5","6","*"),
            ("1","2","3","-"),
            ("0","C","=","+"),
        ]

        for r, row in enumerate(btn_text, start=1):
            for c, label in enumerate(row):
                action = (lambda v=label: self.on_button(v))
                b = tk.Button(self, text=label, width=5, height=2, font=("Arial", 18),
                              command=action)
                b.grid(row=r, column=c, padx=4, pady=4)

    def on_button(self, label):
        if label.isdigit():            # digit pressed
            # append digit to current number (no leading zeros handling)
            if self.current == "0":
                self.current = label
            else:
                self.current += label
            self.display_var.set(self.current)
        elif label in {"+", "-", "*", "/"}:
            self._set_operator(label)
        elif label == "=":
            self._calculate_result()
        elif label == "C":
            self._clear_all()

    def _set_operator(self, op):
        # If there is a current number, push it into total
        if self.current != "":
            if self.total is None:
                # first number entered
                self.total = int(self.current)
            else:
                # compute running total with previous operator
                self.total = self._apply(self.total, int(self.current), self.operator)
            self.current = ""
            self.display_var.set(str(self.total))
        # set (or change) operator
        self.operator = op

    def _calculate_result(self):
        if self.operator is None or self.current == "" or self.total is None:
            return  # nothing to compute
        try:
            right = int(self.current)
            result = self._apply(self.total, right, self.operator)
        except ZeroDivisionError:
            self.display_var.set("Error: Div0")
            self.total = None
            self.current = ""
            self.operator = None
            return

        # show result (if whole number, show as int)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        self.display_var.set(str(result))
        # prepare for chained calculations: result becomes new total
        self.total = result
        self.current = ""
        self.operator = None

    def _apply(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            if b == 0:
                raise ZeroDivisionError
            return a / b
        return b

    def _clear_all(self):
        self.total = None
        self.current = ""
        self.operator = None
        self.display_var.set("0")

if __name__ == "__main__":
    app = SimpleCalc()
    app.mainloop()
