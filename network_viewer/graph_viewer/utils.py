import pandas as pd
import os

def loss_to_width(loss):
    return '{:.1f}'.format((loss*15/1) + 1)


def load_transformer_edges(dot_string, transformers, res_trafo):
    for i in transformers.index:
        thickness = loss_to_width(res_trafo.pl_mw.loc[i])
        loss = '{:.3f} mw'.format(res_trafo.pl_mw.loc[i])

        n1 = transformers.hv_bus.loc[i]
        n2 = transformers.lv_bus.loc[i]

        dot_string += f'\n{n1} -- {n2} [color=red width={thickness} style=dotted label="{loss}"]'

    return dot_string

def load_line_edges(dot_string, lines, res_lines):

    for i in lines.index:
        thickness = loss_to_width(res_lines.pl_mw.loc[i])
        loss = '{:.3f} mw'.format(res_lines.pl_mw.loc[i])

        n1 = lines.from_bus.loc[i]
        n2 = lines.to_bus.loc[i]

        dot_string += f'\n{n1} -- {n2} [color=red width={thickness} label="{loss}"]'

    return dot_string

def add_load_bus_attributes(dot_string, loads):
    complete = set()

    for i in loads.bus:
        if i not in complete:
            dot_string += f'\n{i}[shape=box color=blue fontcolor=white]'

    return dot_string

def add_gen_bus_attributes(dot_string, gens):
    complete = set()

    for i in gens.bus:

        if i not in complete:
            dot_string += f'\n{i}[color=green fontcolor=white]'

    return dot_string

def get_dot_string(source):
    network_data = pd.read_html(source, header=0)

    transformers = network_data[1]
    lines = network_data[2]
    loads = network_data[3]
    gens = network_data[5]
    res_lines = network_data[9]
    res_trafo = network_data[9]

    dot_string = 'graph mynet {'
    dot_string = load_transformer_edges(dot_string, transformers, res_trafo)
    dot_string = load_line_edges(dot_string, lines, res_lines)
    dot_string = add_load_bus_attributes(dot_string, loads)
    dot_string = add_gen_bus_attributes(dot_string, gens)
    dot_string += '\n}'

    return dot_string
