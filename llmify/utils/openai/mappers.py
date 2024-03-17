import json
import inspect
import os
from llmify.utils.openai.tools import functionify
from importlib.util import spec_from_file_location, module_from_spec

class ModuleNotFoundError(Exception):
    pass


class MetaMapper:
    """
    Class for mapping metadata of functions within Python files in the directory of the currently executing script.
    """
    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))

    def map(self):
        meta_dict = {}
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    module_name = file[:-3]
                    module = self.load_module(os.path.join(root, file), module_name)
                    if module:
                        for name, obj in inspect.getmembers(module):
                            if inspect.isfunction(obj):
                                if hasattr(obj, '__wrapped__'):
                                    func = obj
                                    meta = func.meta
                                    meta_dict[name] = meta
        return meta_dict

    def load_module(self, filepath, module_name):
        spec = spec_from_file_location(module_name, filepath)
        if spec is not None:
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            return module