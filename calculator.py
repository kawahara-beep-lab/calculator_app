import tkinter as tk


COLORS = {
    "bg": "#1e1e2e",
    "display_bg": "#181825",
    "num": "#313244",
    "num_hover": "#45475a",
    "op": "#89b4fa",
    "op_hover": "#b4d0fb",
    "eq": "#a6e3a1",
    "eq_hover": "#cef0cb",
    "clear": "#f38ba8",
    "clear_hover": "#f7b8c8",
    "text": "#cdd6f4",
    "text_dark": "#1e1e2e",
    "sub_text": "#6c7086",
}


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])

        self._expr = ""
        self._result_shown = False

        self._build_display()
        self._build_buttons()
        self._bind_keys()

    def _build_display(self):
        frame = tk.Frame(self, bg=COLORS["display_bg"], padx=16, pady=12)
        frame.pack(fill="x")

        self._sub_var = tk.StringVar(value="")
        tk.Label(
            frame, textvariable=self._sub_var,
            font=("Segoe UI", 12), bg=COLORS["display_bg"],
            fg=COLORS["sub_text"], anchor="e",
        ).pack(fill="x")

        self._main_var = tk.StringVar(value="0")
        tk.Label(
            frame, textvariable=self._main_var,
            font=("Segoe UI", 32, "bold"), bg=COLORS["display_bg"],
            fg=COLORS["text"], anchor="e",
        ).pack(fill="x")

    def _make_btn(self, parent, text, bg, hover, fg=COLORS["text"],
                  rowspan=1, colspan=1, cmd=None):
        btn = tk.Button(
            parent, text=text,
            font=("Segoe UI", 16, "bold"),
            bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            relief="flat", bd=0, cursor="hand2",
            command=cmd or (lambda t=text: self._on_button(t)),
        )
        btn.bind("<Enter>", lambda e, b=btn, c=hover: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg: b.config(bg=c))
        return btn

    def _build_buttons(self):
        frame = tk.Frame(self, bg=COLORS["bg"], padx=8, pady=8)
        frame.pack(fill="both", expand=True)

        layout = [
            [("C", "clear"), ("⌫", "op"), ("%", "op"), ("÷", "op")],
            [("7", "num"),   ("8", "num"), ("9", "num"), ("×", "op")],
            [("4", "num"),   ("5", "num"), ("6", "num"), ("−", "op")],
            [("1", "num"),   ("2", "num"), ("3", "num"), ("+", "op")],
            [("±", "op"),    ("0", "num"), (".", "num"), ("=", "eq")],
        ]

        style_map = {
            "num":   (COLORS["num"],   COLORS["num_hover"],   COLORS["text"]),
            "op":    (COLORS["op"],    COLORS["op_hover"],    COLORS["text_dark"]),
            "eq":    (COLORS["eq"],    COLORS["eq_hover"],    COLORS["text_dark"]),
            "clear": (COLORS["clear"], COLORS["clear_hover"], COLORS["text_dark"]),
        }

        for r, row in enumerate(layout):
            frame.rowconfigure(r, weight=1, minsize=64)
            for c, (label, style) in enumerate(row):
                frame.columnconfigure(c, weight=1, minsize=72)
                bg, hover, fg = style_map[style]
                btn = self._make_btn(frame, label, bg, hover, fg)
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

    def _bind_keys(self):
        mapping = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "plus": "+", "minus": "−", "asterisk": "×", "slash": "÷",
            "period": ".",
            "Return": "=", "KP_Enter": "=",
            "BackSpace": "⌫", "Escape": "C",
        }
        for key, label in mapping.items():
            self.bind(f"<{key}>", lambda e, l=label: self._on_button(l))
        self.bind("<equal>", lambda e: self._on_button("="))

    def _on_button(self, label):
        if label == "C":
            self._expr = ""
            self._result_shown = False
            self._main_var.set("0")
            self._sub_var.set("")

        elif label == "⌫":
            if self._result_shown:
                self._expr = ""
                self._result_shown = False
                self._main_var.set("0")
            else:
                self._expr = self._expr[:-1]
                self._main_var.set(self._expr or "0")

        elif label == "=":
            if not self._expr:
                return
            try:
                expr = (self._expr
                        .replace("×", "*")
                        .replace("÷", "/")
                        .replace("−", "-"))
                result = eval(expr)  # noqa: S307
                result = int(result) if isinstance(result, float) and result.is_integer() else round(result, 10)
                self._sub_var.set(self._expr + " =")
                self._main_var.set(str(result))
                self._expr = str(result)
                self._result_shown = True
            except ZeroDivisionError:
                self._main_var.set("Error")
                self._expr = ""
                self._result_shown = False
            except Exception:
                self._main_var.set("Error")
                self._expr = ""
                self._result_shown = False

        elif label == "±":
            if self._expr.startswith("-"):
                self._expr = self._expr[1:]
            elif self._expr:
                self._expr = "-" + self._expr
            self._main_var.set(self._expr or "0")

        elif label == "%":
            try:
                val = eval(self._expr.replace("×", "*").replace("÷", "/").replace("−", "-"))
                self._expr = str(val / 100)
                self._main_var.set(self._expr)
            except Exception:
                pass

        else:
            if self._result_shown and label not in ("+", "−", "×", "÷"):
                self._expr = ""
                self._sub_var.set("")
            self._result_shown = False
            self._expr += label
            self._main_var.set(self._expr)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
