# Literature Review Synthesis

Twelve peer-reviewed studies from IEEE journals, an international electronics journal, and refereed conference proceedings inform this four-bit Ripple-Carry Adder (RCA) case study. Rather than treating metrics across disparate process nodes (0.35 μm down to 22 nm and 32 nm PTM) as directly interchangeable, the table below maps each study's evaluation methodology, reported trade-offs, and design challenges to the RCA implementation context.

## Comparative Literature Matrix

| Study | Approach & Evaluation | Advantage / Reported Result | Limitation / Design Challenge |
| :--- | :--- | :--- | :--- |
| **Suzuki et al. (1973)** [[Ref 5]](../report/latex/references.bib) | Clocked CMOS ($\text{C}^2\text{MOS}$) calculator circuitry | Early integrated arithmetic demonstration of clock-controlled CMOS | Clock phases and timing must be designed as an integral part of the logic system |
| **Nagendra et al. (1994)** [[Ref 1]](../report/latex/references.bib) | RCA, blocked carry-lookahead, and signed-digit adders with sized layouts | Judicious transistor sizing improves speed while controlling power increase; PDP guides trade-off | Faster carry architectures and larger devices add circuit and switching cost |
| **Zimmermann & Fichtner (1997)** [[Ref 6]](../report/latex/references.bib) | Static CMOS vs. Complementary Pass-Transistor Logic (CPL), including 32-bit adder | Static CMOS adder achieves `< 0.5×` CPL PDP in their implementation and is more robust to voltage scaling | Pass-transistor styles reduce device count but require swing restoration and degrade at low $V_{DD}$ |
| **Bisdounis et al. (1998)** [[Ref 2]](../report/latex/references.bib) | Transistor-level HSPICE benchmark study of static and dynamic CMOS styles | Evaluates area, delay, and power jointly and identifies style-dependent PDP trade-offs | Rankings depend heavily on the benchmark circuit and design choices |
| **Shams & Bayoumi (2000)** [[Ref 7]](../report/latex/references.bib) | 16-transistor FA using XOR/XNOR, pass transistors, and transmission gates | Reports higher speed and lower power than standard FA implementations (up to 30% energy savings) | Pass-transistor voltage swing and cascading behavior must be preserved across stages |
| **Alioto & Palumbo (2002)** [[Ref 3]](../report/latex/references.bib) | Full-adder topology comparison in 0.35 μm CMOS using Cadence + layout parasitics | Compares minimum-size and PDP-optimized designs; highlights sizing and parasitic impact | Cell rankings shift with sizing, supply voltage, and physical interconnect |
| **Lin et al. (2007)** [[Ref 8]](../report/latex/references.bib) | 10-transistor FA designs evaluated with HSPICE and cascaded operation | Investigates low-voltage operation and energy-delay behavior across word lengths | Threshold voltage loss in pass-transistor paths degrades output swing and cascading; buffering adds devices |
| **Alioto et al. (2008)** [[Ref 9]](../report/latex/references.bib) | Monte Carlo study of intradie process variation in nanometer Domino logic | Identifies key delay variability mechanisms in dynamic gates | Dynamic nodes and keeper feedback demand variation-aware timing and reliability analysis |
| **Zeydel et al. (2010)** [[Ref 4]](../report/latex/references.bib) | 64-bit static, dynamic, and compound-Domino adders across 65–22 nm | Reports up to 20% performance improvement and 4.5× energy reduction for co-optimized topologies | Gains stem from joint algorithm, topology, sizing, and wire co-optimization; not automatically transferable |
| **Kar et al. (2011)** [[Ref 10]](../report/latex/references.bib) | Mixed Static CMOS / Domino high-fan-in gate sequences with delay elements | Examines hybrid logic for targeted low-power, high-speed gate chains | Phase ordering and inserted delay elements constrain where hybrid chains apply |
| **Saxena et al. (2017)** [[Ref 11]](../report/latex/references.bib) | Four-bit RCA built from alternative MCML full-adder topologies | Evaluates complete cascaded adders; demonstrates why both cell-level and chain-level behavior matter | MCML operates via current-mode steering with a distinct static power profile |
| **Garg & Gupta (2018)** [[Ref 12]](../report/latex/references.bib) | Foot-driven stack-transistor Domino OR gates (2–16 inputs) in PTM 32 nm HSPICE | Reports up to 59.47% lower power than CSK-DL and up to 44.6% lower delay than M-HSCD | Applies specifically to wide OR gates; stacking and keeper choices trade off delay vs. noise |

## Cross-Paper Synthesis

Across these twelve studies, four engineering themes frame this 90 nm RCA evaluation:
1. **Separate design objectives:** Low transistor count, low energy, high speed, and noise immunity do not automatically align in one topology.
2. **Cascaded vs. isolated behavior:** Cell-level metrics alone can be misleading; carry-chain loading and restoration across stages determine real RCA timing.
3. **Domino trade-offs:** Eliminating PMOS pull-up trees accelerates evaluation, but precharge/evaluate clock power, keeper contention, charge sharing, and intradie variation constrain energy efficiency.
4. **Clocked CMOS overhead:** $\text{C}^2\text{MOS}$ enables phase-controlled sequencing and pipelining, at the cost of complementary clock capacitance and additional device count.
