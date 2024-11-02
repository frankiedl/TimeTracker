# TimeTracker V.1.2.1 by Frankie De Leonardis

import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from datetime import datetime, timedelta
import os
import ctypes
import time
from ctypes import Structure, c_ulong, byref

# Check and install required libraries
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import("pandas")
install_and_import("openpyxl")

# Windows API structures and functions for last input detection
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_ulong),
        ('dwTime', c_ulong),
    ]

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        self.root.geometry("400x650")  # Increased height for currency selector
        self.root.configure(bg="#F0F0F0")

        # Currency configuration
        self.currencies = {
            "EUR": "€",
            "USD": "$",
            "GBP": "£",
            "JPY": "¥",
            "CNY": "元"
        }
        self.currency_symbol = "€"  # Default currency

        self.current_project = None
        self.current_rate = None
        self.start_time = None
        self.is_tracking = False
        self.excel_file = "time_tracking.xlsx"
        
        # Initialize total time and rate per minute
        self.total_time = timedelta()
        self.rate_per_minute = 0
        
        # Initialize inactivity tracking
        self.inactivity_threshold = 300  # 5 minutes in seconds
        self.last_activity_check = time.time()
        
        # Initialize last input info
        self.lastInputInfo = LASTINPUTINFO()
        self.lastInputInfo.cbSize = ctypes.sizeof(self.lastInputInfo)
        
        # Styles
        self.style = ttk.Style()
        self.style.configure('Section.TLabel', font=('Helvetica', 10), foreground='#666666')
        self.style.configure('Value.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Timer.TLabel', font=('Helvetica', 32, 'bold'))
        self.style.configure('Amount.TLabel', font=('Helvetica', 24, 'bold'))
        
        # Create Excel file if it doesn't exist
        if not os.path.exists(self.excel_file):
            # Create initial DataFrame with explicit dtypes
            df = pd.DataFrame({
                'Project': pd.Series(dtype='string'),
                'Date': pd.Series(dtype='datetime64[ns]'),
                'Start_Time': pd.Series(dtype='string'),
                'End_Time': pd.Series(dtype='string'),
                'Duration_Minutes': pd.Series(dtype='int64'),
                'Rate': pd.Series(dtype='float64'),
                'Currency': pd.Series(dtype='string')
            })
            df.to_excel(self.excel_file, index=False)
        
        self.setup_ui()
        self.load_projects_and_rates()
    
    def setup_ui(self):  # Note la indentación correcta aquí
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20 20 20 20")
        main_container.pack(fill=tk.BOTH, expand=True)
        ...
        
        # Start/Stop Button as a large circular button
        self.start_button = tk.Button(
            main_container, 
            text="START", 
            font=("Helvetica", 20, "bold"), 
            bg="#4CAF50",
            fg="white",
            width=12,
            height=2,
            command=self.toggle_tracking,
            relief="flat",
            bd=0
        )
        self.start_button.pack(pady=(0, 20))
        
        # Timer Label for the current session
        self.timer_label = ttk.Label(
            main_container,
            text="00:00:00",
            style='Timer.TLabel'
        )
        self.timer_label.pack(pady=(0, 30))

        # Project section
        project_frame = ttk.Frame(main_container)
        project_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            project_frame,
            text="Project",
            style='Section.TLabel'
        ).pack(anchor=tk.W)
        
        project_controls = ttk.Frame(project_frame)
        project_controls.pack(fill=tk.X)
        
        self.project_var = tk.StringVar()
        self.project_combo = ttk.Combobox(
            project_controls,
            textvariable=self.project_var,
            state="readonly",
            font=('Helvetica', 14)
        )
        self.project_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.add_project_button = ttk.Button(
            project_controls,
            text="+",
            width=3,
            command=self.add_project
        )
        self.add_project_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Rate section
        rate_frame = ttk.Frame(main_container)
        rate_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            rate_frame,
            text="Rate",
            style='Section.TLabel'
        ).pack(anchor=tk.W)
        
        rate_controls = ttk.Frame(rate_frame)
        rate_controls.pack(fill=tk.X)
        
        self.rate_var = tk.StringVar()
        self.rate_combo = ttk.Combobox(
            rate_controls,
            textvariable=self.rate_var,
            state="readonly",
            font=('Helvetica', 14)
        )
        self.rate_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.add_rate_button = ttk.Button(
            rate_controls,
            text="+",
            width=3,
            command=self.add_rate
        )
        self.add_rate_button.pack(side=tk.LEFT, padx=(5, 0))

        # Currency section
        currency_frame = ttk.Frame(main_container)
        currency_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            currency_frame,
            text="Currency",
            style='Section.TLabel'
        ).pack(anchor=tk.W)
        
        self.currency_var = tk.StringVar(value="EUR")
        self.currency_combo = ttk.Combobox(
            currency_frame,
            textvariable=self.currency_var,
            state="readonly",
            font=('Helvetica', 14),
            values=list(self.currencies.keys())
        )
        self.currency_combo.pack(fill=tk.X)
        self.currency_combo.bind('<<ComboboxSelected>>', self.on_currency_change)
        
        # Total Project Time section
        time_frame = ttk.Frame(main_container)
        time_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            time_frame,
            text="Total project time",
            style='Section.TLabel'
        ).pack(anchor=tk.W)
        
        self.total_time_label = ttk.Label(
            time_frame,
            text="00:00:00",
            style='Value.TLabel'
        )
        self.total_time_label.pack(anchor=tk.W)
        
        # Amount to Bill section
        bill_frame = ttk.Frame(main_container)
        bill_frame.pack(fill=tk.X)
        
        ttk.Label(
            bill_frame,
            text="Amount to bill",
            style='Section.TLabel'
        ).pack(anchor=tk.W)
        
        self.bill_label = ttk.Label(
            bill_frame,
            text=f"0.00 {self.currency_symbol}",
            style='Amount.TLabel'
        )
        self.bill_label.pack(anchor=tk.W)

        # Add bindings for project and rate selection
        self.project_combo.bind('<<ComboboxSelected>>', self.on_project_or_rate_change)
        self.rate_combo.bind('<<ComboboxSelected>>', self.on_project_or_rate_change)

    def get_last_input_time(self):
        """Get the last input time from Windows API"""
        ctypes.windll.user32.GetLastInputInfo(byref(self.lastInputInfo))
        last_input_time = self.lastInputInfo.dwTime
        current_time = ctypes.windll.kernel32.GetTickCount()
        return (current_time - last_input_time) / 1000  # Convert to seconds

    def check_activity(self):
        """Check for user activity and stop tracking if inactive"""
        if self.is_tracking:
            idle_time = self.get_last_input_time()
            # print(f"Idle time: {idle_time} seconds")  # Debug print
            if idle_time > self.inactivity_threshold:
                # User has been inactive for more than 5 minutes, stop tracking
                messagebox.showinfo(
                    "Inactivity Detected", 
                    "Tracking stopped due to 5 minutes of inactivity."
                )
                self.stop_tracking()
            else:
                # Continue checking activity
                self.root.after(1000, self.check_activity)

    def on_currency_change(self, event=None):
        """Handle currency change"""
        selected_currency = self.currency_var.get()
        self.currency_symbol = self.currencies[selected_currency]
        self.update_project_totals()

    def format_timer(self, td):
        """Format timedelta to show only two digits for seconds"""
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        seconds = int(td.total_seconds() % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def format_amount(self, amount):
        """Format amount with currency symbol"""
        currency = self.currency_var.get()
        if currency in ["CNY", "JPY"]:  # No decimal places for these currencies
            return f"{int(amount):,} {self.currency_symbol}"
        else:
            return f"{amount:,.2f} {self.currency_symbol}"

    def load_projects_and_rates(self):
        try:
            df = pd.read_excel(self.excel_file)
            projects = sorted(df['Project'].unique())
            rates = sorted(df['Rate'].unique())

            if len(projects) > 0:
                self.project_combo['values'] = projects
            if len(rates) > 0:
                self.rate_combo['values'] = rates

            # If there was a previous selection, update the totals
            if self.project_var.get() and self.rate_var.get():
                self.update_project_totals()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading projects and rates: {str(e)}")

    def on_project_or_rate_change(self, event=None):
        """Called when either project or rate selection changes"""
        self.update_project_totals()

    def update_project_totals(self):
        """Update total time and amount for the selected project and rate"""
        project = self.project_var.get()
        try:
            rate = float(self.rate_var.get())
        except (ValueError, TypeError):
            rate = 0

        if project and rate:
            try:
                df = pd.read_excel(self.excel_file)
                
                # Filter by project
                project_data = df[df['Project'] == project]
                
                if not project_data.empty:
                    # Calculate total minutes for the project and convert to Python int
                    total_minutes = int(project_data['Duration_Minutes'].sum())
                    self.total_time = timedelta(minutes=total_minutes)
                    
                    # Calculate rate per minute
                    self.rate_per_minute = rate / 8 / 60  # rate per 8-hour day converted to per minute
                    
                    # Update the displays
                    self.update_billing()
                else:
                    # New project, reset totals
                    self.total_time = timedelta()
                    self.rate_per_minute = rate / 8 / 60
                    self.update_billing()
            except Exception as e:
                messagebox.showerror("Error", f"Error updating totals: {str(e)}")

    def update_timer(self):
        if self.is_tracking:
            elapsed = datetime.now() - self.start_time
            self.timer_label.config(text=self.format_timer(elapsed))
            self.root.after(1000, self.update_timer)

    def update_billing(self):
        total_minutes = self.total_time.total_seconds() / 60
        total_bill = total_minutes * self.rate_per_minute
        self.total_time_label.config(text=self.format_timer(self.total_time))
        self.bill_label.config(text=self.format_amount(total_bill))

    def add_project(self):
        project_name = simpledialog.askstring("New Project", "Enter project name:")
        if project_name:
            if not project_name.strip():
                messagebox.showwarning("Warning", "Project name cannot be empty.")
                return
                
            current_projects = list(self.project_combo['values']) if self.project_combo['values'] else []
            
            if project_name not in current_projects:
                current_projects.append(project_name)
                self.project_combo['values'] = sorted(current_projects)
                self.project_var.set(project_name)
                self.update_project_totals()
            else:
                messagebox.showwarning("Warning", "This project already exists.")

    def add_rate(self):
        rate_value = simpledialog.askfloat("New Rate", f"Enter rate ({self.currency_symbol}) per 8 hours:")
        if rate_value:
            if rate_value <= 0:
                messagebox.showwarning("Warning", "Rate must be greater than zero.")
                return
                
            current_rates = list(self.rate_combo['values']) if self.rate_combo['values'] else []
            
            if rate_value not in current_rates:
                current_rates.append(rate_value)
                self.rate_combo['values'] = sorted(current_rates)
                self.rate_var.set(rate_value)
                self.rate_per_minute = rate_value / 8 / 60
                self.update_project_totals()
            else:
                messagebox.showwarning("Warning", "This rate already exists.")

    def toggle_tracking(self):
        if not self.is_tracking:
            self.start_tracking()
        else:
            self.stop_tracking()

    def start_tracking(self):
        if not self.project_var.get() or not self.rate_var.get():
            messagebox.showwarning("Warning", "Please select a project and rate.")
            return
        
        self.current_project = self.project_var.get()
        self.current_rate = float(self.rate_var.get())
        self.start_time = datetime.now()
        self.is_tracking = True
        self.start_button.config(text="STOP", bg="#f44336")
        self.update_timer()
        
        # Start activity checking immediately
        self.check_activity()
        
        # Disable project and rate selection while tracking
        self.project_combo.config(state="disabled")
        self.rate_combo.config(state="disabled")
        self.currency_combo.config(state="disabled")
        self.add_project_button.config(state="disabled")
        self.add_rate_button.config(state="disabled")

    def stop_tracking(self):
        if self.is_tracking and self.start_time:
            end_time = datetime.now()
            duration = end_time - self.start_time
            duration_minutes = int(duration.total_seconds() / 60)
            
            # Create new record as DataFrame directly with explicit dtypes
            new_record = pd.DataFrame({
                'Project': [self.current_project],
                'Date': [self.start_time.date()],
                'Start_Time': [self.start_time.strftime('%H:%M:%S')],
                'End_Time': [end_time.strftime('%H:%M:%S')],
                'Duration_Minutes': [duration_minutes],
                'Rate': [self.current_rate],
                'Currency': [self.currency_var.get()]
            })

            # Read existing data
            df = pd.read_excel(self.excel_file)
            
            # Ensure both DataFrames have the same column types
            for col in df.columns:
                new_record[col] = new_record[col].astype(df[col].dtype)
            
            # Concatenate and save
            df = pd.concat([df, new_record], ignore_index=True)
            df.to_excel(self.excel_file, index=False)
            
            # Update the total time and billing
            self.update_project_totals()
        
        self.is_tracking = False
        self.start_button.config(text="START", bg="#4CAF50")
        self.timer_label.config(text="00:00:00")
        
        # Re-enable project, rate and currency selection
        self.project_combo.config(state="readonly")
        self.rate_combo.config(state="readonly")
        self.currency_combo.config(state="readonly")
        self.add_project_button.config(state="normal")
        self.add_rate_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
