import sys
from generator.Process import Process
from generator.webpy import webpy
from generator.debug import debug
from generator.HtmlDoc import HtmlDoc
from generator.CodeTemplator import CodeTemplator

class Generator:
    def __init__(self, template, tree):
        self.template = template
        process = Process(tree)
        module = sys.modules[Generator.__module__]
        self.generator = getattr(module, template)(process)
    
    def write(self, outputdir):
        self.generator.write(outputdir)
    
    def setOption(self, key, value):
        self.generator.setOption(key, value)
