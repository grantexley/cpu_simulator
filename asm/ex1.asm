.data
k: 0x0024 //set k
x: 0x21   //set x
grant: 0000


.text
ldi r0, 0xf0
ldi r1, 7
st r1, r0, 0
ldi r1, 8
st r1, r0, 1
ldi r1, 9
st r1, r0, 2

ldi r0, grant
ldi r0, k
ldi r0, x
ldi r0, apple
quit

