import sys

import pycairo

import pycha.bar

from lines import lines


def barChart(output, chartFactory):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 400)

    dataSet = (
        ('lines', [(i, l[1]) for i, l in enumerate(lines)]),
        )

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(lines)],
                'label': 'Files',
                'rotate': 25,
            },
            'y': {
                'tickCount': 4,
                'rotate': 25,
                'label': 'Lines'
            }
        },
        'background': {
            'chartColor': '#ffeeff',
            'baseColor': '#ffffff',
            'lineColor': '#444444'
        },
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': 'red',
            },
        },
        'legend': {
            'hide': True,
        },
        'padding': {
            'left': 0,
            'bottom': 0,
        },
        'title': 'Sample Chart'
    }
    chart = chartFactory(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'barchart.png'
    barChart('v' + output, pycha.bar.VerticalBarChart)
    barChart('h' + output, pycha.bar.HorizontalBarChart)
