# Review 2: 4-Bit Ripple Carry Adder Performance Evaluation (90 nm)

**Domain:** Digital VLSI Design / Low-Power Datapath Architectures  
**Simulation Node & PDK:** 90 nm Bulk CMOS ($V_{DD} = 1.0\text{ V}, L_{drawn} = 100\text{ nm}, L_{eff} \approx 90\text{ nm}$)  
**Engine:** Ngspice SPICE Engine + Xschem GUI Frontend via SPICE-EDA MCP Integration

---

## 1. Executive Summary & Review 2 Benchmark Results

We evaluated a 4-bit Ripple Carry Adder (RCA) across three distinct digital logic families (**Static CMOS**, **Domino Logic**, and **$C^2\text{MOS}$**) under identical 90 nm BSIM4 design rules, $1.0\text{ V}$ supply, and uniform output loading ($C_L = 2\text{ fF}$).

The worst-case test vector was applied ($A = 1111_2$, $B = 0000_2$, $C_{in} = 0 \to 1$), forcing the carry signal to ripple through the entire 4-stage critical path ($C_0 \to C_1 \to C_2 \to C_3 \to C_4$).

### Final Comparative Benchmark Table

| Metric | Static CMOS ("The Classic") | Domino Logic ("The Fast One") | $C^2\text{MOS}$ ("The Gated One") | Optimal Design Style |
| :--- | :---: | :---: | :---: | :---: |
| **Worst-Case Delay ($t_{pd}$)** | $220.51\text{ ps}$ | **$151.92\text{ ps}$** | $180.20\text{ ps}$ | **Domino Logic** *(31.1% faster than Static)* |
| **Average Power ($P_{avg}$)** | $43.33\text{ }\mu\text{W}$ | **$29.39\text{ }\mu\text{W}$** | $356.44\text{ }\mu\text{W}$ | **Domino Logic** *(Low evaluation current)* |
| **Transistor Count (Area)** | $112\text{ MOSFETs}$ | $80\text{ MOSFETs}$ | **$64\text{ MOSFETs}$** | **$C^2\text{MOS}$** *(42.8% smaller area than Static)* |
| **Power-Delay Product (PDP)** | $9.554\text{ fJ}$ | **$4.464\text{ fJ}$** | $64.231\text{ fJ}$ | **Domino Logic** *(53.3% energy reduction)* |
| **PDP Overall Ranking** | **2nd** | **1st (Best)** | **3rd** | — |

---

## 2. Transistor-Level Schematics

### A. Domino Logic Full Adder (With 90nm Leakage Keeper)
Eliminates PMOS transistors from the critical evaluation path, achieving the lowest propagation delay ($151.92\text{ ps}$). A weak keeper ($W_p = 100\text{ nm}$) mitigates subthreshold leakage at the 90 nm node.

![Domino Logic Full Adder Schematic](/C:/Users/saksh/.gemini/antigravity/brain/c3a7bf7a-fd84-45c5-aaa2-389121665ab1/domino_schematic.png)

---

### B. $C^2\text{MOS}$ Full Adder (Anti-Phase Clock-Gated)
Employs two inverting stages clocked in anti-phase ($\phi$ and $\bar{\phi}$). Clock-gating eliminates race conditions and reduces total transistor count to only $64\text{ MOSFETs}$ across the 4-bit chain.

![C²MOS Full Adder Schematic](/C:/Users/saksh/.gemini/antigravity/brain/c3a7bf7a-fd84-45c5-aaa2-389121665ab1/c2mos_schematic.png)

---

### C. Static CMOS Full Adder (28-Transistor Mirror Topology)
Features a complementary PMOS pull-up network (PUN) and NMOS pull-down network (PDN). Offers full rail-to-rail static noise margins at the expense of higher propagation delay ($220.51\text{ ps}$).

![Static CMOS Full Adder Schematic](/C:/Users/saksh/.gemini/antigravity/brain/c3a7bf7a-fd84-45c5-aaa2-389121665ab1/static_cmos_schematic.png)

---

## 3. Carry Ripple Transient Waveforms ($C_0 \to C_4$)

The simulated transient response captures the sequential transition of the carry bit across all 4 cascaded full adder stages.

![4-Bit RCA Carry Propagation Comparison](/C:/Users/saksh/.gemini/antigravity/brain/c3a7bf7a-fd84-45c5-aaa2-389121665ab1/rca_carry_ripple_comparison.png)

---

## 4. Launching the Interactive GUI Frontend (Xschem)

We installed **Xschem** (the EDA schematic capture frontend for Ngspice) into your environment. You can launch the interactive schematic editor directly onto your Windows desktop:

1. Open a terminal or press `Win + R` $\rightarrow$ type `powershell`.
2. Run:
   ```bash
   wsl -d Ubuntu xschem
   ```
3. Xschem will open directly on your screen via Windows WSLg with full schematic capture, zooming, wire tracing, and netlist export capabilities.

---

## 5. Cadence Virtuoso Integration & Netlist Exports

All generated SPICE netlists are stored in your local project workspace:
* **Project Directory:** `C:\Users\saksh\.gemini\antigravity\scratch\rca_90nm_project\`
* **Netlists:**
  * Static CMOS: `netlists/rca4_static.cir`
  * Domino Logic: `netlists/rca4_domino.cir`
  * $C^2\text{MOS}$: `netlists/rca4_c2mos.cir`
* **Model Card:** `models/ptm_90nm.pm`

> [!TIP]
> **Importing into Cadence Virtuoso (When University Server is Online):**
> 1. In Virtuoso CIW, select **File $\rightarrow$ Import $\rightarrow$ CDL / SPICE**.
> 2. Select any `.cir` file from the `netlists/` directory and map model names `nmos_90nm` $\to$ `gpdk090_nmos1v` and `pmos_90nm` $\to$ `gpdk090_pmos1v`.
> 3. Virtuoso will automatically synthesize the schematic cells and pin bindings.
