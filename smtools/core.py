#! python
""" Tools for plotting Stark maps
"""
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
        >>> lines = lc_cmap(xvals, yvals, colors)
        >>> lines.set_linewidth(3)

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> ax.add_collection(lines)
        >>> plt.show()
    """
    pts = np.array([xvals, yvals]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lines = LineCollection(segs, colors=colors)
    return lines

def sm_sort(arr, arr2=None, **kwargs):
    """ Attempt to sort a Stark map (arr) into continuous lines by discreet extrapolation.

         args:
                arr                       np.array() (2D)
                arr2=None                 np.array() (2D)
                                          arr2 will be returned using the
                                          same ordering as applied to arr.

         kwargs:
                 mid_sort=True            start from the middle line
                 order=False              return ordering

         return:
                sorted_arr, [sorted arr2], [order]
    """
    mid_sort = kwargs.get('mid_sort', True)
    get_order = kwargs.get('order', False)
    num_rows, num_lines = np.shape(arr)
    # initialise
    order = np.zeros_like(arr, dtype=int)
    d2arr = arr.copy()
    if arr2 is not None:
        assert np.shape(arr) == np.shape(arr2), "arr and arr2 must have the same shape"
        d2arr2 = arr2.copy()
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
            if arr2 is not None:
                d2arr2[i, j] = arr2[i][arg]
    output = (d2arr,)
    if arr2 is not None:
        output = output + (d2arr2,)
    if get_order:
        output = output + (order,)
    if len(output) == 1:
        output = output[0]
    return output

def tros_ms(arr, arr2=None, **kwargs):
    """ The inverse of sm_sort().
    """
    get_order = kwargs.get('order', False)
    num_rows, num_cols = np.shape(arr)
    # initialise
    order = np.zeros_like(arr, dtype=int)
    d2arr = arr.copy()
    if arr2 is not None:
        assert np.shape(arr) == np.shape(arr2), "arr and arr2 must have the same shape"
        d2arr2 = arr2.copy()
    # sort
    for i in range(num_rows):
        arg = np.argsort(arr[i])
        order[i] = arg
        d2arr[i] = arr[i, arg]
        if arr2 is not None:
            d2arr2[i] = arr2[i, arg]
    # output
    output = (d2arr,)
    if arr2 is not None:
        output = output + (d2arr2,)
    if get_order:
        output = output + (order,)
    if len(output) == 1:
        output = output[0]
    return output