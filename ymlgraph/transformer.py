from graphviz import Digraph
import yaml


def isa(o, key):
    return key in o and o[key]


def add_node(g, name, **attrs):
    g.node(name, label=name, **attrs)


def eprops(n):
    """Extract edge properties"""
    if isinstance(n, basestring):
        return n, {}
    if isinstance(n, dict):
        return n.pop('node'), n
    assert False, n

    
def add_edge(g, out, in_):
    outs, outp = eprops(out)
    ins, inp = eprops(in_)
    kwargs = (outp or inp)
    kwargs.pop('style', {})
    g.edge(outs, ins, **kwargs) 

    
def build(desc, g):
    """Function to take a descriptor and populate a graph."""
    for node in desc:
        if isinstance(node, basestring):
            add_node(g, node)
        elif isinstance(node, list):
            pass
        elif isa(node, 'subgraph'):
            sg = Digraph()
            build(node['nodes'], sg)
            g.subgraph(sg)
        elif isa(node, 'style'):
            for k, v in node['style'].items():
                getattr(g, '%s_attr' % k).update(**v)
        else:
            add_node(g, node['name'], **node.pop('attrs', {}))
    for node in desc:
        if isinstance(node, dict) and 'name' in node:
            for e in node.get('out', []):
                add_edge(g, node['name'], e)
            for e in node.get('in', []):
                add_edge(g, e, node['name'])
