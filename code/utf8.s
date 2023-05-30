
; @param hl: Start address to read from
; @return c: Unicode codepoint, upper 1 byte
; @return de: Unicode codepoint, lower 2 bytes
readUTF8:
    ld c, $00
    ld d, $00

    call @nextByte

    bit 7, a
    jr z, @singleByte
    bit 5, a
    jr z, @doubleByte
    bit 4, a
    jr z, @tripleByte
    bit 3, a
    jr z, @quadByte
    jr @end

@singleByte:
    and a, $7f
    ld e, a
    jr @end

@doubleByte:
    push af
    and a, $1c
    rrca
    rrca
    ld d, a
    jr @lastByte

@tripleByte:
    and a, $0f
    rlca
    rlca
    rlca
    rlca
    ld d, a

    call @nextByte

    push af
    and a, $3c
    rrca
    rrca
    or d
    ld d, a

    jr @lastByte

@quadByte:
    and a, $07
    rlca
    rlca
    ld c, a

    call @nextByte

    push af
    and a, $30
    rrca
    rrca
    rrca
    rrca
    or c
    ld c, a

    pop af
    and a, $0f
    rlca
    rlca
    rlca
    rlca
    ld d, a

    call @nextByte

    push af
    and a, $3c
    rrca
    rrca
    or d
    ld d, a

    jr @lastByte

@lastByte:
    pop af
    and a, $03
    rrca
    rrca
    ld e, a

    call @nextByte

    and a, $3f
    or e
    ld e, a

@end:
    ret

@nextByte:
    ld a, $4f
    call readByteFromW7ActiveBankAndReturn
    inc hl
    ret
