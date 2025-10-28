import streamlit as st

# -----------------------------
# Safe CPU Simulator Class
# -----------------------------
class CPUSimulator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.registers = [0] * 6
        self.memory = [10] * 6
        self.pc = 0  # Program Counter

    def validate_reg(self, reg_str):
        """Ensure register format like $0–$5"""
        if not reg_str.startswith("$") or len(reg_str) != 2 or not reg_str[1].isdigit():
            raise ValueError(f"Invalid register format: {reg_str}")
        idx = int(reg_str[1])
        if not 0 <= idx < 6:
            raise ValueError(f"Register index out of range: {reg_str}")
        return idx

    def validate_addr(self, addr_str):
        """Ensure memory address within 0–5"""
        if not addr_str.isdigit():
            raise ValueError(f"Invalid memory address: {addr_str}")
        addr = int(addr_str)
        if not 0 <= addr < 6:
            raise ValueError(f"Memory address out of range: {addr}")
        return addr

    def step(self, instructions):
        """Execute one instruction safely"""
        if self.pc >= len(instructions):
            return False, "✅ Program completed."

        line = instructions[self.pc].strip()
        self.pc += 1

        if not line:  # skip blank
            return True, "Skipped empty line."

        line = line.lower()  # case-insensitive
        if line == "end":
            return False, "✅ END reached. Execution stopped."

        parts = line.replace(',', ' ').split()
        if not parts:
            return True, "Skipped empty line."

        opcode = parts[0]

        try:
            # ADD ------------------------------------------------------
            if opcode == "add":
                if len(parts) != 4:
                    raise ValueError("ADD requires 3 operands: add $d, $s1, $s2")
                rd = self.validate_reg(parts[1])
                rs1 = self.validate_reg(parts[2])
                rs2 = self.validate_reg(parts[3])
                self.registers[rd] = self.registers[rs1] + self.registers[rs2]
                return True, f"✅ {line.upper()} executed successfully."

            # SUB ------------------------------------------------------
            elif opcode == "sub":
                if len(parts) != 4:
                    raise ValueError("SUB requires 3 operands: sub $d, $s1, $s2")
                rd = self.validate_reg(parts[1])
                rs1 = self.validate_reg(parts[2])
                rs2 = self.validate_reg(parts[3])
                self.registers[rd] = self.registers[rs1] - self.registers[rs2]
                return True, f"✅ {line.upper()} executed successfully."

            # LOAD ------------------------------------------------------
            elif opcode == "load":
                if len(parts) != 3:
                    raise ValueError("LOAD requires 2 operands: load $d, addr")
                rd = self.validate_reg(parts[1])
                addr = self.validate_addr(parts[2])
                self.registers[rd] = self.memory[addr]
                return True, f"✅ Loaded memory[{addr}] into {parts[1]}."

            # STORE ------------------------------------------------------
            elif opcode == "store":
                if len(parts) != 3:
                    raise ValueError("STORE requires 2 operands: store $s, addr")
                rs = self.validate_reg(parts[1])
                addr = self.validate_addr(parts[2])
                self.memory[addr] = self.registers[rs]
                return True, f"✅ Stored {parts[1]} into memory[{addr}]."

            else:
                raise ValueError(f"Unknown instruction: '{opcode}'")

        except Exception as e:
            return True, f"❌ Error: {e}"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="DFCA CPU Simulator", layout="centered")
st.title("💻 DFCA CPU Simulator — Safe & Step-by-Step")

st.markdown("""
This simulator safely mimics a **6-register CPU** (Registers $0–$5) with **6 memory cells** (0–5).  
It supports instructions: `add`, `sub`, `load`, `store`, and ends on `END`.  
You can step through each instruction safely.
""")

# Initialize session state
if "cpu" not in st.session_state:
    st.session_state.cpu = CPUSimulator()
if "program" not in st.session_state:
    st.session_state.program = []
if "status" not in st.session_state:
    st.session_state.status = "🟢 Ready to load program."

# Program input area
st.subheader("🧾 Program Input")
program_input = st.text_area(
    "Enter your assembly program:",
    height=200,
    placeholder="Example:\nload $0 , 0\nload $1 , 1\nadd $2 , $0 , $1\nsub $3 , $2 , $0\nEND"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 Load Program"):
        st.session_state.program = program_input.strip().splitlines()
        st.session_state.cpu.reset()
        st.session_state.status = "✅ Program loaded successfully."

with col2:
    if st.button("⏭ Next Step"):
        if not st.session_state.program:
            st.warning("⚠ Load a program first!")
        else:
            cont, msg = st.session_state.cpu.step(st.session_state.program)
            st.session_state.status = msg
            if not cont:
                st.success("🏁 Program execution complete.")

with col3:
    if st.button("🔄 Reset"):
        st.session_state.cpu.reset()
        st.session_state.program = []
        st.session_state.status = "🔁 CPU and memory reset."

# Display current CPU status
st.info(st.session_state.status)

# Display current CPU state
st.subheader("📊 CPU State")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Registers:**")
    reg_data = {f"$ {i}": st.session_state.cpu.registers[i] for i in range(6)}
    st.table(reg_data)

with col2:
    st.markdown("**Memory:**")
    mem_data = {f"Addr {i}": st.session_state.cpu.memory[i] for i in range(6)}
    st.table(mem_data)

# Footer
st.markdown("---")
st.caption("✅ DFCA Python Lab — Robust Streamlit CPU Simulator ")
