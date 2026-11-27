# Standalone Ngspice Quick-Verification Suite (PTM 90nm)

This directory provides a **portable, open-source SPICE testbench harness** using `ngspice` and a 90 nm BSIM4 Predictive Technology Model ([`models/ptm_90nm.pm`](models/ptm_90nm.pm)) so anyone can inspect or run functional carry-ripple transient simulations without a Cadence Virtuoso license.

> **Important Distinction:**
> The authoritative benchmark numbers, schematics, and transient outputs reported in the root [`README.md`](../README.md), [`analysis/`](../analysis/), and [`report/case_study.pdf`](../report/case_study.pdf) were simulated in **Cadence Virtuoso IC6.1.7 / Spectre** using the **`gpdk090`** PDK and the exact netlist in [`cadence/rca_all_designs.sp`](../cadence/rca_all_designs.sp) (Static CMOS: 28T/FA, $\text{C}^2\text{MOS}$: 32T/FA, Domino: 26T/FA).
>
> By contrast, `standalone_simulation/` uses PTM 90 nm BSIM4 parameters and simplified dynamic/clocked test decks for open-source `ngspice` portability.

## Prerequisites

- Python 3.8+ (`matplotlib`, `numpy`)
- `ngspice` installed natively on `PATH` (or in WSL Ubuntu on Windows)

## Usage

```bash
cd standalone_simulation
python runner.py
```

Running `runner.py` regenerates clean relative-path `.cir` decks under `netlists/`, executes transient simulations if `ngspice` is installed, extracts carry-ripple timing, and saves comparison waveforms to `plots/rca_carry_ripple_comparison.png`.
