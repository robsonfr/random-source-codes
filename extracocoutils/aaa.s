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
    db 0x92
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x90
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x84
    db 0x86
    db 0x86
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x82
    db 0x84
    db 0x84
    db 0x80
    db 0x82
    db 0x82
    db 0x82
    db 0x80
    db 0x82
    db 0x82
    db 0x82
    db 0x82
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x82
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x84
    db 0x93
    db 0x80
    db 0x8c
    db 0x80
    db 0x85
    db 0x85
    db 0x80
    db 0x82
    db 0x91
    db 0x80
    db 0x8a
    db 0x85
    db 0x8a
    db 0x80
    db 0x8f
    db 0x80
    db 0x85
    db 0x8a
    db 0x80
    db 0x8f
    db 0x80
    db 0x80
    db 0x80
    db 0x8f
    db 0x8f
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x89
    db 0x8e
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x88
    db 0x8d
    db 0x87
    db 0x8c
    db 0x80
    db 0x80
    db 0x85
    db 0x8a
    db 0x80
    db 0x8f
    db 0x80
    db 0x85
    db 0x8a
    db 0x80
    db 0x8f
    db 0x80
    db 0x80
    db 0x85
    db 0x8a
    db 0x87
    db 0x8a
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x91
    db 0x86
    db 0x8e
    db 0x88
    db 0x8d
    db 0x8a
    db 0x8b
    db 0x80
    db 0x8f
    db 0x84
    db 0x8c
    db 0x85
    db 0x8a
    db 0x82
    db 0x8f
    db 0x80
    db 0x85
    db 0x8a
    db 0x80
    db 0x8f
    db 0x82
    db 0x82
    db 0x87
    db 0x88
    db 0x85
    db 0x8a
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x80
    db 0x88
    db 0x8d
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x85
    db 0x8a
    