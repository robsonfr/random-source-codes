    org $3000
    
    pshs a,x
    ldx #$1c00
    orcc #$50
lp1:    
    sta $ffde
    lda, x
    sta $ffdf
    sta, x+
    cmpx #$FF00
    bne lp1
    puls x,a
    sta $ffdf
    andcc #$AF
    rts
    