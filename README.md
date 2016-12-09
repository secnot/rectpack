# rectpack
Python 2D rectangle packing library

![alt tag](docs/maxrects.png)

Usage
=====

Packing rectangles in a number of bins is very simple:

```python
from rectpack import newPacker

rectangles = [(100, 30), (40, 60), (30, 30), .....]
bins = [(300, 450), (80, 40), ...]

p = newPacker()

# Add all the rectangles to be packed
for r in rectangles:
	p.add_rect(*r)

# Add bins where the rectangles will be placed
for b in bins:
	p.add_bin(*b)

# Do packing
p.pack()

# Iterate through each bin and obtain a list of rectangle positions
# format [(x0, y0, w0, h0, rid0), (x1, y1, w1, h1, rid1), ...]
#	x -> Lower-left corner x coordinate
#	y -> Lower-left forner y coordinate
#	w -> Width
#	h -> Height
#	rid -> User asigned id or None
for b in p:
	b.get_rect_list()

```

Tests
=====

Float
=====

Most of the packing algorithms implemented have problems with float rounding 
errors which can result in collisions.
If you need to use floats just convert them to fixed-point using Decimal 
rounding up so the actual rectangle size is always smaller than the conversion.
Rectpack provides helper funcion **float2dev** for this task:

```python
	from rectpack import float2dec, newPacker

	float_rects = [...] 
	dec_rects = [(float2dec(r[0], 3), float2dec(r[1], 3)) for r in float_rects]
				
	p = newPacker()
	
	....
```




Enclose
=======

Enclose rectangles


References
==========

[1] Jukka Jylang - A Thousand Ways to Pack the Bin - A Practical Approach to Two-Dimensional
Rectangle Bin Packing (2010)

[2] Huang, E. Korf - Optimal Rectangle Packing: An Absolute Placement Approach (2013)
