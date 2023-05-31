
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

;; Read next byte from hl, incrementing hl itself
@nextByte:
    ld a, :@nextByte
    call readByteFromW7ActiveBankAndReturn
    inc hl
    ret


; @param c: Unicode codepoint, upper 1 byte
; @param de: Unicode codepoint, lower 2 bytes
; @return de: Glyph index, as in font table
getFontId:
	ld a, c
	and a, $1f
	rlca
	rlca
	rlca
	ld c, a
	ld a, d
	and a, $e0
	rrca
	rrca
	rrca
	rrca
	rrca
	or a, c

	add a, :gfx_font_unicode_table
	push af
	sla e
	rl d
	ld a, d
	and a, $3f
	or a, $40
	ld h, a
	ld a, e
	ld l, a
	pop af
	push af

    ld b, a
    ld a, :getFontId
    call readByteFromBankAndReturn
    ld d, a
	inc hl
    ld a, :getFontId
    call readByteFromBankAndReturn
	ld e, a
	pop af

	ret


; @param de: Glyph index as in font table
; @return a: Bank number that tile is in
; @return hl: Offset of the tile
getFontOffset:
	ld a, d			; First 6 bits of first byte for bank id
	and a, $fc
	rrca
	rrca
	add a, :gfx_font_unicode
	push af
	ld a, d
	and a, $03
	ld h, a
	ld a, e
	ld l, a			; Transfer other bits to hl

	sla l
	rl h
	sla l
	rl h
	sla l
	rl h
	sla l
	rl h

	ld a, h
	add a, $40		; Add $4000 to hl
	ld h, a
	pop af
	ret
