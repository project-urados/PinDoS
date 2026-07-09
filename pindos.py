#!/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

SCRIPT = "core/pindos-start.py"
ENTRY = "#3c3f41"


class PindosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pindos Launcher")
        self.root.geometry("450x350")
        self.root.resizable(True, True)
        style = ttk.Style()

        style = ttk.Style()
        style.theme_use("clam")

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill="both", expand=True)

        self.output = tk.Text(
            frame,
            bg="#212121",
            fg="#ababab",
            insertbackground="white",
            font=("Consolas", 10),
            wrap="word"
        )

        style.configure(
            ".",
            background="#121212",
            foreground="#ababab",
            fieldbackground=ENTRY,
            font=("Segoe UI", 10)
        )

        ttk.Label(frame, text="Server IP").grid(row=0, column=0, sticky="w")
        self.server_ip = ttk.Entry(frame, width=30)
        self.server_ip.grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="Server Port").grid(row=1, column=0, sticky="w")
        self.server_port = ttk.Entry(frame, width=30)
        self.server_port.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Message").grid(row=2, column=0, sticky="w")
        self.message = ttk.Entry(frame, width=30)
        self.message.grid(row=2, column=1, pady=4)

        ttk.Label(frame, text="Count").grid(row=3, column=0, sticky="w")
        self.count = ttk.Entry(frame, width=30)
        self.count.grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="Processes").grid(row=4, column=0, sticky="w")
        self.processes = ttk.Entry(frame, width=30)
        self.processes.grid(row=4, column=1, pady=4)

        self.kill_enabled = tk.BooleanVar()

        ttk.Checkbutton(
            frame,
            text="Enable --kill",
            variable=self.kill_enabled
        ).grid(row=5, column=0, sticky="w")

        self.kill = ttk.Entry(frame, width=30)
        self.kill.grid(row=5, column=1, pady=4)
        
        ttk.Button(
            frame,
            text="Run",
            command=self.run_script
        ).grid(row=6, column=0, pady=15)

        ttk.Button(
            frame,
            text="Exit",
            command=root.destroy
        ).grid(row=6, column=1, pady=15)

        self.output = tk.Text(frame, height=8, width=50)
        self.output.grid(row=7, column=0, columnspan=2)

    def run_script(self):
        if not os.path.exists(SCRIPT):
            messagebox.showerror("Error", f"{SCRIPT} not found.")
            return

        cmd = ["python3", SCRIPT]

        if self.server_ip.get():
            cmd += ["--server-ip", self.server_ip.get()]

        if self.server_port.get():
            cmd += ["--server-port", self.server_port.get()]

        if self.message.get():
            cmd += ["--message", self.message.get()]

        if self.count.get():
            cmd += ["--count", self.count.get()]

        if self.processes.get():
            cmd += ["--processes", self.processes.get()]

        if self.kill_enabled.get():
            cmd.append("--kill")

            pid = self.kill.get().strip()
            if pid:
                cmd.append(pid)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, result.stdout)

            if result.stderr:
                self.output.insert(tk.END, "\n--- Errors ---\n")
                self.output.insert(tk.END, result.stderr)

        except Exception as e:
            messagebox.showerror("Error", str(e))


root = tk.Tk()
app = PindosGUI(root)
root.mainloop()