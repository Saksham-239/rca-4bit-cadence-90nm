# Technical Audit & Verification Record

This document records the netlist verification, arithmetic checks, measurement scope, and methodological boundaries underlying the reported results in [`comparative_analysis.md`](comparative_analysis.md) and [`report/case_study.pdf`](../report/case_study.pdf).

---

## 1. Cadence Netlist Transistor Count Verification

The transistor counts are directly verified against [`cadence/rca_all_designs.sp`](../cadence/rca_all_designs.sp), which is the SPICE netlist imported into Cadence Virtuoso (`gpdk090`) and referenced by all three Spectre testbenches:

| Subcircuit | PMOS / FA | NMOS / FA | Total MOSFETs / FA | 4-Bit Top-Level (`RCA4_*`) | Breakdown & Key Devices |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `FA_STATIC` | 14 | 14 | **28** | **112** | Mirror carry stage (12T: 5P, 5N, 2T inv) + sum stage (16T: 7P, 7N, 2T inv) |
| `FA_C2MOS` | 16 | 16 | **32** | **128** | Clock-gated carry stage (14T: `Mp_cclk` on `clkb`, `Mn_cclk` on `clk` + 2T inv) + clock-gated sum stage (18T) |
| `FA_DOMINO` | 11 | 15 | **26** | **104** | Footed dynamic carry cone (10T incl. `Mp_cpre`, weak keeper `Mp_ckp` $W=100\text{ nm}$, footer `Mn_cfoot`, 2T inv) + sum stage (16T driven by `dyn_cout`) |

> **Note:** These figures represent schematic-level MOSFET counts rather than post-layout silicon area. Physical area depends additionally on device sizing ($W/L$), routing tracks, clock distribution, and well/contact rules.

---

## 2. Calculator Summary & PDP Arithmetic Verification

Power-Delay Product (PDP) is evaluated in femtojoules ($\text{fJ}$) from the reported Cadence Calculator average power $P_{\text{avg}}$ ($\mu\text{W}$) and corrected calculator delay $t_{\text{pd}}$ ($\text{ps}$):

$$\mathrm{PDP}\ (\mathrm{fJ}) = \frac{P_{\text{avg}}\ (\mu\mathrm{W}) \times t_{\text{pd}}\ (\mathrm{ps})}{1000}$$

| Logic Family | $P_{\text{avg}}$ ($\mu\text{W}$) | Corrected $t_{\text{pd}}$ ($\text{ps}$) | Exact Product ($\text{fJ}$) | Reported Rounded PDP ($\text{fJ}$) |
| :--- | :---: | :---: | :---: | :---: |
| **Static CMOS** | 13.25 | 251.81 | $13.25 \times 251.81 / 1000 = 3.3364825$ | **3.34 fJ** |
| **$\text{C}^2\text{MOS}$** | 29.49 | 260.75 | $29.49 \times 260.75 / 1000 = 7.6895175$ | **7.69 fJ** |
| **Domino Logic** | 30.76 | 222.35 | $30.76 \times 222.35 / 1000 = 6.8394860$ | **6.84 fJ** |

Both [`analysis/scripts/generate_performance_plots.m`](scripts/generate_performance_plots.m) and [`analysis/scripts/generate_performance_plots.py`](scripts/generate_performance_plots.py) assert exact match to `[3.34, 7.69, 6.84]` before generating any figures.

### Delay Label Correction Note
Earlier preliminary review slides had the summary delay labels for Static CMOS (`251.81 ps`) and Domino Logic (`222.35 ps`) swapped. The final Case Study report and all repository tables use the corrected assignments confirmed by the authors:
* **Domino Logic:** `222.35 ps` (fastest)
* **Static CMOS:** `251.81 ps`
* **$\text{C}^2\text{MOS}$:** `260.75 ps`

---

## 3. Transient Waveform Evidence & Path Observations

The transient waveform annotations provide path-specific timing checks that complement (but are distinct from) the aggregate calculator summary delays:

1. **Static CMOS (`static_carry_ripple_step.jpg` & `static_output_waveforms.png`):**
   * Single-step ripple staircase (`Cin` rising at `1.000 ns`):
     * `S0`: $\approx 1.080\text{ ns}$ ($\approx 80\text{ ps}$)
     * `S1`: $\approx 1.148\text{ ns}$ ($\approx 148\text{ ps}$)
     * `S2`: $\approx 1.212\text{ ns}$ ($\approx 212\text{ ps}$)
     * `Cout (C4)`: $\approx 1.248\text{ ns}$ (**248 ps** from `Cin`)
     * `S3`: $\approx 1.265\text{ ns}$ (**265 ps** from `Cin`)
   * Multi-cycle transient (`static_output_waveforms.png`, $0\text{–}60\text{ ns}$): shows repeated transitions across all sum and carry outputs synchronized to `Cin`.

2. **$\text{C}^2\text{MOS}$ (`c2mos_output_waveforms.png`):**
   * Vector: $A = 1011_2\ (11)$, $B = 1100_2\ (12)$, complementary clocks (`clk`, `clkb`) at $500\text{ MHz}$ ($T = 2\text{ ns}$).
   * Intervals $0\text{–}10\text{ ns}$, $20\text{–}30\text{ ns}$ ($C_{in} = 0$): $\{C_{out}, S_3, S_2, S_1, S_0\} = 10111_2 = 23_{10}$.
   * Intervals $10\text{–}20\text{ ns}$, $30\text{–}40\text{ ns}$ ($C_{in} = 1$): $\{C_{out}, S_3, S_2, S_1, S_0\} = 11000_2 = 24_{10}$.

3. **Domino Logic (`domino_output_waveforms.png`):**
   * Vector: $A = 0111_2\ (7)$, $B = 1000_2\ (8)$, full carry-propagate condition ($P_i = A_i \oplus B_i = 1$ for all 4 bits).
   * Intervals with $C_{in} = 0$: $\{C_{out}, S_3, S_2, S_1, S_0\} = 01111_2 = 15_{10}$ during evaluation (`clk = 1`).
   * Intervals with $C_{in} = 1$: $\{C_{out}, S_3, S_2, S_1, S_0\} = 10000_2 = 16_{10}$ during evaluation (`clk = 1`).
   * Marked waveform propagation observation: $C_{in} \to S_2 \approx 232\text{ ps}$ (`10.010 ns` to `10.242 ns`).

---

## 4. Methodological Scope & Caveats

To present an intellectually honest engineering benchmark, the following boundaries from the Case Study apply:
* **Unmatched stimulus vectors in ViVA captures:** The displayed $\text{C}^2\text{MOS}$ and Domino waveforms evaluate different operand vectors ($A=1011_2, B=1100_2$ vs. $A=0111_2, B=1000_2$), and the Static CMOS multi-cycle waveform operand levels are not specified in the captured screenshot metadata.
* **Aggregate average power:** Reported average powers ($13.25$, $29.49$, and $30.76\ \mu\text{W}$) reflect total supply power across their respective simulation runs; they do not isolate clock-tree power, precharge switching, short-circuit current, and static leakage individually.
* **PDP vs. integrated energy per operation:** PDP is computed from $P_{\text{avg}} \cdot t_{\text{pd}}$, which carries energy units ($\text{fJ}$) as a combined figure of merit, rather than integrating $V_{DD} I_{DD}(t)\,dt$ over a single isolated addition window.
* **Schematic-level scope:** Results exclude post-layout RC parasitic extraction, process/voltage/temperature (PVT) corners, and Monte Carlo mismatch sweeps.
