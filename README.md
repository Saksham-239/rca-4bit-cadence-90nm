# 4-Bit Ripple Carry Adder (RCA) Design & Evaluation Suite (90nm CMOS)

[![Virtuoso IC6.1.7](https://img.shields.io/badge/Cadence%20Virtuoso-IC6.1.7-blue.svg)](https://www.cadence.com)
[![Simulator Spectre](https://img.shields.io/badge/Simulator-Spectre%20%2F%20MMSIM15-orange.svg)]()
[![PDK GPDK090](https://img.shields.io/badge/PDK-gpdk090%20(90nm)-green.svg)]()
[![Ngspice Standalone](https://img.shields.io/badge/Standalone-Ngspice%2038%2B-lightgrey.svg)]()

This repository contains the complete design, transistor netlists, SKILL automation scripts, simulation testbenches, and benchmark reports for a **4-Bit Ripple Carry Adder (RCA)** designed at the **90nm CMOS** technology node ($V_{DD} = 1.0\text{ V}$).

Three distinct digital VLSI logic styles are implemented, simulated, and benchmarked:
1. **Static CMOS** (28-Transistor Mirror Topology per Full Adder, 112 MOSFETs total)
2. **Domino Logic** (Compound Dynamic Logic with 90nm Subthreshold Weak Keeper, 80 MOSFETs total)
3. **$C^2\text{MOS}$** (Anti-Phase Clock-Gated Latched Logic, 64 MOSFETs total)

---

## 1. Benchmark & Performance Summary

All three architectures were simulated under identical conditions: $V_{DD} = 1.0\text{ V}$, $T = 27^\circ\text{C}$, $90\text{ nm}$ BSIM4 models, and identical output loads ($C_L = 2\text{ fF}$ per output pin). The worst-case carry ripple vector was applied ($A = 1111_2$, $B = 0000_2$, $C_{in} = 0 \to 1$ step transition), forcing the carry signal to ripple through the full 4-stage critical path ($C_0 \to C_1 \to C_2 \to C_3 \to C_4$).

| Architecture | Transistor Count (4-Bit) | Worst-Case Delay ($t_{pd}$) | Average Power ($P_{avg}$) | Power-Delay Product (PDP) | Key Strengths |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Domino Logic** | **80 MOSFETs** | **$151.92\text{ ps}$** *(Fastest)* | **$29.39\text{ }\mu\text{W}$** | **$4.464\text{ fJ}$** *(Best)* | 31.1% faster than Static, lowest dynamic delay. |
| **Static CMOS** | 112 MOSFETs | $220.51\text{ ps}$ | $43.33\text{ }\mu\text{W}$ | $9.554\text{ fJ}$ | Full rail-to-rail noise margin, zero static leakage. |
| **$C^2\text{MOS}$** | **64 MOSFETs** *(Smallest)*| $180.20\text{ ps}$ | $356.44\text{ }\mu\text{W}$ | $64.231\text{ fJ}$ | 42.8% smaller area than Static, eliminates race conditions. |

---

## 2. Repository Structure

```
RCA_4Bit_Cadence_90nm/
├── README.md                           # This complete setup and execution guide
├── .gitignore                          # EDA lock/log and temporary file exclusion
│
├── cadence/                            # Cadence Virtuoso IC6.1.7 import & setup files
│   ├── rca_all_designs.sp              # Complete SPICE netlist (Static, Domino, C2MOS)
│   ├── devmap_gpdk090.map              # Device map for GPDK090 (maps nmos_90nm/pmos_90nm -> nmos1v/pmos1v)
│   ├── devmap_analogLib.map            # Device map for generic analogLib
│   ├── model_alias.scs                 # Spectre model alias file for GPDK090
│   ├── fix_symbols.il                  # SKILL script to generate standardized clean symbols
│   ├── create_all_testbenches.il       # SKILL script: AUTO-CREATES tb_rca4_static, tb_rca4_domino, tb_rca4_c2mos
│   └── testbenches/                    # Ready-to-simulate Spectre testbench decks (.scs)
│       ├── tb_rca4_static.scs
│       ├── tb_rca4_domino.scs
│       └── tb_rca4_c2mos.scs
│
├── schematics_and_waveforms/           # Reference diagrams and simulation results
│   ├── static_cmos_schematic.png       # 28T Mirror Static Full Adder schematic
│   ├── domino_schematic.png            # Compound Domino Full Adder schematic
│   ├── c2mos_schematic.png             # Clock-gated C²MOS Full Adder schematic
│   ├── rca_carry_ripple_comparison.png # 4-stage carry ripple transient waveform comparison
│   └── testbenches/                    # Screenshots of the exact Cadence Virtuoso testbenches & ADE L
│       ├── tb_rca4_static_schematic.png
│       ├── tb_rca4_static_waveforms.jpg
│       ├── tb_rca4_domino_schematic.png
│       ├── tb_rca4_domino_adel.png
│       ├── tb_rca4_domino_waveforms.png
│       ├── tb_rca4_c2mos_schematic.png
│       └── tb_rca4_c2mos_adel.png
│
├── standalone_simulation/              # Standalone Python/Ngspice simulation suite (No VM required)
│   ├── runner.py                       # Automated benchmark script (executes ngspice and plots)
│   ├── render_schematics.py            # Schematic layout renderer
│   ├── models/ptm_90nm.pm              # BSIM4 90nm Predictive Technology Model
│   └── netlists/                       # Standalone SPICE decks (.cir)
│       ├── rca4_static.cir
│       ├── rca4_domino.cir
│       └── rca4_c2mos.cir
│
└── docs/                               # Project reports and presentation decks
    ├── 4bit_RCA_ProjectReview.pdf
    ├── Project Review 1_ 4-Bit RCA Design & Evaluation (90nm).pdf
    └── benchmark_results.md
```

---

## 3. Running in Cadence Virtuoso (Getintopc VM Workstation)

This project is pre-configured to run directly on the **Getintopc Cadence IC6.1.7 VM** image:
* **Host Platform:** VMware Workstation
* **Guest OS:** Red Hat Enterprise Linux 6 (RHEL6 64-bit)
* **Default VM Password:** `111111`
* **Pre-installed Tools:** Cadence Virtuoso IC6.1.7, MMSIM 15 (Spectre), GPDK090 PDK

Follow the steps below to import and simulate the designs.

---

### Step 1: Transfer Project Files into the VM

#### Method A: VMware Shared Folders (Recommended)
1. In VMware Workstation, click **VM** $\rightarrow$ **Settings...** $\rightarrow$ **Options** tab $\rightarrow$ **Shared Folders**.
2. Select **Always enabled**.
3. Click **Add...**, browse to this folder (`RCA_4Bit_Cadence_90nm`), and name the share `RCA_4Bit_Cadence_90nm`.
4. Inside the Linux VM, the folder is accessible at:
   ```bash
   /mnt/hgfs/RCA_4Bit_Cadence_90nm
   ```
   *(If `/mnt/hgfs` is empty, run `vmhgfs-fuse /mnt/hgfs -o allow_other` in terminal).*

#### Method B: Direct Git Clone inside the VM
Inside the VM terminal:
```bash
git clone <your-private-github-repo-url> ~/RCA_4Bit_Cadence_90nm
```

---

### Step 2: Start Cadence Virtuoso

1. Open a terminal in the VM.
2. Navigate to your Cadence working directory (where `cds.lib` is located, typically `~/work` or `~/cadence`):
   ```bash
   cd ~/work
   virtuoso &
   ```
3. The Virtuoso Command Interpreter Window (CIW) and Library Manager will open.

---

### Step 3: Create the Target Library

1. In Virtuoso CIW, click **File** $\rightarrow$ **New** $\rightarrow$ **Library...**
2. Name the library: `rca`
3. In the technology selection dialog, choose **Attach to an existing technology library**.
4. Select **`gpdk090`** and click **OK**.

---

### Step 4: Import the SPICE Netlist (`rca_all_designs.sp`)

1. In Virtuoso CIW, click **File** $\rightarrow$ **Import** $\rightarrow$ **CDL / SPICE...**
2. Fill out the dialog as follows:
   * **Netlist File:** `/mnt/hgfs/RCA_4Bit_Cadence_90nm/cadence/rca_all_designs.sp`  
     *(or your cloned path `~/RCA_4Bit_Cadence_90nm/cadence/rca_all_designs.sp`)*
   * **Target Library:** `rca`
   * **Device-map file:** `/mnt/hgfs/RCA_4Bit_Cadence_90nm/cadence/devmap_gpdk090.map`
   * **Reference Library List:** `gpdk090 analogLib basic`
3. Click **OK**.
4. Virtuoso will automatically synthesize transistor schematics and pin bindings for:
   * `FA_STATIC` & `RCA4_STATIC` (Static CMOS)
   * `FA_DOMINO` & `RCA4_DOMINO` (Domino Logic)
   * `FA_C2MOS` & `RCA4_C2MOS` ($C^2\text{MOS}$)

---

### Step 5: Automatically Fix & Clean Symbols

Default symbols generated by SPICE In have random pin placement. A dedicated Cadence SKILL script is included to automatically rebuild clean, professional symbols with:
* **Inputs on Left:** $a, b, cin, a_0\dots a_3, b_0\dots b_3, clk, clkb$
* **Outputs on Right:** $sum, cout, s_0\dots s_3$
* **VDD on Top**
* **GND on Bottom**

In the Virtuoso CIW command line, type:
```lisp
load("/mnt/hgfs/RCA_4Bit_Cadence_90nm/cadence/fix_symbols.il")
```
You will see confirmation messages for each cell. Now opening the symbol view of any cell will show clean, standardized rectangular symbols.

---

### Step 6: Create or Auto-Generate Testbenches & Simulate in ADE L

You have two easy ways to run the testbenches in Virtuoso:

#### Method 1: Automatic Testbench Generation via SKILL (Zero-Wiring!)
Instead of manually placing and wiring dozens of sources and pins, simply load the included SKILL script in Virtuoso CIW:
```lisp
load("/mnt/hgfs/RCA_4Bit_Cadence_90nm/cadence/create_all_testbenches.il")
```
This automatically builds and saves all three fully-wired testbenches in your `rca` library:
* **`tb_rca4_static`** (Static CMOS)
* **`tb_rca4_domino`** (Domino Logic with 500 MHz evaluation clock)
* **`tb_rca4_c2mos`** ($C^2\text{MOS}$ with anti-phase $\phi$ and $\bar{\phi}$ clocks)

You can now open any of them in Library Manager, click **Launch $\rightarrow$ ADE L**, set `gpdk090.scs` + `model_alias.scs`, choose `tran 3n` (or `20n` for clocked adders), and click **Netlist and Run**!

#### Method 2: Command-Line Simulation via Spectre
Teammates can also simulate the pre-built Spectre decks directly from the Linux terminal:
```bash
cd /mnt/hgfs/RCA_4Bit_Cadence_90nm/cadence/testbenches
spectre tb_rca4_static.scs
spectre tb_rca4_domino.scs
spectre tb_rca4_c2mos.scs
```
View the waveforms immediately in ViVA:
```bash
viva tb_rca4_static.raw &
```

#### Method 3: Manual Schematic Construction (Visual Reference)
If teammates prefer or are required to build the testbenches by hand in schematic editor:
* Reference schematics and ADE L settings are in `schematics_and_waveforms/testbenches/`:
  * `tb_rca4_static_schematic.png`
  * `tb_rca4_domino_schematic.png` & `tb_rca4_domino_adel.png`
  * `tb_rca4_c2mos_schematic.png` & `tb_rca4_c2mos_adel.png`

#### Simulation Waveform Signatures:
* **Static CMOS (`tb_rca4_static`):** When $C_{in}$ rises at $t = 1.00\text{ ns}$, the carry propagates through stages 0, 1, 2, and 3 sequentially ($S_0 \to S_1 \to S_2 \to C_{out} \to S_3$) with total carry delay $t_{pd} \approx 220-250\text{ ps}$.
* **Domino Logic (`tb_rca4_domino`):** Dynamic evaluate/precharge pulses with clock $\phi$, producing the fastest carry propagation delay ($t_{pd} \approx 150-160\text{ ps}$).
* **$C^2\text{MOS}$ (`tb_rca4_c2mos`):** Full rail-to-rail dynamic latching clocked by $\phi$ and $\bar{\phi}$, holding outputs clean without static leakage.

---

## 4. Standalone Simulation (Quick Check without Cadence VM)

If you or your teammates want to verify the results immediately on Windows/macOS/Linux without booting the heavy Cadence VM:

### Prerequisites
* Python 3.8+
* `ngspice` (installed on Windows via `winget install ngspice` or on Linux `sudo apt install ngspice`)
* Python packages: `pip install matplotlib numpy`

### Run
```bash
cd standalone_simulation
python runner.py
```
This script will:
1. Run SPICE simulations for Static, Domino, and $C^2\text{MOS}$ 4-bit RCAs.
2. Measure propagation delays ($t_{pd}$), average power dissipation ($P_{avg}$), and Power-Delay Product (PDP).
3. Output comparative waveform plots directly to `plots/rca_carry_ripple_comparison.png`.

---

## 5. How to Share with Teammates

### Option 1: Private GitHub Repository
1. Initialize the repo locally and commit:
   ```powershell
   cd C:\Users\saksh\Documents\RCA_4Bit_Cadence_90nm
   git init
   git add .
   git commit -m "Initial commit: 4-Bit RCA Cadence Virtuoso 90nm suite"
   ```
2. Create and push to a **Private** GitHub repository using the GitHub CLI:
   ```powershell
   gh auth login
   gh repo create rca-4bit-cadence-90nm --private --source=. --push
   ```
   *(Or create a new private repo on [github.com](https://github.com/new) and run:)*
   ```powershell
   git remote add origin https://github.com/<your-username>/rca-4bit-cadence-90nm.git
   git branch -M main
   git push -u origin main
   ```
3. Add teammates: On GitHub, go to **Settings** $\rightarrow$ **Collaborators** $\rightarrow$ **Add people**.

### Option 2: Pre-Packaged ZIP Archive
A pre-packaged, ready-to-share ZIP archive (`RCA_4Bit_Cadence_90nm.zip`) is available directly on this machine. You can send it via Google Drive, Discord, Teams, or USB.
