// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(RESTART)
@SCREEN
D = A
@0
M = D	// screen base address(start) at RAM[0].

(KBDCHECK)
@KBD
D = M
@BLACK
D;JGT	// jump if key is pressed.
@WHITE
D;JEQ	// else white-out the screen.

@KBDCHECK  // loop
0;JMP

(BLACK)
@1
M = -1	// to black-out the pixel. (in binary : 1111111111111111)
@CHANGE
0;JMP

(WHITE)
@1
M = 0	// to set pixel to white.
@CHANGE
0;JMP

(CHANGE)
@1	// What to change to.
D = M	// black or white? 

@0
A = M	// select a pixel
M = D	// change selected pixel

@0
D = M + 1	// address of next pixel.
@KBD
D = A - D	// KBD - SCREEN = A

@0
M = M + 1	// next pixel
A = M

@CHANGE
D;JGT	// while screen is not black completely, continue loop.

@RESTART  // when screen is completely black -> goto top of program.
0;JMP