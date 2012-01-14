; The following code can be used to uncompress and play a 2500 Hz raw audio data
; The numbers in the comments below are the number of cycles

                       org $E828
                       pshs a,x,y,u
                       ldx #fimsnd
                       leax 3,x
                       ldu #$2200
                       ldy #5000
                       jsr $e7ad    ; uncompressing routine
                       
                       lda   $ff01
                       anda  #$f7
                       sta   $ff01                       
                       
                       lda   $ff03
                       anda  #$f7
                       sta   $ff03
                       
                       lda   $ff23
                       ora   #8
                       sta   $ff23
                       
prox:                  ldx   #41        ; 3                    
                       lda   ,u+       ; 4 + 2
                       anda  #$fc      ; 2
                       sta   $ff20     ; 5
delay:                 leax  -1,x      ; 4 + 1
                       bne delay       ; 3
                       nop             ; 2
                       nop             ; 2
                       nop             ; 2
                       leay -1,y       ; 4 + 1
                       bne prox        ; 3 
esptec:                jsr [$a000]	   ; POLCAT function in the BIOS
                       beq esptec
                       puls u,y,x,a
fimsnd:                jmp $C175
                       
                       
                       