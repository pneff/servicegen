#!/usr/bin/python
import sys, os.path
from parser.Service import Service
from generator.Generator import Generator

def main():
    service = Service()
    filename = sys.argv[1]
    print "Converting %(filename)s" % locals()
    tree = service.parse(filename)
    # Generator("debug", tree.tree).write("out")
    
    targets = (
        # Name,   Template,       Outdir
        ('webpy', 'python-webpy', 'webpy'),
        ('html',  'html',         'webpy/static/docs/'),
        ('html',  'html',         'html'),
    )
    
    for target in targets:
        type = target[0]
        template = target[1]
        outdir = target[2]
        
        gen = Generator("CodeTemplator", tree.tree)
        gen.setOption("template", sys.path[0] + "/templates/" + template)
        gen.setOption("sourcedir", os.path.dirname(filename))
        gen.setOption("type", type)
        gen.write("out/" + outdir)

if __name__ == "__main__":
    main()
