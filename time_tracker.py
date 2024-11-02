
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from datetime import datetime, timedelta
import os

# Check and install required libraries
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import("pandas")
install_and_import("openpyxl")

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        self.root.geometry("300x450")
        self.root.configure(bg="#F0F0F0")

        self.current_project = None
        self.current_rate = None
        self.start_time = None
        self.is_tracking = False
        self.excel_file = "time_tracking.xlsx"
        
        # Initialize total time and rate per minute
        self.total_time = timedelta()
        self.rate_per_minute = 0
        
        # Create Excel file if it doesn't exist
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=['Proyecto', 'Fecha', 'Hora_Inicio', 'Hora_Fin', 'Duración_Minutos', 'Tarifa'])
            df.to_excel(self.excel_file, index=False)
        
        self.setup_ui()
        self.load_projects_and_rates()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="TIME TRACKER", font=("Helvetica", 16), bg="#F0F0F0")
        title_label.pack(pady=10)

        # Start/Stop Button as a large circular button
        self.start_button = tk.Button(self.root, text="START", font=("Helvetica", 16), bg="green", fg="white", width=10, height=2, command=self.toggle_tracking)
        self.start_button.pack(pady=10)
        
        # Timer Label for the current session
        self.timer_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 24), bg="#F0F0F0")
        self.timer_label.pack(pady=10)

        # Project selection section
        project_frame = tk.Frame(self.root, bg="#F0F0F0")
        project_frame.pack(pady=5, fill="x")
        
        project_label = tk.Label(project_frame, text="Proyecto", bg="#F0F0F0")
        project_label.grid(row=0, column=0, padx=(10, 5))
        self.project_var = tk.StringVar()
        self.project_combo = ttk.Combobox(project_frame, textvariable=self.project_var, state="readonly", width=15)
        self.project_combo.grid(row=0, column=1, padx=(5, 10))
        
        self.add_project_button = tk.Button(project_frame, text="+", command=self.add_project, width=2, bg="#F0F0F0", relief="flat")
        self.add_project_button.grid(row=0, column=2, padx=(0, 10))
        
        # Rate selection section
        rate_frame = tk.Frame(self.root, bg="#F0F0F0")
        rate_frame.pack(pady=5, fill="x")
        
        rate_label = tk.Label(rate_frame, text="Tarifa", bg="#F0F0F0")
        rate_label.grid(row=0, column=0, padx=(10, 5))
        self.rate_var = tk.StringVar()
        self.rate_combo = ttk.Combobox(rate_frame, textvariable=self.rate_var, state="readonly", width=15)
        self.rate_combo.grid(row=0, column=1, padx=(5, 10))
        
        self.add_rate_button = tk.Button(rate_frame, text="+", command=self.add_rate, width=2, bg="#F0F0F0", relief="flat")
        self.add_rate_button.grid(row=0, column=2, padx=(0, 10))
        
        # Total Project Time display
        self.total_time_label = tk.Label(self.root, text="Tiempo total del proyecto: 00:00:00", bg="#F0F0F0", font=("Helvetica", 12))
        self.total_time_label.pack(pady=10)
        
        # Amount to Bill display
        self.bill_label = tk.Label(self.root, text="Importe a facturar: €0.00", bg="#F0F0F0", font=("Helvetica", 12))
        self.bill_label.pack(pady=10)
        
    def load_projects_and_rates(self):
        try:
            df = pd.read_excel(self.excel_file)
            projects = sorted(df['Proyecto'].unique())
            rates = sorted(df['Tarifa'].unique())

            self.project_combo['values'] = projects
            self.rate_combo['values'] = rates
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar proyectos y tarifas: {str(e)}")

    def add_project(self):
        project_name = simpledialog.askstring("Nuevo Proyecto", "Introduce el nombre del proyecto:")
        if project_name:
            current_projects = list(self.project_combo['values'])
            if project_name not in current_projects:
                current_projects.append(project_name)
                self.project_combo['values'] = sorted(current_projects)

    def add_rate(self):
        rate_value = simpledialog.askinteger("Nueva Tarifa", "Introduce la tarifa (€) por 8 horas:")
        if rate_value:
            rate_per_minute = rate_value / 8 / 60  # Calculate rate per minute based on an 8-hour day
            self.rate_per_minute = rate_per_minute
            current_rates = list(self.rate_combo['values'])
            if rate_value not in current_rates:
                current_rates.append(rate_value)
                self.rate_combo['values'] = sorted(current_rates)

    def toggle_tracking(self):
        if not self.is_tracking:
            self.start_tracking()
        else:
            self.stop_tracking()

    def start_tracking(self):
        if not self.project_var.get() or not self.rate_var.get():
            messagebox.showwarning("Advertencia", "Por favor selecciona un proyecto y una tarifa.")
            return
        
        self.current_project = self.project_var.get()
        self.current_rate = float(self.rate_var.get())
        self.start_time = datetime.now()
        self.is_tracking = True
        self.start_button.config(text="STOP", bg="red")
        self.update_timer()

    def stop_tracking(self):
        if self.is_tracking and self.start_time:
            end_time = datetime.now()
            duration = end_time - self.start_time
            duration_minutes = int(duration.total_seconds() / 60)
            
            # Update total time and billing
            self.total_time += duration
            self.update_billing()

            # Save the session to Excel
            new_record = {
                'Proyecto': [self.current_project],
                'Fecha': [self.start_time.date()],
                'Hora_Inicio': [self.start_time.strftime('%H:%M:%S')],
                'Hora_Fin': [end_time.strftime('%H:%M:%S')],
                'Duración_Minutos': [duration_minutes],
                'Tarifa': [self.current_rate]
            }
            df = pd.read_excel(self.excel_file)
            df = pd.concat([df, pd.DataFrame(new_record)], ignore_index=True)
            df.to_excel(self.excel_file, index=False)
        
        self.is_tracking = False
        self.start_button.config(text="START", bg="green")
        self.timer_label.config(text="00:00:00")

    def update_timer(self):
        if self.is_tracking:
            elapsed = datetime.now() - self.start_time
            self.timer_label.config(text=str(elapsed).split('.')[0])
            self.root.after(1000, self.update_timer)

    def update_billing(self):
        # Calculate total time in minutes and update the bill
        total_minutes = self.total_time.total_seconds() / 60
        total_bill = total_minutes * self.rate_per_minute
        self.total_time_label.config(text=f"Tiempo total del proyecto: {self.total_time}")
        self.bill_label.config(text=f"Importe a facturar: €{total_bill:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
