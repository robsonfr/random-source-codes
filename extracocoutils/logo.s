    org $3000
    leay [dados]
    ldx #$400
lp1:
    ldd, y++
    std, x++
    cmpx #$600
    bne lp1
lp2:
    jsr [$a000]
    beq lp2
    rts


dados:
