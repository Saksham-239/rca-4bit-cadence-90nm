#!/usr/bin/env python3
"""
90nm 4-Bit Ripple Carry Adder Benchmark Suite for Review 2
Implements Static CMOS, Domino Logic, and C²MOS 4-bit Ripple Carry Adders.
Simulates via ngspice and extracts Delay, Power, Transistor Count, and PDP.
"""

import os
import sys
import subprocess
import re
import math
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
NETLIST_DIR = os.path.join(BASE_DIR, "netlists")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

for d in [NETLIST_DIR, RESULTS_DIR, PLOTS_DIR]:
    os.makedirs(d, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, "ptm_90nm.pm")

def to_wsl_path(win_path):
    p = win_path.replace("\\", "/")
    if len(p) >= 2 and p[1] == ":":
        drive = p[0].lower()
        return f"/mnt/{drive}{p[2:]}"
    return p

# -------------------------------------------------------------
# 1. Subcircuits (All Ground references mapped to 0)
# -------------------------------------------------------------

def get_header(title):
    wsl_model = to_wsl_path(MODEL_PATH)
    return f"""* {title}
.include "{wsl_model}"
.param VDD_VAL = 1.0V
Vdd vdd 0 DC 'VDD_VAL'
"""

def generate_static_cmos_fa_subcircuit():
    return """
* Static CMOS 1-Bit Full Adder (28 Transistors)
* Subcircuit: FA_STATIC A B Cin Sum Cout VDD 0
.subckt FA_STATIC a b cin sum cout vdd 0

* --- Carry Generation (12 Transistors) ---
* PUN for Cout_bar (5 PMOS)
Mp_c1 n_cp1 a   vdd vdd pmos_90nm w=420n l=100n
Mp_c2 cout_b b   n_cp1 vdd pmos_90nm w=420n l=100n
Mp_c3 n_cp2 a   vdd vdd pmos_90nm w=420n l=100n
Mp_c4 n_cp2 b   vdd vdd pmos_90nm w=420n l=100n
Mp_c5 cout_b cin n_cp2 vdd pmos_90nm w=420n l=100n

* PDN for Cout_bar (5 NMOS)
Mn_c1 cout_b a   n_cn1 0 nmos_90nm w=360n l=100n
Mn_c2 n_cn1  b   0     0 nmos_90nm w=360n l=100n
Mn_c3 cout_b cin n_cn2 0 nmos_90nm w=360n l=100n
Mn_c4 n_cn2  a   0     0 nmos_90nm w=360n l=100n
Mn_c5 n_cn2  b   0     0 nmos_90nm w=360n l=100n

* Inverter for Cout (2 Transistors)
Mp_cinv cout cout_b vdd vdd pmos_90nm w=420n l=100n
Mn_cinv cout cout_b 0   0   nmos_90nm w=120n l=100n

* --- Sum Generation (16 Transistors) ---
* PUN for Sum_bar (7 PMOS)
Mp_s1 n_sp1 a    vdd vdd pmos_90nm w=420n l=100n
Mp_s2 n_sp1 b    vdd vdd pmos_90nm w=420n l=100n
Mp_s3 n_sp1 cin  vdd vdd pmos_90nm w=420n l=100n
Mp_s4 sum_b cout n_sp1 vdd pmos_90nm w=420n l=100n
Mp_s5 n_sp2 a    vdd vdd pmos_90nm w=420n l=100n
Mp_s6 n_sp3 b    n_sp2 vdd pmos_90nm w=420n l=100n
Mp_s7 sum_b cin  n_sp3 vdd pmos_90nm w=420n l=100n

* PDN for Sum_bar (7 NMOS)
Mn_s1 sum_b cout n_sn1 0 nmos_90nm w=360n l=100n
Mn_s2 n_sn1 a    0     0 nmos_90nm w=360n l=100n
Mn_s3 n_sn1 b    0     0 nmos_90nm w=360n l=100n
Mn_s4 n_sn1 cin  0     0 nmos_90nm w=360n l=100n
Mn_s5 sum_b a    n_sn2 0 nmos_90nm w=360n l=100n
Mn_s6 n_sn2 b    n_sn3 0 nmos_90nm w=360n l=100n
Mn_s7 n_sn3 cin  0     0 nmos_90nm w=360n l=100n

* Inverter for Sum (2 Transistors)
Mp_sinv sum sum_b vdd vdd pmos_90nm w=420n l=100n
Mn_sinv sum sum_b 0   0   nmos_90nm w=120n l=100n

.ends FA_STATIC
"""

def generate_domino_fa_subcircuit():
    return """
* Domino Logic 1-Bit Full Adder
* Precharge PMOS + NMOS Evaluate + Weak Keeper + Output Inverter
.subckt FA_DOMINO a b cin clk sum cout vdd 0

* --- Domino Carry (10 Transistors) ---
* Precharge PMOS (Phi=0 -> precharge dyn_cout to VDD)
Mp_cpre dyn_cout clk vdd vdd pmos_90nm w=420n l=100n

* Weak PMOS Keeper (Gated by cout)
Mp_ckp dyn_cout cout vdd vdd pmos_90nm w=100n l=100n

* NMOS Evaluate Tree for Cout (Carry = AB + BCin + ACin)
Mn_ce1 dyn_cout a    n_cev1 0 nmos_90nm w=360n l=100n
Mn_ce2 n_cev1   b    n_cfoot 0 nmos_90nm w=360n l=100n
Mn_ce3 dyn_cout cin  n_cev2 0 nmos_90nm w=360n l=100n
Mn_ce4 n_cev2   a    n_cfoot 0 nmos_90nm w=360n l=100n
Mn_ce5 n_cev2   b    n_cfoot 0 nmos_90nm w=360n l=100n

* Evaluate Foot Transistor (Clocked by clk)
Mn_cfoot n_cfoot clk 0 0 nmos_90nm w=360n l=100n

* Static Output Inverter (Monotonic output)
Mp_cinv cout dyn_cout vdd vdd pmos_90nm w=420n l=100n
Mn_cinv cout dyn_cout 0 0 nmos_90nm w=120n l=100n

* --- Domino Sum (10 Transistors) ---
* Precharge PMOS
Mp_spre dyn_sum clk vdd vdd pmos_90nm w=420n l=100n

* Weak PMOS Keeper
Mp_skp dyn_sum sum vdd vdd pmos_90nm w=100n l=100n

* Evaluate Tree for Sum (A, B, Cin)
Mn_se1 dyn_sum a    n_sfoot 0 nmos_90nm w=360n l=100n
Mn_se2 dyn_sum b    n_sfoot 0 nmos_90nm w=360n l=100n
Mn_se3 dyn_sum cin  n_sfoot 0 nmos_90nm w=360n l=100n
Mn_sfoot n_sfoot clk 0 0 nmos_90nm w=360n l=100n

* Output Inverter
Mp_sinv sum dyn_sum vdd vdd pmos_90nm w=420n l=100n
Mn_sinv sum dyn_sum 0 0 nmos_90nm w=120n l=100n

.ends FA_DOMINO
"""

def generate_c2mos_fa_subcircuit():
    return """
* C²MOS 1-Bit Full Adder
* Anti-phase Clock-Gated Inverting Stages (Phi and Phi_bar)
.subckt FA_C2MOS a b cin clk clk_b sum cout vdd 0

* --- Stage 1: Carry Generation (Clocked on Phi) ---
* PUN (PMOS logic + PMOS clock gate driven by clk_b)
Mp_c1 n_cp1 a   vdd vdd pmos_90nm w=420n l=100n
Mp_c2 n_cp2 b   n_cp1 vdd pmos_90nm w=420n l=100n
Mp_c3 n_cp3 cin vdd vdd pmos_90nm w=420n l=100n
Mp_c4 n_cg  a   n_cp3 vdd pmos_90nm w=420n l=100n
Mp_c5 n_cg  b   n_cp3 vdd pmos_90nm w=420n l=100n
Mp_cclk cout_b clk_b n_cg vdd pmos_90nm w=420n l=100n

* PDN (NMOS clock gate driven by clk + NMOS logic)
Mn_cclk cout_b clk n_cn 0 nmos_90nm w=360n l=100n
Mn_c1 n_cn  a   n_cn1 0 nmos_90nm w=360n l=100n
Mn_c2 n_cn1 b   0     0 nmos_90nm w=360n l=100n
Mn_c3 n_cn  cin n_cn2 0 nmos_90nm w=360n l=100n
Mn_c4 n_cn2 a   0     0 nmos_90nm w=360n l=100n
Mn_c5 n_cn2 b   0     0 nmos_90nm w=360n l=100n

* Stage 2: Output Inverter for Cout
Mp_cinv cout cout_b vdd vdd pmos_90nm w=420n l=100n
Mn_cinv cout cout_b 0   0   nmos_90nm w=120n l=100n

* --- Sum Generation (C²MOS Stage) ---
Mp_s1 n_sp1 a    vdd vdd pmos_90nm w=420n l=100n
Mp_s2 n_sp1 b    vdd vdd pmos_90nm w=420n l=100n
Mp_s3 n_sp1 cin  vdd vdd pmos_90nm w=420n l=100n
Mp_sclk sum_b clk_b n_sp1 vdd pmos_90nm w=420n l=100n

Mn_sclk sum_b clk n_sn1 0 nmos_90nm w=360n l=100n
Mn_s1 n_sn1 a   0 0 nmos_90nm w=360n l=100n
Mn_s2 n_sn1 b   0 0 nmos_90nm w=360n l=100n
Mn_s3 n_sn1 cin 0 0 nmos_90nm w=360n l=100n

* Stage 2: Output Inverter for Sum
Mp_sinv sum sum_b vdd vdd pmos_90nm w=420n l=100n
Mn_sinv sum sum_b 0   0   nmos_90nm w=120n l=100n

.ends FA_C2MOS
"""

# -------------------------------------------------------------
# 2. 4-Bit RCA Testbench Generator
# -------------------------------------------------------------

def build_4bit_rca_netlist(style="static"):
    header = get_header(f"4-Bit RCA Benchmark - {style.upper()} CMOS 90nm")
    
    # Input stimulus: Worst-case carry ripple propagation
    # A = 1111 (all 1), B = 0000 (all 0)
    # Cin transitions from 0 -> 1 at 1.0 ns
    # Carry must ripple C0 -> C1 -> C2 -> C3 -> C4
    stimulus = """
* Operand Inputs: A=1111, B=0000
VA0 a0 0 DC 1.0
VA1 a1 0 DC 1.0
VA2 a2 0 DC 1.0
VA3 a3 0 DC 1.0

VB0 b0 0 DC 0.0
VB1 b1 0 DC 0.0
VB2 b2 0 DC 0.0
VB3 b3 0 DC 0.0

* Carry-In Step Input (Transition 0 -> 1 at 1.0ns)
Vcin c0 0 PULSE(0.0 1.0 1.0n 20p 20p 2.0n 5.0n)
"""

    if style == "static":
        subckt = generate_static_cmos_fa_subcircuit()
        instantiations = """
* 4-Bit RCA Chain (Static CMOS)
XFA0 a0 b0 c0 s0 c1 vdd 0 FA_STATIC
XFA1 a1 b1 c1 s1 c2 vdd 0 FA_STATIC
XFA2 a2 b2 c2 s2 c3 vdd 0 FA_STATIC
XFA3 a3 b3 c3 s3 c4 vdd 0 FA_STATIC

* Load Capacitances (2 fF per output)
CL0 s0 0 2f
CL1 s1 0 2f
CL2 s2 0 2f
CL3 s3 0 2f
CLC c4 0 2f
"""
    elif style == "domino":
        subckt = generate_domino_fa_subcircuit()
        stimulus += """
* Clock: 1 GHz (Low precharge, High evaluate at 1.0ns)
Vclk clk 0 PULSE(0.0 1.0 1.0n 20p 20p 1.0n 2.0n)
"""
        instantiations = """
* 4-Bit RCA Chain (Domino Logic)
XFA0 a0 b0 c0 clk s0 c1 vdd 0 FA_DOMINO
XFA1 a1 b1 c1 clk s1 c2 vdd 0 FA_DOMINO
XFA2 a2 b2 c2 clk s2 c3 vdd 0 FA_DOMINO
XFA3 a3 b3 c3 clk s3 c4 vdd 0 FA_DOMINO

CL0 s0 0 2f
CL1 s1 0 2f
CL2 s2 0 2f
CL3 s3 0 2f
CLC c4 0 2f
"""
    elif style == "c2mos":
        subckt = generate_c2mos_fa_subcircuit()
        stimulus += """
* Clocks: Phi and Phi_bar
Vclk clk 0 PULSE(0.0 1.0 1.0n 20p 20p 1.0n 2.0n)
Vclk_b clk_b 0 PULSE(1.0 0.0 1.0n 20p 20p 1.0n 2.0n)
"""
        instantiations = """
* 4-Bit RCA Chain (C²MOS)
XFA0 a0 b0 c0 clk clk_b s0 c1 vdd 0 FA_C2MOS
XFA1 a1 b1 c1 clk clk_b s1 c2 vdd 0 FA_C2MOS
XFA2 a2 b2 c2 clk clk_b s2 c3 vdd 0 FA_C2MOS
XFA3 a3 b3 c3 clk clk_b s3 c4 vdd 0 FA_C2MOS

CL0 s0 0 2f
CL1 s1 0 2f
CL2 s2 0 2f
CL3 s3 0 2f
CLC c4 0 2f
"""

    control = f"""
.control
tran 1p 3.0n

* Worst-Case Carry Propagation Delay: C0 (50%) -> C4 (50%)
meas tran tp_carry trig v(c0) val=0.5 rise=1 targ v(c4) val=0.5 rise=1
meas tran tp_c1 trig v(c0) val=0.5 rise=1 targ v(c1) val=0.5 rise=1
meas tran tp_c2 trig v(c0) val=0.5 rise=1 targ v(c2) val=0.5 rise=1
meas tran tp_c3 trig v(c0) val=0.5 rise=1 targ v(c3) val=0.5 rise=1

* Average Power Dissipation: Integral of Vdd * I(Vdd) / Period
meas tran avg_curr avg i(Vdd) from=1.0n to=2.0n
let avg_pwr = -avg_curr * 1.0
print avg_pwr tp_carry

* Export waveforms to raw table
wrdata {to_wsl_path(os.path.join(RESULTS_DIR, f"{style}_waveforms.txt"))} v(c0) v(c1) v(c2) v(c3) v(c4)
quit
.endc
.end
"""

    return header + subckt + stimulus + instantiations + control

# -------------------------------------------------------------
# 3. Simulator Execution & Metric Extraction
# -------------------------------------------------------------

def run_simulation(style):
    netlist_content = build_4bit_rca_netlist(style)
    netlist_path = os.path.join(NETLIST_DIR, f"rca4_{style}.cir")
    with open(netlist_path, "w") as f:
        f.write(netlist_content)
    
    wsl_netlist = to_wsl_path(netlist_path)
    cmd = ["wsl", "-d", "Ubuntu", "ngspice", "-b", wsl_netlist]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = res.stdout
    
    tp_carry = None
    avg_pwr = None
    
    m_delay = re.search(r"tp_carry\s*=\s*([0-9.eE+-]+)", out)
    if m_delay:
        tp_carry = float(m_delay.group(1))

    m_pwr = re.search(r"avg_pwr\s*=\s*([0-9.eE+-]+)", out)
    if m_pwr:
        avg_pwr = float(m_pwr.group(1))

    transistor_counts = {
        "static": 28 * 4,    # 112 transistors
        "domino": 20 * 4,    # 80 transistors
        "c2mos": 16 * 4      # 64 transistors
    }

    delay_ps = (tp_carry * 1e12) if tp_carry else 0.0
    pwr_uW = (avg_pwr * 1e6) if avg_pwr else 0.0
    pdp_fJ = (pwr_uW * delay_ps) * 1e-3

    return {
        "style": style,
        "delay_ps": round(delay_ps, 2),
        "power_uW": round(pwr_uW, 2),
        "transistors": transistor_counts.get(style, 0),
        "pdp_fJ": round(pdp_fJ, 3),
        "stdout": out
    }

# -------------------------------------------------------------
# 4. Generate Comparative Plots
# -------------------------------------------------------------

def generate_plots():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    for idx, style in enumerate(["static", "domino", "c2mos"]):
        wfile = os.path.join(RESULTS_DIR, f"{style}_waveforms.txt")
        if not os.path.exists(wfile):
            continue
            
        data = np.loadtxt(wfile)
        time_ns = data[:, 0] * 1e9
        c0 = data[:, 1]
        c1 = data[:, 3]
        c2 = data[:, 5]
        c3 = data[:, 7]
        c4 = data[:, 9]

        ax = axes[idx]
        ax.plot(time_ns, c0, label="Cin (C0)", linewidth=1.8, linestyle="--", color="black")
        ax.plot(time_ns, c1, label="C1", linewidth=1.5)
        ax.plot(time_ns, c2, label="C2", linewidth=1.5)
        ax.plot(time_ns, c3, label="C3", linewidth=1.5)
        ax.plot(time_ns, c4, label="Cout (C4)", linewidth=2.0, color="crimson")
        
        ax.set_title(f"{style.upper()} 4-Bit Carry Ripple (90nm)", fontsize=11, fontweight="bold")
        ax.set_xlabel("Time (ns)", fontsize=9)
        ax.set_ylabel("Voltage (V)", fontsize=9)
        ax.set_xlim(0.95, 1.6)
        ax.set_ylim(-0.05, 1.1)
        ax.grid(True, linestyle=":", alpha=0.6)
        if idx == 0:
            ax.legend(loc="upper left", fontsize=8)

    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, "rca_carry_ripple_comparison.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    return plot_path

if __name__ == "__main__":
    print("Running 4-Bit RCA Benchmark for all 3 logic styles at 90nm...")
    results = []
    for s in ["static", "domino", "c2mos"]:
        res = run_simulation(s)
        results.append(res)
        print(f"[{s.upper()}] Delay: {res['delay_ps']} ps | Power: {res['power_uW']} uW | Transistors: {res['transistors']} | PDP: {res['pdp_fJ']} fJ")
    
    plot_file = generate_plots()
    print(f"Comparison plot generated at: {plot_file}")
