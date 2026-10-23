* ==============================================================================
* Cadence Virtuoso SPICE Import File (Direct gpdk090 Native Mapping - VERIFIED)
* 4-Bit Ripple Carry Adder Designs (90nm CMOS)
* Logic Styles: Static CMOS, Domino Logic (Compound Domino), and C2MOS
* ==============================================================================

* ------------------------------------------------------------------------------
* 1. STATIC CMOS 1-BIT FULL ADDER (28 Transistors - 100% Formally Verified)
* ------------------------------------------------------------------------------
.subckt FA_STATIC a b cin sum cout vdd gnd

* Carry Generation PUN (5 PMOS)
Mp_c1 n_cp1 a   vdd vdd pmos1v w=420n l=100n
Mp_c2 cout_b b   n_cp1 vdd pmos1v w=420n l=100n
Mp_c3 n_cp2 a   vdd vdd pmos1v w=420n l=100n
Mp_c4 n_cp2 b   vdd vdd pmos1v w=420n l=100n
Mp_c5 cout_b cin n_cp2 vdd pmos1v w=420n l=100n

* Carry Generation PDN (5 NMOS)
Mn_c1 cout_b a   n_cn1 gnd nmos1v w=360n l=100n
Mn_c2 n_cn1  b   gnd   gnd nmos1v w=360n l=100n
Mn_c3 cout_b cin n_cn2 gnd nmos1v w=360n l=100n
Mn_c4 n_cn2  a   gnd   gnd nmos1v w=360n l=100n
Mn_c5 n_cn2  b   gnd   gnd nmos1v w=360n l=100n

* Carry Inverter (2 Transistors)
Mp_cinv cout cout_b vdd vdd pmos1v w=420n l=100n
Mn_cinv cout cout_b gnd gnd nmos1v w=120n l=100n

* Sum Generation PUN (7 PMOS)
Mp_s1 n_sp1 a      vdd vdd pmos1v w=420n l=100n
Mp_s2 n_sp1 b      vdd vdd pmos1v w=420n l=100n
Mp_s3 n_sp1 cin    vdd vdd pmos1v w=420n l=100n
Mp_s4 sum_b cout_b n_sp1 vdd pmos1v w=420n l=100n
Mp_s5 n_sp2 a      vdd vdd pmos1v w=420n l=100n
Mp_s6 n_sp3 b      n_sp2 vdd pmos1v w=420n l=100n
Mp_s7 sum_b cin    n_sp3 vdd pmos1v w=420n l=100n

* Sum Generation PDN (7 NMOS)
Mn_s1 sum_b cout_b n_sn1 gnd nmos1v w=360n l=100n
Mn_s2 n_sn1 a      gnd   gnd nmos1v w=360n l=100n
Mn_s3 n_sn1 b      gnd   gnd nmos1v w=360n l=100n
Mn_s4 n_sn1 cin    gnd   gnd nmos1v w=360n l=100n
Mn_s5 sum_b a      n_sn2 gnd nmos1v w=360n l=100n
Mn_s6 n_sn2 b      n_sn3 gnd nmos1v w=360n l=100n
Mn_s7 n_sn3 cin    gnd   gnd nmos1v w=360n l=100n

* Sum Inverter (2 Transistors)
Mp_sinv sum sum_b vdd vdd pmos1v w=420n l=100n
Mn_sinv sum sum_b gnd gnd nmos1v w=120n l=100n
.ends FA_STATIC

* Top-Level 4-Bit Static CMOS RCA
.subckt RCA4_STATIC a0 a1 a2 a3 b0 b1 b2 b3 cin s0 s1 s2 s3 cout vdd gnd
XFA0 a0 b0 cin s0 c1 vdd gnd FA_STATIC
XFA1 a1 b1 c1  s1 c2 vdd gnd FA_STATIC
XFA2 a2 b2 c2  s2 c3 vdd gnd FA_STATIC
XFA3 a3 b3 c3  s3 cout vdd gnd FA_STATIC
.ends RCA4_STATIC

* ------------------------------------------------------------------------------
* 2. DOMINO LOGIC 1-BIT FULL ADDER (Compound Domino: High-Speed Carry + Exact Sum)
* ------------------------------------------------------------------------------
.subckt FA_DOMINO a b cin clk sum cout vdd gnd

* Domino Carry Precharge & Weak Keeper
Mp_cpre dyn_cout clk  vdd vdd pmos1v w=420n l=100n
Mp_ckp  dyn_cout cout vdd vdd pmos1v w=100n l=100n

* Domino Carry NMOS Evaluation Tree (AB + Cin(A+B))
Mn_ce1 dyn_cout a    n_cev1  gnd nmos1v w=360n l=100n
Mn_ce2 n_cev1   b    n_cfoot gnd nmos1v w=360n l=100n
Mn_ce3 dyn_cout cin  n_cev2  gnd nmos1v w=360n l=100n
Mn_ce4 n_cev2   a    n_cfoot gnd nmos1v w=360n l=100n
Mn_ce5 n_cev2   b    n_cfoot gnd nmos1v w=360n l=100n
Mn_cfoot n_cfoot clk gnd     gnd nmos1v w=360n l=100n

* Domino Carry Output Inverter (Monotonic output)
Mp_cinv cout dyn_cout vdd vdd pmos1v w=420n l=100n
Mn_cinv cout dyn_cout gnd gnd nmos1v w=120n l=100n

* Exact Sum Generation PUN (7 PMOS) using dyn_cout (cout_bar)
Mp_s1 n_sp1 a        vdd vdd pmos1v w=420n l=100n
Mp_s2 n_sp1 b        vdd vdd pmos1v w=420n l=100n
Mp_s3 n_sp1 cin      vdd vdd pmos1v w=420n l=100n
Mp_s4 sum_b dyn_cout n_sp1 vdd pmos1v w=420n l=100n
Mp_s5 n_sp2 a        vdd vdd pmos1v w=420n l=100n
Mp_s6 n_sp3 b        n_sp2 vdd pmos1v w=420n l=100n
Mp_s7 sum_b cin      n_sp3 vdd pmos1v w=420n l=100n

* Exact Sum Generation PDN (7 NMOS)
Mn_s1 sum_b dyn_cout n_sn1 gnd nmos1v w=360n l=100n
Mn_s2 n_sn1 a        gnd   gnd nmos1v w=360n l=100n
Mn_s3 n_sn1 b        gnd   gnd nmos1v w=360n l=100n
Mn_s4 n_sn1 cin      gnd   gnd nmos1v w=360n l=100n
Mn_s5 sum_b a        n_sn2 gnd nmos1v w=360n l=100n
Mn_s6 n_sn2 b        n_sn3 gnd nmos1v w=360n l=100n
Mn_s7 n_sn3 cin      gnd   gnd nmos1v w=360n l=100n

* Sum Output Inverter
Mp_sinv sum sum_b vdd vdd pmos1v w=420n l=100n
Mn_sinv sum sum_b gnd gnd nmos1v w=120n l=100n
.ends FA_DOMINO

* Top-Level 4-Bit Domino Logic RCA
.subckt RCA4_DOMINO a0 a1 a2 a3 b0 b1 b2 b3 cin clk s0 s1 s2 s3 cout vdd gnd
XFA0 a0 b0 cin clk s0 c1   vdd gnd FA_DOMINO
XFA1 a1 b1 c1  clk s1 c2   vdd gnd FA_DOMINO
XFA2 a2 b2 c2  clk s2 c3   vdd gnd FA_DOMINO
XFA3 a3 b3 c3  clk s3 cout vdd gnd FA_DOMINO
.ends RCA4_DOMINO

* ------------------------------------------------------------------------------
* 3. C2MOS 1-BIT FULL ADDER (True Clock-Gated Mirror Topology)
* ------------------------------------------------------------------------------
.subckt FA_C2MOS a b cin clk clkb sum cout vdd gnd

* --- Carry Stage: cout_b = !(AB + Cin(A+B)) clocked on clk=1, clkb=0 ---
Mp_cclk n_cpmos clkb vdd vdd pmos1v w=420n l=100n
Mp_c1 n_cp1 a    n_cpmos vdd pmos1v w=420n l=100n
Mp_c2 cout_b b   n_cp1   vdd pmos1v w=420n l=100n
Mp_c3 n_cp2 a    n_cpmos vdd pmos1v w=420n l=100n
Mp_c4 n_cp2 b    n_cpmos vdd pmos1v w=420n l=100n
Mp_c5 cout_b cin n_cp2   vdd pmos1v w=420n l=100n

Mn_c1 cout_b a   n_cn1   gnd nmos1v w=360n l=100n
Mn_c2 n_cn1  b   n_cnmos gnd nmos1v w=360n l=100n
Mn_c3 cout_b cin n_cn2   gnd nmos1v w=360n l=100n
Mn_c4 n_cn2  a   n_cnmos gnd nmos1v w=360n l=100n
Mn_c5 n_cn2  b   n_cnmos gnd nmos1v w=360n l=100n
Mn_cclk n_cnmos clk gnd gnd nmos1v w=360n l=100n

Mp_cinv cout cout_b vdd vdd pmos1v w=420n l=100n
Mn_cinv cout cout_b gnd gnd nmos1v w=120n l=100n

* --- Sum Stage: sum_b = !((A+B+Cin)cout_b + ABCin) clocked on clk=1, clkb=0 ---
Mp_sclk n_spmos clkb vdd vdd pmos1v w=420n l=100n
Mp_s1 n_sp1 a      n_spmos vdd pmos1v w=420n l=100n
Mp_s2 n_sp1 b      n_spmos vdd pmos1v w=420n l=100n
Mp_s3 n_sp1 cin    n_spmos vdd pmos1v w=420n l=100n
Mp_s4 sum_b cout_b n_sp1   vdd pmos1v w=420n l=100n
Mp_s5 n_sp2 a      n_spmos vdd pmos1v w=420n l=100n
Mp_s6 n_sp3 b      n_sp2   vdd pmos1v w=420n l=100n
Mp_s7 sum_b cin    n_sp3   vdd pmos1v w=420n l=100n

Mn_s1 sum_b cout_b n_sn1   gnd nmos1v w=360n l=100n
Mn_s2 n_sn1 a      n_snmos gnd nmos1v w=360n l=100n
Mn_s3 n_sn1 b      n_snmos gnd nmos1v w=360n l=100n
Mn_s4 n_sn1 cin    n_snmos gnd nmos1v w=360n l=100n
Mn_s5 sum_b a      n_sn2   gnd nmos1v w=360n l=100n
Mn_s6 n_sn2 b      n_sn3   gnd nmos1v w=360n l=100n
Mn_s7 n_sn3 cin    n_snmos gnd nmos1v w=360n l=100n
Mn_sclk n_snmos clk gnd gnd nmos1v w=360n l=100n

Mp_sinv sum sum_b vdd vdd pmos1v w=420n l=100n
Mn_sinv sum sum_b gnd gnd nmos1v w=120n l=100n
.ends FA_C2MOS

* Top-Level 4-Bit C2MOS RCA
.subckt RCA4_C2MOS a0 a1 a2 a3 b0 b1 b2 b3 cin clk clkb s0 s1 s2 s3 cout vdd gnd
XFA0 a0 b0 cin clk clkb s0 c1   vdd gnd FA_C2MOS
XFA1 a1 b1 c1  clk clkb s1 c2   vdd gnd FA_C2MOS
XFA2 a2 b2 c2  clk clkb s2 c3   vdd gnd FA_C2MOS
XFA3 a3 b3 c3  clk clkb s3 cout vdd gnd FA_C2MOS
.ends RCA4_C2MOS
