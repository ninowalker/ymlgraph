from graphviz import Digraph
from docopt import docopt
import yaml

__doc__ = """SOA Graph Generator.

Usage:
  gen.py [options] all <descriptor> 
  gen.py [options] <node> <descriptor> 
  
Options:
  -h --help          Show this screen.
  --format=<fmt>     Format [default: pdf]
  --engine=<engine>  Engine [default: dot]
"""


def isa(o, key):
    return key in o and o[key]


_added = set()

def add_node(g, name, **attrs):
    if name in _added:
        return
#    _added.add(name)
    g.node(name, label=name, **attrs)


def eprops(n):
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


def render(descfn):
    fn = dot.render(descfn + ".gv")
    print "Generated:", fn


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    
    desc = yaml.load(open(arguments['<descriptor>']))
    
    dot = Digraph(format=arguments['--format'], engine=arguments['--engine'])
    build(desc, dot)
    render(arguments['<descriptor>'])