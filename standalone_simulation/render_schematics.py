#!/usr/bin/env python3
"""
Generate transistor-level schematic diagrams for Review 2:
1. Static CMOS Full Adder
2. Domino Logic Full Adder (with keeper)
3. C²MOS Full Adder (clock-gated)
"""

import os
import schemdraw
import schemdraw.elements as elm
import schemdraw.logic as logic

ARTIFACT_DIR = r"C:\Users\saksh\.gemini\antigravity\brain\c3a7bf7a-fd84-45c5-aaa2-389121665ab1"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def draw_domino():
    with schemdraw.Drawing(file=os.path.join(ARTIFACT_DIR, "domino_schematic.png"), show=False) as d:
        d.config(fontsize=11, font='sans-serif', unit=2.5)
        
        # Title
        d += elm.Label().label('Domino Logic 1-Bit Full Adder (90nm Node)', loc='top').at((3.5, 6.8))
        
        # VDD Rail
        d += elm.Vdd().at((1.5, 5.5)).label('VDD (1.0V)')
        d += elm.Vdd().at((4.5, 5.5)).label('VDD (1.0V)')
        
        # Precharge PMOS
        mp1 = elm.PFet(bulk=False).at((1.5, 4.0)).label('M_pre\n(W=420n)', loc='left')
        d += mp1
        d += elm.Line().at(mp1.gate).left(0.8).label('CLK (Phi)', loc='left')
        
        # Weak Keeper PMOS
        mp_kp = elm.PFet(bulk=False).at((4.5, 4.0)).label('M_keeper\n(W=100n)', loc='right')
        d += mp_kp
        
        # Dynamic Node
        d += elm.Line().at(mp1.drain).to((3.0, 3.0))
        d += elm.Line().at(mp_kp.drain).to((3.0, 3.0))
        d += elm.Dot().at((3.0, 3.0)).label('Dynamic Node\n(V_dyn)', loc='top')
        
        # NMOS Evaluate Network Box
        d += elm.Line().at((3.0, 3.0)).down(0.8)
        d += elm.Rect(w=3.2, h=1.6).at((1.4, 0.6)).label('NMOS Evaluate Network\n(Carry: AB + BCin + ACin)\n(Sum: A ^ B ^ Cin)', loc='center')
        
        # Evaluation Foot Transistor
        mn_foot = elm.NFet(bulk=False).at((3.0, -1.0)).label('M_foot\n(W=360n)', loc='left')
        d += mn_foot
        d += elm.Line().at(mn_foot.gate).left(0.8).label('CLK (Phi)', loc='left')
        d += elm.Ground().at(mn_foot.source)
        
        # Static Output Inverter
        d += elm.Line().at((3.0, 3.0)).right(1.5)
        inv = logic.Not().right().label('Static Inverter\n(Wp=420n, Wn=120n)', loc='top')
        d += inv
        d += elm.Line().at(inv.out).right(1.2).label('Out (Sum / Cout)\n[Monotonic Rising]', loc='right')
        
        # Keeper feedback line
        d += elm.Line().at(inv.out).up(1.5)
        d += elm.Line().to(mp_kp.gate)

def draw_c2mos():
    with schemdraw.Drawing(file=os.path.join(ARTIFACT_DIR, "c2mos_schematic.png"), show=False) as d:
        d.config(fontsize=11, font='sans-serif', unit=2.5)
        
        d += elm.Label().label('C²MOS Stage (Clock-Gated Inverting Architecture)', loc='top').at((3.0, 7.5))
        
        # VDD
        d += elm.Vdd().at((3.0, 6.5)).label('VDD (1.0V)')
        
        # Top PMOS: Data input
        mp1 = elm.PFet(bulk=False).at((3.0, 5.0)).label('M1 (Logic)\nW=420n', loc='left')
        d += mp1
        d += elm.Line().at(mp1.gate).left(0.8).label('Data In', loc='left')
        
        # Clocked PMOS: Gated by CLK_b (Phi_bar)
        mp2 = elm.PFet(bulk=False).at((3.0, 3.2)).label('M2 (Clock Gate)\nW=420n', loc='left')
        d += mp2
        d += elm.Line().at(mp2.gate).left(0.8).label('CLK_b (Phi_bar)', loc='left')
        
        # Output Node
        d += elm.Line().at(mp2.drain).down(0.4)
        d += elm.Dot().at((3.0, 2.8)).label('Gated Output', loc='right')
        d += elm.Line().at((3.0, 2.8)).right(1.5).label('To Stage 2 (Anti-phase)', loc='right')
        
        # Clocked NMOS: Gated by CLK (Phi)
        mn1 = elm.NFet(bulk=False).at((3.0, 1.4)).label('M3 (Clock Gate)\nW=360n', loc='left')
        d += mn1
        d += elm.Line().at(mn1.gate).left(0.8).label('CLK (Phi)', loc='left')
        
        # Bottom NMOS: Data input
        mn2 = elm.NFet(bulk=False).at((3.0, -0.4)).label('M4 (Logic)\nW=360n', loc='left')
        d += mn2
        d += elm.Line().at(mn2.gate).left(0.8).label('Data In', loc='left')
        d += elm.Ground().at(mn2.source)

def draw_static_cmos():
    with schemdraw.Drawing(file=os.path.join(ARTIFACT_DIR, "static_cmos_schematic.png"), show=False) as d:
        d.config(fontsize=11, font='sans-serif', unit=2.5)
        
        d += elm.Label().label('Static CMOS Full Adder Architecture (28-Transistor Mirror)', loc='top').at((3.5, 6.5))
        
        d += elm.Vdd().at((2.0, 5.5)).label('VDD (1.0V)')
        d += elm.Vdd().at((5.5, 5.5)).label('VDD (1.0V)')
        
        # Pull Up Networks
        d += elm.Rect(w=2.6, h=1.6).at((0.7, 3.2)).label('Carry PUN (5 PMOS)\n(A*B + Cin*(A+B))\nWp = 420 nm', loc='center')
        d += elm.Rect(w=2.6, h=1.6).at((4.2, 3.2)).label('Sum PUN (7 PMOS)\n(Cout_b*(A+B+Cin)+A*B*Cin)\nWp = 420 nm', loc='center')
        
        # Mid Nodes & Inverters
        d += elm.Line().at((2.0, 3.2)).down(0.8)
        d += elm.Dot().at((2.0, 2.4)).label('Cout_bar', loc='left')
        inv_c = logic.Not().at((2.0, 2.4)).right(1.2).label('Cout', loc='right')
        d += inv_c
        
        d += elm.Line().at((5.5, 3.2)).down(0.8)
        d += elm.Dot().at((5.5, 2.4)).label('Sum_bar', loc='left')
        inv_s = logic.Not().at((5.5, 2.4)).right(1.2).label('Sum', loc='right')
        d += inv_s
        
        # Pull Down Networks
        d += elm.Rect(w=2.6, h=1.6).at((0.7, 0.2)).label('Carry PDN (5 NMOS)\n(A*B + Cin*(A+B))\nWn = 360 nm', loc='center')
        d += elm.Rect(w=2.6, h=1.6).at((4.2, 0.2)).label('Sum PDN (7 NMOS)\n(Cout*(A+B+Cin)+A*B*Cin)\nWn = 360 nm', loc='center')
        
        d += elm.Ground().at((2.0, 0.2))
        d += elm.Ground().at((5.5, 0.2))

if __name__ == '__main__':
    draw_domino()
    draw_c2mos()
    draw_static_cmos()
    print("Schematics generated successfully in artifact directory!")
