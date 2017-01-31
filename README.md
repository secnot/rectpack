# rectpack

Rectpack is a collection of algorithms for solving the 2D knapsack problem,
or packing as much rectangles as possible into another one.

![alt tag](docs/maxrects.png)


## Installation

Just dowload the package or clone the repository, Then install with:

```bash
python setup.py install
```

or using pypi:

```bash
pip install rectpack
```

## Basic Usage

Packing rectangles into a number of bins is very simple:

```python
from rectpack import newPacker

rectangles = [(100, 30), (40, 60), (30, 30),(70, 70), (100, 50), (30, 30)]
bins = [(300, 450), (80, 40), (200, 150)]

packer = newPacker()

# Add the rectangles to packing queue
for r in rectangles:
	packer.add_rect(*r)

# Add the bins where the rectangles will be placed
for b in bins:
	packer.add_bin(*b)

# Start packing
packer.pack()
```

Once the rectangles have been packed the results can be accessed in several ways:

```python
# Obtain number of bins used for packing
nbins = len(packer)

# Index first bin
abin = packer[0]

# Bin dimmensions (bins can be reordered during packing)
width, height = abin.width, abin.height

# Number of rectangles packed into first bin
nrect = len(packer[0])

# Second bin first rectangle
rect = packer[1][0]

# rect is a Rectangle object
x = rect.x # rectangle bottom-left x coordinate
y = rect.y # rectangle bottom-left y coordinate
w = rect.width
h = rect.height
```

But in the majority of cases you will only need a rectangle list:

```python
# Full rectangle list
all_rects = packer.rect_list()
for rect in all_rects:
	b, x, y, w, h, rid = rect

# b - Bin index
# x - Rectangle bottom-left corner x coordinate
# y - Rectangle bottom-left corner y coordinate
# w - Rectangle width
# h - Rectangle height
# rid - User asigned rectangle id or None
```

Lastly all the dimmension (bins and rectangles) must be integers or decimals to avoid
collisions caused by floating point rounding. If your data is floating point use 
float2dec to convert float values to decimals (see float below)


## API

* class **newPacker**([, mode][, bin_algo][, pack_algo][, sort_algo][, rotation])  
  Return a new packer object
  * mode: Mode of operations
    * PackingMode.Offline: The set of rectangles is known beforehand, packing won't
    start until *pack()* is called.
    * PackingMode.Online: The rectangles are unknown at beginning of the job, and
    will be packed as soon as they are added through *add_rect()*.
  * bin_algo: Bin selection heuristic
    * PackingBin.BNF: (Bin Next Fit) If a rectangle doesn't fit into current bin
    close it and try next one.
    * PackingBin.BFF: (Bin First Fit) Pack rectangle into the first bin it fits (without closing)
    * PackingBin.BBF: (Bin Best Fit) Pack rectangle into the bin that gives best fitness.
    * PackingBin.Global:  For each bin pack the rectangle with the best fitness.
  * pack_algo: One of the supported packing algorithms (see supported list below)
  * sort_algo: Sort method used for 
    * SORT_NONE: Rectangles left unsorted.
    * SORT_AREA: Sort by descending area.
    * SORT_PERI: Sort by descending perimeter.
    * SORT_DIFF: Sort by difference of rectangle sides.
    * SORT_SSIDE: Sort by shortest side.
    * SORT_LSIDE: Sort by longest side.
    * SORT_RATIO: Sort by ration between sides.
  * rotation: Enable or disable packing rectangle rotation.


* packer.**add_bin**(width, height[, count])  
  Add empty bin or bins to a packer
  * width: Bin width
  * height: Bin height
  * count: Number of bins to add, 1 by default. It is possible to create infinie bins
  with *count=float("inf")*


* packer.**add_rect**(width, height[, rid])  
  Add rectangle to packing queue
  * width: Rectangle width
  * height: Rectangle height
  * rid: User assigned rectangle id


* packer.**pack**():  
  When in offline mode starts packing process.


* packer.**rect_list**()


## Supported Algorithms

This library implements three of the algorithms described in [1] an excellent
survey of packing algorithms, Skyline, Maxrects, and Guillotine.

To select an specific algorithm for packing:

```python
form rectpack import *

pack = newPacker(pack_algo=MaxRectsBssf)
```

The list of available algorithms is as follows:

* MaxRects
	* MaxRectsBl
	* MaxRectsBssf
	* MaxRectsBaf
	* MaxRectsBlsf

* Skyline
	* SkylineMwf
	* SkylineMwfl
	* SkylineBl
	* SkylineBlWm
	* SkylineMwfWm
	* SkylineMwflWm

* Guillotine
	* GuillotineBssfSas
	* GuillotineBssfLas
	* GuillotineBssfSlas
	* GuillotineBssfLlas
	* GuillotineBssfMaxas
	* GuillotineBssfMinas
	* GuillotineBlsfSas
	* GuillotineBlsfLas
	* GuillotineBlsfSlas
	* GuillotineBlsfLlas
	* GuillotineBlsfMaxas
	* GuillotineBlsfMinas
	* GuillotineBafSas
	* GuillotineBafLas
	* GuillotineBafSlas
	* GuillotineBafLlas
	* GuillotineBafMaxas
	* GuillotineBafMinas

The nomenclature used is the same as described in [1], if you don't want to read
anything I recomend the default algorithm unles the number of rectangles is too
big and the packing is slow, in that case change to the Guillotine that
gives you the best result.

## Testing

Rectpack is thoroughly tested, you can run the tests with:

```bash
python setup.py test
```

or

```bash
python -m unittest discover
```

## Float

If you need to use floats just convert them to fixed-point using a Decimal type,
be carefull rounding up so the actual rectangle size is always smaller than
the conversion. Rectpack provides helper funcion **float2dec** for this task,
it accepts a number and the number of decimals to round to, and returns
the rounded Decimal.

```python
	from rectpack import float2dec, newPacker

	float_rects = [...]
	dec_rects = [(float2dec(r[0], 3), float2dec(r[1], 3)) for r in float_rects]

	p = newPacker()

	....
```

## References

[1] Jukka Jylang - A Thousand Ways to Pack the Bin - A Practical Approach to Two-Dimensional
Rectangle Bin Packing (2010)

[2] Huang, E. Korf - Optimal Rectangle Packing: An Absolute Placement Approach (2013)
