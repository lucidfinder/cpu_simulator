import tkinter as tk
from tkinter import messagebox, scrolledtext

# CPU Simulator Logic
class CPUSimulator:
    def __init__(self):
        self.registers = [0] * 6
        self.memory = [10] * 6

    def execute(self, program_lines):
        self.registers = [0] * 6
        self.memory = [10] * 6

        for line in program_lines:
            line = line.strip()
            if not line or line == "END":
                continue

            parts = line.replace(",", "").split()
            opcode = parts[0]

            try:
                if opcode == "add":
                    rd, rs1, rs2 = int(parts[1][1]), int(parts[2][1]), int(parts[3][1])
                    self.registers[rd] = self.registers[rs1] + self.registers[rs2]

                elif opcode == "sub":
                    rd, rs1, rs2 = int(parts[1][1]), int(parts[2][1]), int(parts[3][1])
                    self.registers[rd] = self.registers[rs1] - self.registers[rs2]

                elif opcode == "load":
                    rd, mem_addr = int(parts[1][1]), int(parts[2])
                    self.registers[rd] = self.memory[mem_addr]

                elif opcode == "store":
                    rs, mem_addr = int(parts[1][1]), int(parts[2])
                    self.memory[mem_addr] = self.registers[rs]
            except Exception as e:
                raise ValueError(f"Invalid instruction: '{line}'")

        return self.registers, self.memory


# GUI Application
class CPUSimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple CPU Simulator")
        self.root.geometry("700x500")
        self.root.config(bg="#e6f0ff")

        self.cpu = CPUSimulator()

        # Title Label
        tk.Label(root, text="DFCA Python CPU Simulator",
                 font=("Arial", 18, "bold"), bg="#004080", fg="white", pady=10).pack(fill=tk.X)

        # Instruction Input
        tk.Label(root, text="Enter Instructions (max 6):",
                 font=("Arial", 12, "bold"), bg="#e6f0ff").pack(anchor="w", padx=15, pady=(10, 0))
        self.text_area = scrolledtext.ScrolledText(root, width=60, height=10, font=("Courier", 12))
        self.text_area.pack(padx=15, pady=10)

        # Buttons
        button_frame = tk.Frame(root, bg="#e6f0ff")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Run Program", font=("Arial", 12, "bold"),
                  bg="#0073e6", fg="white", command=self.run_program).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Clear", font=("Arial", 12, "bold"),
                  bg="#ff4d4d", fg="white", command=self.clear_text).grid(row=0, column=1, padx=10)

        # Output
        tk.Label(root, text="Output:", font=("Arial", 12, "bold"), bg="#e6f0ff").pack(anchor="w", padx=15)
        self.output_box = tk.Text(root, height=6, width=60, font=("Courier", 12), bg="#f5faff")
        self.output_box.pack(padx=15, pady=5)

    def run_program(self):
        program = self.text_area.get("1.0", tk.END).strip().splitlines()
        if not program or "END" not in program:
            messagebox.showerror("Error", "Program must end with 'END'")
            return

        try:
            registers, memory = self.cpu.execute(program)
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, f"Register File : {', '.join(map(str, registers))}\n")
            self.output_box.insert(tk.END, f"Memory : {', '.join(map(str, memory))}\n")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSimulatorUI(root)
    root.mainloop()
