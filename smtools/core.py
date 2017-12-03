#! python
import numpy as np

from matplotlib.collections import LineCollection
def lc_cmap(xvals, yvals, colors):
    """ Apply a color map to line plot. 

        args:
            xvals              np.array
            yvals              np.array
            colors             np.array of RGB[alpha] tuples
    
        return:
            matplotlib.collections.LineCollection
    
        >>> colors = np.asarray([(0.8, 0.2, 0.2, a) for a in zs]) #RGBalpha
        >>> lc = lc_cmap(xvals, yvals, colors)
        >>> lc.set_linewidth(3)
        
        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> ax.add_collection(lc)
        >>> plt.show()
    """
    pts = np.array([xvals, yvals]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(segs, colors=colors)
    return lc

def sm_sort(arr, **kwargs):
    """ Attempt to sort a Stark map (arr) into continuous lines by discreet extrapolation.

         args:
                arr                        np.array() (2D)

         kwargs:
                 mid_sort=True             start from the middle line

         return:
                sorted_array, order
    """
    mid_sort = kwargs.get('mid_sort', True)
    num_rows, num_lines = np.shape(arr)
    # initialise
    order = np.zeros_like(arr)
    d2arr = arr.copy()
    # assume no crossings in first 4 rows
    for i in range(4):
        order[i] = range(num_lines)
    # lines
    jvals = np.arange(num_lines)
    if mid_sort:
        # start from the middle line
        jvals = jvals[np.argsort(np.abs(jvals - (len(jvals) - 1.0)/2.0))]
    for i in range(4, num_rows):
        for j in jvals:
            # extrapolate last 4 values to guess the next
            yvals = d2arr[i-4:i, j]
            guess = 4 * yvals[-1] - 6 * yvals[-2] + 4 * yvals[-3] - yvals[-4]
            # find the closest data point
            arg = np.argmin(np.abs(guess - arr[i]))
            order[i, j] = arg
            d2arr[i, j] = arr[i][arg]
    return d2arr, order
