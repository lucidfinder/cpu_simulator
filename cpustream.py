import streamlit as st

# -----------------------------
# CPU Simulator Class
# -----------------------------
class CPUSimulator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.registers = [0] * 6
        self.memory = [10] * 6
        self.pc = 0  # program counter (current instruction index)

    def step(self, instructions):
        """Execute one instruction based on the current PC (program counter)"""
        if self.pc >= len(instructions):
            return False, "Program complete."

        line = instructions[self.pc].strip()
        self.pc += 1

        if not line or line.upper() == "END":
            return False, "END reached."

        parts = line.replace(',', '').split()
        opcode = parts[0]

        try:
            if opcode == "add":
                rd = int(parts[1][1])
                rs1 = int(parts[2][1])
                rs2 = int(parts[3][1])
                self.registers[rd] = self.registers[rs1] + self.registers[rs2]
                return True, f"Executed: {line}"

            elif opcode == "sub":
                rd = int(parts[1][1])
                rs1 = int(parts[2][1])
                rs2 = int(parts[3][1])
                self.registers[rd] = self.registers[rs1] - self.registers[rs2]
                return True, f"Executed: {line}"

            elif opcode == "load":
                rd = int(parts[1][1])
                mem_addr = int(parts[2])
                self.registers[rd] = self.memory[mem_addr]
                return True, f"Loaded memory[{mem_addr}] into {parts[1]}"

            elif opcode == "store":
                rs = int(parts[1][1])
                mem_addr = int(parts[2])
                self.memory[mem_addr] = self.registers[rs]
                return True, f"Stored {parts[1]} into memory[{mem_addr}]"

            else:
                return True, f"Unknown instruction: {line}"

        except Exception as e:
            return False, f"Error in '{line}': {e}"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="DFCA CPU Simulator", layout="centered")
st.title("💻 DFCA Python CPU Simulator — Step-by-Step")
st.markdown("""
Simulate a **simple CPU** with 6 registers and 6 memory slots.  
You can execute **one instruction at a time** using the "Next Step" button.
""")

# Initialize CPU state in session
if "cpu" not in st.session_state:
    st.session_state.cpu = CPUSimulator()
if "program" not in st.session_state:
    st.session_state.program = []
if "status" not in st.session_state:
    st.session_state.status = "Ready."

# Program Input Area
st.subheader("🧾 Enter Instructions")
program_input = st.text_area(
    "Assembly Instructions:",
    height=180,
    placeholder="Example:\nload $0 , 0\nload $1 , 1\nadd $2 , $0 , $1\nEND"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 Load Program"):
        st.session_state.program = program_input.strip().splitlines()
        st.session_state.cpu.reset()
        st.session_state.status = "Program loaded. Press 'Next Step' to start."

with col2:
    if st.button("⏭ Next Step"):
        if not st.session_state.program:
            st.warning("⚠ Load a program first.")
        else:
            cont, msg = st.session_state.cpu.step(st.session_state.program)
            st.session_state.status = msg
            if not cont:
                st.success("✅ Program execution completed.")

with col3:
    if st.button("🔄 Reset"):
        st.session_state.cpu.reset()
        st.session_state.program = []
        st.session_state.status = "Reset complete."

# Display Status
st.info(st.session_state.status)

# Display Current CPU State
st.subheader("📊 CPU State")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Registers ($0–$5):**")
    reg_data = {f"$ {i}": st.session_state.cpu.registers[i] for i in range(6)}
    st.table(reg_data)

with col2:
    st.markdown("**Memory (Addr 0–5):**")
    mem_data = {f"Addr {i}": st.session_state.cpu.memory[i] for i in range(6)}
    st.table(mem_data)

# Footer
st.markdown("---")
st.caption("✅ DFCA Python Lab Problem A — Interactive Step-by-Step Simulator")
