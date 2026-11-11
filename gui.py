"""Tkinter desktop interface for Real Estate Price Predictor."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
from pathlib import Path
from main import load_dataset, train_model, predict_price, format_price, FEATURES

BASE = Path(__file__).resolve().parent

class PredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Price Predictor | Group 9")
        self.root.geometry("900x650")
        self.root.minsize(760, 580)
        self.model = None
        self.metrics = {}
        self.history = []
        self._style()
        self._build()
        self._train()

    def _style(self):
        self.root.configure(bg="#eef2f7")
        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("TLabel", background="#eef2f7", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground="#15345b")
        style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#53657d")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Accent.TButton", background="#1769aa", foreground="white")
        style.configure("Card.TLabelframe", background="white", padding=15)
        style.configure("Card.TLabelframe.Label", background="white", foreground="#15345b",
                        font=("Segoe UI", 11, "bold"))

    def _build(self):
        header = tk.Frame(self.root, bg="#15345b", padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="REAL ESTATE PRICE PREDICTOR", bg="#15345b",
                 fg="white", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(header, text="Machine learning based property price estimation • Group 9",
                 bg="#15345b", fg="#d8e8f8", font=("Segoe UI", 10)).pack(anchor="w", pady=(4,0))

        content = ttk.Frame(self.root, padding=20)
        content.pack(fill="both", expand=True)
        left = ttk.LabelFrame(content, text="Property details", style="Card.TLabelframe")
        left.pack(side="left", fill="y", padx=(0,14))
        right = ttk.Frame(content)
        right.pack(side="left", fill="both", expand=True)

        self.vars = {
            "area_sqft": tk.StringVar(value="1200"),
            "bedrooms": tk.StringVar(value="3"),
            "bathrooms": tk.StringVar(value="2"),
            "age_years": tk.StringVar(value="5"),
            "floor": tk.StringVar(value="4"),
            "parking": tk.StringVar(value="1"),
            "location": tk.StringVar(value="Kolkata")
        }
        fields = [
            ("Area (sq. ft.)", "area_sqft"), ("Bedrooms", "bedrooms"),
            ("Bathrooms", "bathrooms"), ("Property age (years)", "age_years"),
            ("Floor number", "floor"), ("Parking spaces", "parking")
        ]
        for label, key in fields:
            ttk.Label(left, text=label).pack(anchor="w", pady=(8,2))
            ttk.Entry(left, textvariable=self.vars[key], width=27).pack(fill="x")
        ttk.Label(left, text="Location").pack(anchor="w", pady=(8,2))
        ttk.Combobox(left, textvariable=self.vars["location"],
                     values=["Kolkata","Howrah","Salt Lake","New Town","Bardhaman","Durgapur"],
                     state="readonly", width=24).pack(fill="x")
        ttk.Button(left, text="Predict property price", style="Accent.TButton",
                   command=self._predict).pack(fill="x", pady=(18,7))
        ttk.Button(left, text="Clear fields", command=self._clear).pack(fill="x")

        result = ttk.LabelFrame(right, text="Prediction result", style="Card.TLabelframe")
        result.pack(fill="x")
        self.price_label = tk.Label(result, text="₹ —", bg="white", fg="#1769aa",
                                    font=("Segoe UI", 27, "bold"))
        self.price_label.pack(anchor="w", pady=(6,2))
        self.status_label = tk.Label(result, text="Enter property details and select Predict.",
                                     bg="white", fg="#53657d", font=("Segoe UI", 10))
        self.status_label.pack(anchor="w")
        self.model_label = tk.Label(result, text="Preparing model...", bg="white",
                                    fg="#53657d", font=("Segoe UI", 9))
        self.model_label.pack(anchor="w", pady=(8,0))

        hist = ttk.LabelFrame(right, text="Recent prediction history", style="Card.TLabelframe")
        hist.pack(fill="both", expand=True, pady=(14,0))
        columns = ("time","location","area","price")
        self.tree = ttk.Treeview(hist, columns=columns, show="headings", height=9)
        for col, title, width in [
            ("time","Time",125),("location","Location",110),
            ("area","Area (sq.ft.)",105),("price","Estimated price",150)]:
            self.tree.heading(col, text=title); self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)
        ttk.Button(hist, text="Export history to CSV", command=self._export).pack(anchor="e", pady=(10,0))

        footer = tk.Label(self.root, text="Academic project • Python for Machine Learning • Group 9",
                          bg="#eef2f7", fg="#6b7b90", font=("Segoe UI", 9), pady=8)
        footer.pack(fill="x")

    def _train(self):
        try:
            rows = load_dataset()
            self.model, self.metrics, method = train_model(rows)
            self.model_label.config(text=f"Model: {method}  |  Dataset: {len(rows)} properties")
        except Exception as exc:
            self.model_label.config(text=f"Model unavailable: {exc}")

    def _predict(self):
        try:
            data = {
                "area_sqft": float(self.vars["area_sqft"].get()),
                "bedrooms": int(self.vars["bedrooms"].get()),
                "bathrooms": int(self.vars["bathrooms"].get()),
                "age_years": int(self.vars["age_years"].get()),
                "floor": int(self.vars["floor"].get()),
                "parking": int(self.vars["parking"].get()),
                "location": self.vars["location"].get()
            }
            price, method = predict_price(data, self.model)
            formatted = format_price(price)
            self.price_label.config(text=formatted)
            self.status_label.config(text=f"Estimated market value using {method}. This is an academic estimate.")
            stamp = datetime.now().strftime("%H:%M:%S")
            record = {"time":stamp, "location":data["location"], "area":data["area_sqft"],
                      "price_lakh":price, "formatted":formatted}
            self.history.append(record)
            self.tree.insert("", "end", values=(stamp, data["location"], data["area_sqft"], formatted))
        except (ValueError, KeyError) as exc:
            messagebox.showerror("Invalid input", f"Please check the property details.\n{exc}")
        except Exception as exc:
            messagebox.showerror("Prediction error", str(exc))

    def _clear(self):
        defaults = {"area_sqft":"1200","bedrooms":"3","bathrooms":"2",
                    "age_years":"5","floor":"4","parking":"1","location":"Kolkata"}
        for key, value in defaults.items(): self.vars[key].set(value)
        self.price_label.config(text="₹ —")
        self.status_label.config(text="Enter property details and select Predict.")

    def _export(self):
        if not self.history:
            messagebox.showinfo("No history", "Make at least one prediction before exporting.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                    filetypes=[("CSV files","*.csv")], initialfile="prediction_history.csv")
        if not path: return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["time","location","area","price_lakh","formatted"])
            writer.writeheader(); writer.writerows(self.history)
        messagebox.showinfo("Export complete", f"History saved to:\n{path}")

if __name__ == "__main__":
    root = tk.Tk()
    PredictorApp(root)
    root.mainloop()
