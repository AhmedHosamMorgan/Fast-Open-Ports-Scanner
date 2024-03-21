import tkinter as tk
from tkinter import messagebox, ttk
import socket
import concurrent.futures

class PortScannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Open Ports Scanner")
        self.configure(background='#f0f0f0')
        self.create_widgets()
        self.scanning = False
        self.scanned_ports = []
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 500
        window_height = 550
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.geometry(f"500x600+{x_position}+{y_position}")
        self.minsize(500, 550)
        
    def create_developer_info(self, parent):
        developer_info_frame = tk.Frame(parent, bg='#f0f0f0')
        developer_info_frame.pack(side='bottom', fill='x', padx=10, pady=(10, 0))
        name_label = tk.Label(developer_info_frame, text="Developed by: Ahmed Hossam Morgan", bg='#f0f0f0', font=('Helvetica', 10))
        name_label.grid(row=0, column=0, sticky='w')
        email_label = tk.Label(developer_info_frame, text="Email: ahmedhossammorgan@gmail.com", bg='#f0f0f0', font=('Helvetica', 10))
        email_label.grid(row=1, column=0, sticky='w')        
        
    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=1, pady=1)
        self.create_title(main_frame)
        self.create_host_entry(main_frame)
        self.create_port_entries(main_frame)
        self.create_buttons(main_frame)
        self.create_progress_bar(main_frame)
        self.create_result_text(main_frame)
        self.create_developer_info(main_frame)
        
        
    def create_title(self, parent):
        title_label = tk.Label(parent, text="Open Ports Scanner", font=('Helvetica', 24, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 10), side='top', anchor='n')

    def create_host_entry(self, parent):
        host_frame = tk.Frame(parent, bg='#f0f0f0')
        host_frame.pack(fill='both', padx=1, pady=1)
        tk.Label(host_frame, text="Target Host:", bg='#f0f0f0', font=('Helvetica', 16)).pack(side='left')
        self.host_entry = tk.Entry(host_frame, font=('Helvetica', 16), width=20)
        self.host_entry.pack(side='left')

    def create_port_entries(self, parent):
        port_frame = tk.Frame(parent, bg='#f0f0f0')
        port_frame.pack(fill='both', padx=1, pady=1)

        tk.Label(port_frame, text="Start Port:   ", bg='#f0f0f0', font=('Helvetica', 16)).grid(row=0, column=0, sticky='w')
        self.start_port_entry = tk.Entry(port_frame, font=('Helvetica', 16), width=10)
        self.start_port_entry.grid(row=0, column=1, sticky='w')
        self.start_port_entry.insert(0, "1-65535")  # Insert the hint "1" as default value
        self.start_port_entry.bind("<FocusIn>", self.remove_start_hint)

        tk.Label(port_frame, text="End Port:", bg='#f0f0f0', font=('Helvetica', 16)).grid(row=1, column=0, sticky='w')
        self.end_port_entry = tk.Entry(port_frame, font=('Helvetica', 16), width=10)
        self.end_port_entry.grid(row=1, column=1, sticky='w')
        self.end_port_entry.insert(0, "1-65535")  # Insert the hint "65500" as default value
        self.end_port_entry.bind("<FocusIn>", self.remove_end_hint)

    def remove_start_hint(self, event):
        if self.start_port_entry.get() == "1-65535":
            self.start_port_entry.delete(0, tk.END)

    def remove_end_hint(self, event):
        if self.end_port_entry.get() == "1-65535":
            self.end_port_entry.delete(0, tk.END)    
    
    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill='both', padx=5, pady=5)
        self.scan_button = tk.Button(button_frame, text="Start Scan", command=self.start_scan, font=('Helvetica', 16, 'bold'), bg='#4CAF50', fg='white')
        self.scan_button.pack(side='left', padx=8)
        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_scan, font=('Helvetica', 16, 'bold'), bg='#FF5733', fg='white', state='disabled')
        self.stop_button.pack(side='left', padx=5)

    def create_progress_bar(self, parent):
        progress_frame = tk.Frame(parent, bg='#f0f0f0')
        progress_frame.pack(pady=10)
        self.progress_label = tk.Label(progress_frame, text="Scanning Progress:", bg='#f0f0f0', font=('Helvetica', 16))
        self.progress_label.pack(side='left')
        self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack(side='left')
        self.progress_percent = tk.Label(progress_frame, text="0%", bg='#f0f0f0', font=('Helvetica', 16))
        self.progress_percent.pack(side='left', padx=(10, 0))

    def create_result_text(self, parent):
        result_frame = tk.Frame(parent, bg='#f0f0f0')
        result_frame.pack(pady=1, fill='both', expand=True)
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, font=('Helvetica', 14), bg='#FFFFFF', width=9, height=9, padx=1, pady=1)
        self.result_text.pack(fill='both', expand=True)
        
    def start_scan(self):
        host = self.host_entry.get()
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())
        self.scan_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = end_port - start_port + 1
        self.scanning = True
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.futures = []
        self.result_text.delete(1.0, tk.END)

        for port in range(start_port, end_port + 1):
            future = self.executor.submit(self.scan_port, host, port)
            self.futures.append(future)
        self.after(100, self.check_thread)

    def stop_scan(self):
        self.scanning = False
        self.scan_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.executor.shutdown(wait=False)

    def check_thread(self):
        if any(future.running() for future in self.futures):
            self.after(100, self.check_thread)
        else:
            self.progress_bar["value"] = self.progress_bar["maximum"]
            if self.scanning:
                self.process_results()
            else:
                messagebox.showinfo("Scan Stopped", "Port scanning has been stopped.")

    def scan_port(self, host, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    service = socket.getservbyport(port)
                    return (port, service)
        except socket.error:
            pass

    def process_results(self):
        self.scanned_ports = [future.result() for future in self.futures if future.result()]
        if self.scanned_ports:
            open_ports_info = "\n".join([f"Port: {port}, {service}" for port, service in self.scanned_ports])
            self.result_text.insert(tk.END, f"Open ports:\n{open_ports_info}")
            with open("Port_Scan_Results.txt", "w") as file:
                file.write(open_ports_info)
        else:
            self.result_text.insert(tk.END, "No open ports found.")
        self.scan_button.config(state="normal")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    app = PortScannerGUI()
    app.mainloop()
