// x = (y - z) + 4 * (i - j) + k

.data
k: 8
ad: 0x48
hi: 0x15

.text
ldi r1, 0x3     // y = 3
ldi r2, 0x2     // z = 2
ldi r3, 0x6     // i = 6
ldi r4, 0x3     // j = 3
ldi r8, ad


quit

