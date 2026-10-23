* Standard 90nm BSIM4 Bulk CMOS Model Card (1.0V Nominal)
* Process: 90nm CMOS, Tox = 2.1nm, Vdd = 1.0V

.model nmos_90nm nmos level=54 version=4.5
+ vth0=0.25 toxe=2.1e-9 toxm=2.1e-9 lint=10e-9 wint=5e-9
+ u0=0.045 rdsw=150 vsat=1.1e5 lpe0=5e-9
+ cgdo=3.0e-10 cgso=3.0e-10 capmod=2

.model pmos_90nm pmos level=54 version=4.5
+ vth0=-0.22 toxe=2.2e-9 toxm=2.2e-9 lint=10e-9 wint=5e-9
+ u0=0.012 rdsw=250 vsat=8.5e4 lpe0=5e-9
+ cgdo=3.5e-10 cgso=3.5e-10 capmod=2
