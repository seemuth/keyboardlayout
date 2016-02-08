# keyboardlayout
Keyboard layout generator for https://github.com/blahlicus/animus-family/

This tool allows for automated generation of layout codes for keyboards from
http://uniquekeyboard.com/ . It is not affiliated with uniquekeyboard.com or
blahlicus, but is offered purely in the hope that it will be useful.

# Examples
An example layout file is given in `DivergeIIExample.tsv`.
It provides a QWERTY-ish layout for the [Diverge-II keyboard](http://uniquekeyboard.com/store/split-keyboard/diverge-ii).

These keyboards offer a serial interface for setting layouts, and this tool
automatically produces these serial commands.

To produce the commands for the left-hand board, run:
```
./keyboardlayout.py 5 8 keycodes.tsv DivergeIIExample.tsv -f LEFT
```
and for the right-hand board (which is reversed due to flipping over the PCB):
```
./keyboardlayout.py 5 8 keycodes.tsv DivergeIIExample.tsv -f RIGHT --reverse --command uniqueksetsubkey
```

This will produce the serial commands that will implement the desired layout.

# Layout file syntax
(Note that the Markdown rendering translates the internal TAB characters to
multiple space characters.)
```
LAYOUT 0 LEFT							
ESC	1	2	3	4	5	6	
`	q	w	e	r	t	TV_10_0	
TAB	a	s	d	f	g	TV_10_1	
LEFT_CTRL	z	x	c	v	b	TV_10_2	
LEFT_SHIFT	LEFT_CTRL	LEFT_GUI	LEFT_ALT	PRINTSCREEN	TV_10_3	SPACE	FN
							
LAYOUT 0 RIGHT							
	7	8	9	0	-	=	BACKSPACE
	\	y	u	i	o	p	'
	[	h	j	k	l	;	ENTER
	]	n	m	,	.	UP	/
RIGHT_SHIFT	SPACEFN	BACKSPACE	RIGHT_ALT	RIGHT_CTRL	LEFT	DOWN	RIGHT
							
LAYOUT 1 LEFT							
ESC	F1	F2	F3	F4	F5	F6	
`	F7	F8	F9	F10	F11	F12	
TAB	INSERT		SCROLL_LOCK	NUM_LOCK		TV_10_4	
LEFT_CTRL	PAUSEBREAK		COMPOSE	CAPS_LOCK	TV_10_5	TV_10_6	
LEFT_SHIFT	LEFT_CTRL	LEFT_GUI	LEFT_ALT	TV_10_7	TV_10_8	TV_10_9	FN
							
LAYOUT 1 RIGHT							
	KP_7	KP_8	KP_9	KP_DIVIDE	VOL_DOWN	VOL_UP	DELETE
	KP_4	KP_5	KP_6	KP_MULTIPLY	STOP	PLAY	TV_10_10
	KP_1	KP_2	KP_3	KP_MINUS	PREV	NEXT	ENTER
	KP_0	KP_PERIOD	KP_ENTER	KP_PLUS		PAGEUP	
RIGHT_SHIFT		DELETE	RIGHT_ALT	RIGHT_CTRL	HOME	PAGEDOWN	END
```

A layer's layout starts with ```LAYOUT LAYERNUMBER TAG```.
Subsequent lines specify one key per cell.
Columns are separated by TABs, and rows are specified one per line.

Custom keys can be specified by using ```CUSTOM_TYPE_VALUE```, where
```VALUE``` and ```TYPE``` are used in the keyboard firmware.
```TYPE``` is typically used to differentiate special keys like Fn, SpaceFn, etc.
