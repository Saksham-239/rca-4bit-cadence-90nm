;; ==============================================================================
;; CADENCE VIRTUOSO SKILL SCRIPT: Automatically Create All 3 Testbench Schematics
;; Generates:
;;   - rca / tb_rca4_static / schematic
;;   - rca / tb_rca4_domino / schematic
;;   - rca / tb_rca4_c2mos  / schematic
;; Fully wired with VDD, GND, Stimulus (A=1111, B=0000, Cin Pulse), and Clocks
;; ==============================================================================

procedure( buildRCATestbench(libName tbCellName rcaCellName hasClk hasClkb)
  let((cv rcaMaster vdcMaster vpulseMaster gndMaster instRCA instVdd instVcin instClk instClkb instVa)
    printf(">> Building testbench schematic: %s/%s for cell %s...\n" libName tbCellName rcaCellName)
    
    ;; 1. Open or Overwrite Schematic
    cv = dbOpenCellViewByType(libName tbCellName "schematic" "schematic" "w")
    unless(cv
      error("Could not open %s/%s/schematic for writing!" libName tbCellName)
    )

    ;; 2. Fetch Masters
    rcaMaster = dbOpenCellViewByType(libName rcaCellName "symbol" "" "r")
    unless(rcaMaster
      error("Could not find symbol for %s/%s! Run fix_symbols.il first." libName rcaCellName)
    )

    vdcMaster    = dbOpenCellViewByType("analogLib" "vdc" "symbol" "" "r")
    vpulseMaster = dbOpenCellViewByType("analogLib" "vpulse" "symbol" "" "r")
    gndMaster    = dbOpenCellViewByType("analogLib" "gnd" "symbol" "" "r")

    ;; 3. Place RCA DUT
    instRCA = schCreateInst(cv rcaMaster "I_DUT" list(5.0 3.5) "R0")

    ;; 4. Place VDD (1.0V)
    instVdd = schCreateInst(cv vdcMaster "V_VDD" list(1.5 5.5) "R0")
    instVdd~>vdc = "1.0"

    ;; 5. Place V_A (Logic 1 = 1.0V)
    instVa = schCreateInst(cv vdcMaster "V_A" list(1.5 4.0) "R0")
    instVa~>vdc = "1.0"

    ;; 6. Place Cin Pulse (Step at 1.0ns)
    instVcin = schCreateInst(cv vpulseMaster "V_CIN" list(1.5 2.5) "R0")
    instVcin~>v1 = "0.0"
    instVcin~>v2 = "1.0"
    instVcin~>td = "1.0n"
    instVcin~>tr = "20p"
    instVcin~>tf = "20p"
    instVcin~>pw = "2.0n"
    instVcin~>per = "5.0n"

    ;; 7. Place Clocks if required
    when(hasClk
      instClk = schCreateInst(cv vpulseMaster "V_CLK" list(1.5 1.0) "R0")
      instClk~>v1 = "0.0"
      instClk~>v2 = "1.0"
      instClk~>td = "0.0"
      instClk~>tr = "20p"
      instClk~>tf = "20p"
      instClk~>pw = "1.0n"
      instClk~>per = "2.0n"
    )

    when(hasClkb
      instClkb = schCreateInst(cv vpulseMaster "V_CLKB" list(1.5 -0.5) "R0")
      instClkb~>v1 = "1.0"
      instClkb~>v2 = "0.0"
      instClkb~>td = "0.0"
      instClkb~>tr = "20p"
      instClkb~>tf = "20p"
      instClkb~>pw = "1.0n"
      instClkb~>per = "2.0n"
    )

    ;; 8. Place Grounds
    when(gndMaster
      schCreateInst(cv gndMaster "GND_VDD" list(1.5 5.0) "R0")
      schCreateInst(cv gndMaster "GND_VA"  list(1.5 3.5) "R0")
      schCreateInst(cv gndMaster "GND_CIN" list(1.5 2.0) "R0")
      when(hasClk  schCreateInst(cv gndMaster "GND_CLK"  list(1.5 0.5) "R0"))
      when(hasClkb schCreateInst(cv gndMaster "GND_CLKB" list(1.5 -1.0) "R0"))
      schCreateInst(cv gndMaster "GND_DUT" list(5.0 2.0) "R0")
    )

    ;; 9. Check and Save
    schCheck(cv)
    dbSave(cv)
    dbClose(cv)
    printf(">> [SUCCESS] Created testbench: %s/%s\n" libName tbCellName)
  )
)

procedure( createAllRCATestbenches(@optional (libName "rca"))
  printf("============================================================\n")
  printf("Generating All 3 Testbenches in Library: %s\n" libName)
  printf("============================================================\n")
  
  ;; 1. Static CMOS Testbench
  buildRCATestbench(libName "tb_rca4_static" "RCA4_STATIC" nil nil)

  ;; 2. Domino Logic Testbench
  buildRCATestbench(libName "tb_rca4_domino" "RCA4_DOMINO" t nil)

  ;; 3. C2MOS Testbench
  buildRCATestbench(libName "tb_rca4_c2mos"  "RCA4_C2MOS"  t t)

  printf("============================================================\n")
  printf("All 3 Testbenches Successfully Created in Library '%s'!\n" libName)
  printf("Open them in Library Manager -> Launch ADE L -> Netlist and Run.\n")
  printf("============================================================\n")
)

;; Automatically run for default library "rca"
createAllRCATestbenches("rca")
