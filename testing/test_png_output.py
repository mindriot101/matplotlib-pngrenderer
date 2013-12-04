from __future__ import print_function

import os
import sys
sys.path.insert(0, '.')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import zipfile

from pngrenderer.core import PNGRenderer
from pngrenderer.context import png_render

def build_plot():
    renderer = PNGRenderer(os.path.join(
        os.path.dirname(__file__), "out"))

    xdata = np.arange(10)
    ydata = xdata ** 2
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xdata, ydata, 'r-')

    out_fname = os.path.join(os.path.dirname(__file__), "out.zip")

    return (fig, ax, renderer, out_fname)


def setup_function(function):
    print("Setup")
    fig, ax, renderer, out_fname = build_plot()
    function.func_globals['fig'] = fig
    function.func_globals['ax'] = ax
    function.func_globals['renderer'] = renderer
    function.func_globals['out_fname'] = out_fname


def teardown_function(function):
    print("Teardown")
    try:
        os.remove(function.func_globals['out_fname'])
    except OSError:
        pass


def zip_contents(fname, test_contents):
    with zipfile.ZipFile(fname) as infile:
        return infile.namelist() == test_contents

def test_single_page():
    renderer.save_page("first.png", fig)
    renderer.render()

    assert os.path.isfile(out_fname)
    assert zip_contents(out_fname, ['first.png'])


def test_multiple_pages():
    renderer.save_page("first.png", fig)
    renderer.save_page("second.png", fig)
    renderer.render()

    assert os.path.isfile(out_fname)
    assert zip_contents(out_fname, ['first.png', 'second.png'])


def test_without_explicit_figure():
    renderer.save_page("first.png")
    renderer.render()

    assert zip_contents(out_fname, ['first.png'])


def test_context_manager():
    stub = os.path.join(os.path.dirname(__file__), "out")
    with png_render(stub) as png_renderer:
        build_plot()
        png_renderer.save_page("first.png")

    assert zip_contents(stub + '.zip', ['first.png'])


def test_savefig_alias():
    assert renderer.save_page == renderer.savefig
