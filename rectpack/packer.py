from .skyline import SkylineBlWm

import operator
import itertools
import collections

import decimal

# Float to Decimal helper
def float2dec(ft, decimal_digits):
    """
    Convert float (or int) to Decimal (rounding up) with the
    requested number of decimal digits.

    Arguments:
        ft (float, int): Number to convert
        decimal (int): Number of digits after decimal point

    Return:
        Decimal: Number converted to decima
    """
    with decimal.localcontext() as ctx:
        ctx.rounding = decimal.ROUND_UP
        places = decimal.Decimal(10)**(-decimal_digits)
        return decimal.Decimal.from_float(float(ft)).quantize(places)



# Sorting algos for rectangle lists
SORT_AREA  = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: r[0]*r[1]) # Sort by area

SORT_PERI  = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: r[0]+r[1]) # Sort by perimeter

SORT_DIFF  = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: abs(r[0]-r[1])) # Sort by Diff

SORT_SSIDE = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: (min(r[0], r[1]), max(r[0], r[1]))) # Sort by short side

SORT_LSIDE = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: (max(r[0], r[1]), min(r[0], r[1]))) # Sort by long side

SORT_RATIO = lambda rectlist: sorted(rectlist, reverse=True,
        key=lambda r: r[0]/r[1]) # Sort by side ratio

SORT_NONE = lambda rectlist: list(rectlist) # Unsorted




class PackerBNFMixin(object):

    def add_rect(self, width, height, rid=None):
        while True:
            if len(self._open_bins)==0:
                new_bin = self._new_open_bin()
                if new_bin is None:
                    return None

            rect = self._open_bins[0].add_rect(width, height, rid=rid)
            if rect is not None:
                return rect
            else:
                closed_bin = self._open_bins.popleft()
                self._closed_bins.append(closed_bin)


class PackerBFFMixin(object):
 
    def add_rect(self, width, height, rid=None):
        for b in self._open_bins:
            rect = b.add_rect(width, height, rid=rid)
            if rect is not None:
                return rect

        while True:
            new_bin = self._new_open_bin()
            if new_bin is None:
                return None
            rect = new_bin.add_rect(width, height, rid=rid)
            if rect is not None:
                return rect


class PackerBBFMixin(object):

    def add_rect(self, width, height, rid=None):
 
        # Try packing into open bins
        fit = ((b.fitness(width, height),  b) for b in self._open_bins)
        fit = (b for b in fit if b[0] is not None)
        try:
            _, best_bin = min(fit, key=operator.itemgetter(0))
            best_bin.add_rect(width, height, rid)
            return True
        except ValueError:
            pass    

        # Try packing into empty bins
        while True:
            new_bin = self._new_open_bin()
            if new_bin is None:
                return False

            if new_bin.add_rect(width, height, rid):
                return True



class PackerOnline(object):

    def __init__(self, pack_algo=SkylineBlWm, rotation=True):
        """
        Arguments:
            pack_algo (PackingAlgorithm): What packing algo to use
            rotation (bool): Enable/Disable rectangle rotation
        """
        self._rotation = rotation
        self._pack_algo = pack_algo
        self._factory = None
        self.reset()

    def __iter__(self):
        return itertools.chain(self._closed_bins, self._open_bins)

    def __len__(self):
        return len(self._closed_bins)+len(self._open_bins)
    
    def __getitem__(self, key):
        """
        Return bin in selected position. (excluding empty bins)
        """
        if not isinstance(key, int):
            raise TypeError("Indices must be integers")

        size = len(self)  # avoid recalulations

        if key < 0:
            key += size

        if not 0 <= key < size:
            raise IndexError("Index out of range")
        
        if key < len(self._closed_bins):
            return self._closed_bins[key]
        else:
            return self._open_bins[key-len(self._closed_bins)]

    def _new_open_bin(self):
        """
        Extract next empty bin and append it to open bins

        Returns:
            PackingAlgorithm: Initialized empty packing bin.
        """
        # Do we have any more empty bins?
        if len(self._empty_bins) > 0:
            new_bin = self._empty_bins.popleft()
            self._open_bins.append(new_bin)
            return new_bin
        # Do we have a factory?
        if self._factory:
            new_bin = self._factory()
            self._open_bins.append(new_bin)
            return new_bin
        # No more places to look.
        return None

    def add_factory(self, width, height, *args, **kwargs):
        from functools import partial
        # accept the same parameters as PackingAlgorithm objects
        self._factory = partial(self._pack_algo, width, height, self._rotation, *args, **kwargs)

    def add_bin(self, width, height, *args, **kwargs):
        # accept the same parameters as PackingAlgorithm objects
        self._empty_bins.append(self._pack_algo(width, height, self._rotation, *args, **kwargs))

    def rect_list(self):
        rectangles = []
        bin_count = 0

        for abin in self:
            for rect in abin:
                rectangles.append((bin_count, rect.x, rect.y, rect.width, rect.height, rect.rid))
            bin_count += 1

        return rectangles

    def bin_list(self):
        """
        Return a list of the dimmensions of the bins in use, that is closed
        or open containing at least one rectangle
        """
        return [(b.width, b.height) for b in self]

    def validate_packing(self):
        for b in self:
            b.validate_packing()

    def reset(self): 
        # Bins fully packed and closed.
        self._closed_bins = collections.deque()

        # Bins ready to pack rectangles
        self._open_bins = collections.deque()

        # User provided bins not in current use
        self._empty_bins = collections.deque()



class Packer(PackerOnline):

    def __init__(self, pack_algo=SkylineBlWm, sort_algo=SORT_LSIDE, 
            rotation=True):
        """
        """
        super(Packer, self).__init__(pack_algo=pack_algo, rotation=rotation)
        
        self._sort_algo = sort_algo

        # User provided bins and Rectangles
        self._avail_bins = collections.deque()
        self._avail_rect = collections.deque()

        # Aux vars used during packing
        self._sorted_rect = []

    def add_bin(self, width, height, count=1):
        for _ in range(0, count):
            self._avail_bins.append((width, height))

    def add_rect(self, width, height, rid=None):
        self._avail_rect.append((width, height, rid))

    def _is_everything_ready:
        return self._avail_rect and (self._avail_bins or self._factory):

    def pack(self):

        self.reset()

        if not self._is_everything_ready():
            # maybe we should throw an error here?
            return

        # Add available bins to packer
        for b in self._avail_bins:
            super(Packer, self).add_bin(*b)

        # If enabled sort rectangles
        self._sorted_rect = self._sort_algo(self._avail_rect)

        # Start packing
        for r in self._sorted_rect:
            super(Packer, self).add_rect(*r)


 
class PackerBNF(Packer, PackerBNFMixin):
    """
    BNF (Bin Next Fit): Only one open bin, if rectangle doesn't fit
    go to next bin and close current one.
    """
    pass

class PackerBFF(Packer, PackerBFFMixin):
    """
    BFF (Bin First Fit): Pack rectangle in first bin it fits
    """
    pass
    
class PackerBBF(Packer, PackerBBFMixin):
    """
    BBF (Bin Best Fit): Pack rectangle in bin that gives best fitness
    """
    pass

class PackerOnlineBNF(PackerOnline, PackerBNFMixin):
    """
    BNF Bin Next Fit Online variant
    """
    pass

class PackerOnlineBFF(PackerOnline, PackerBFFMixin):
    """
    BFF Bin First Fit Online variant
    """
    pass

class PackerOnlineBBF(PackerOnline, PackerBBFMixin):
    """
    BBF Bin Best Fit Online variant
    """
    pass


class PackerGlobal(Packer, PackerBNFMixin):
    """
    GLOBAL: For each bin pack the rectangle with the best fitness.
    """
    def __init__(self, pack_algo=SkylineBlWm, rotation=True):
        """
        """
        super(PackerGlobal, self).__init__(pack_algo=pack_algo,
            sort_algo=SORT_NONE, rotation=rotation)

    def _find_best_fit(self, pbin):
        """
        Return rectangle with best fitness for the list from _sorted_rect list

        Arguments:
            pbin (PackingAlgorithm): Packing bin
        """
        fit = ((pbin.fitness(r[0], r[1]), r) for r in self._sorted_rect)
        fit = (f for f in fit if f[0] is not None)
        try:
            _, rect = min(fit, key=operator.itemgetter(0))
            return rect
        except ValueError:
            return None

    def pack(self):
       
        self.reset()

        if not self._is_everything_ready():
            return
        
        # Add available bins to packer
        for b in self._avail_bins:
            super(Packer, self).add_bin(*b)
    
        #TODO: Use something faster for elem removal than a list 
        self._sorted_rect = self._sort_algo(self._avail_rect)
        
        # Order rectangles using best fitness
        for b in self._avail_bins:
            
            if len(self._sorted_rect)==0:
                break

            pbin = self._new_open_bin()
            while True:
               
                best_rect = self._find_best_fit(pbin)
                if best_rect is None:
                    closed_bin = self._open_bins.popleft()
                    self._closed_bins.append(closed_bin)
                    break

                self._sorted_rect.remove(best_rect)

                PackerBNFMixin.add_rect(self, *best_rect)






# Packer factory
class Enum(tuple): 
    __getattr__ = tuple.index

PackingMode = Enum(["Online", "Offline"])
PackingBin = Enum(["BNF", "BFF", "BBF", "Global"])


def newPacker(mode=PackingMode.Offline, 
        bin_algo=PackingBin.BBF, 
        pack_algo=SkylineBlWm,
        sort_algo=None, 
        rotation=True):
    """
    Packer factory helper function

    Arguments:
        mode (PackingMode): Packing mode
            Online: Rectangles are packed as soon are they are added
            Offline: Rectangles aren't packed untils pack() is called
        bin_algo (PackingBin): Bin selection heuristic
        pack_algo (PackingAlgorithm): Algorithm used
        rotation (boolean): Enable or disable rectangle rotation. 

    Returns:
        Packer: Initialized packer instance.
    """
    packer_class = None

    # Online Mode
    if mode == PackingMode.Online:
        sort_algo=None
        if bin_algo == PackingBin.BNF:
            packer_class = PackerOnlineBNF
        elif bin_algo == PackingBin.BFF:
            packer_class = PackerOnlineBFF
        elif bin_algo == PackingBin.BBF:
            packer_class = PackerOnlineBBF
        else:
            raise AttributeError("Unsupported bin selection heuristic")

    # Offline Mode
    elif mode == PackingMode.Offline:
        if bin_algo == PackingBin.BNF:
            packer_class = PackerBNF
        elif bin_algo == PackingBin.BFF:
            packer_class = PackerBFF
        elif bin_algo == PackingBin.BBF:
            packer_class = PackerBBF
        elif bin_algo == PackingBin.Global:
            packer_class = PackerGlobal
            sort_algo=None
        else:
            raise AttributeError("Unsupported bin selection heuristic")

    else:
        raise AttributeError("Unknown packing mode.")

    if sort_algo:
        return packer_class(pack_algo=pack_algo, sort_algo=sort_algo, 
            rotation=rotation)
    else:
        return packer_class(pack_algo=pack_algo, rotation=rotation)


