;; ==============================================================================
;; Cadence Virtuoso SKILL Script: Automatically Generate Clean Symbols for RCA Library
;; Places Inputs on Left, Outputs on Right, VDD on Top, GND on Bottom
;; ==============================================================================

procedure( createCleanSymbol(libName cellName)
  let((pinList ports)
    printf(">> Creating clean symbol for %s/%s...\n" libName cellName)
    
    ;; Delete existing symbol if it exists
    when(ddGetObj(libName cellName "symbol")
      ddDeleteObj(ddGetObj(libName cellName "symbol"))
    )

    ;; Extract pin list from schematic
    pinList = schSchemToPinList(libName cellName "schematic")
    
    when(pinList
      ports = pinList->ports
      when(ports
        foreach(port ports
          cond(
            (member(port->name '("a" "b" "cin" "a0" "a1" "a2" "a3" "b0" "b1" "b2" "b3" "clk" "clkb"))
              port->accessDir = "left"
            )
            (member(port->name '("sum" "cout" "s0" "s1" "s2" "s3"))
              port->accessDir = "right"
            )
            (equal(port->name "vdd")
              port->accessDir = "top"
            )
            (equal(port->name "gnd")
              port->accessDir = "bottom"
            )
            (t
              port->accessDir = "left"
            )
          )
        )
      )
      
      ;; Build clean symbol view
      schPinListToSymbol(libName cellName "symbol" pinList)
      printf(">> [SUCCESS] Created clean symbol for %s/%s\n" libName cellName)
    )
  )
)

;; Procedure to fix all RCA cells in the given library (default: "rca")
procedure( fixAllRCASymbols(@optional (libName "rca"))
  let((cells)
    cells = '("FA_STATIC" "RCA4_STATIC" "FA_DOMINO" "RCA4_DOMINO" "FA_C2MOS" "RCA4_C2MOS")
    printf("============================================================\n")
    printf("Fixing all RCA Symbols in Library: %s\n" libName)
    printf("============================================================\n")
    foreach(cell cells
      if(ddGetObj(libName cell "schematic") then
        createCleanSymbol(libName cell)
      else
        printf(">> [INFO] Cell %s/%s schematic not found, skipping.\n" libName cell)
      )
    )
    printf("============================================================\n")
    printf("Done! Clean symbols created for all imported RCA cells.\n")
    printf("============================================================\n")
  )
)

;; Automatically run for default library "rca" upon loading
fixAllRCASymbols("rca")
