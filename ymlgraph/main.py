from graphviz import Digraph
from docopt import docopt
from ymlgraph.transformer import build
from ymlgraph import __version__
import yaml


__doc__ = """YAML to .dot, etc.

Usage:
  ymlgraph [options] <descriptor> 
  
Options:
  -h --help          Show this screen.
  --format=<fmt>     Format [default: pdf]
  --suffix=<suffix>  Output suffix [default: .gv]
  --engine=<engine>  Engine [default: dot]
"""


def render(dot, desc_filename, suffix):
    """Outputs the graph."""
    return dot.render(desc_filename + suffix)


def main():
    arguments = docopt(__doc__, version=__version__)
    
    desc = yaml.load(open(arguments['<descriptor>']))
    
    dot = Digraph(format=arguments['--format'], engine=arguments['--engine'])
    build(desc, dot)
    fn = render(dot, arguments['<descriptor>'], arguments['--suffix'])
    print("generated: %s" % fn)

    
if __name__ == '__main__':
    main()
