    org $3000

    pshs a,b,x,y,u
    ldx #$400
    leay [dados]
    
    bsr uncompress
    puls y,u,x,b,a
    rts
    
uncompress:    
    ; y aponta para os dados compactados
    ; a, b, u e x sao destruidos
    ldd, y++
    leau d,x
    pshs u
    lda, y+
    pshs a
prox:    
    lda, y+
    cmpa, s
    beq dc
sto:    
    sta ,x+
    cmpx 1,s
    blo prox
    bra fim    
    
dc:
    lda ,y+
    bne dx
    lda, s
    bra sto
dx:    
    ldb, y+
    leau a,x
lp1:
    lda, u+
    sta, x+
    decb
    bne lp1
    cmpx 1,s
    blo prox    
fim:
    puls u
    puls a
    rts
    
dados:    
