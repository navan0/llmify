import inspect
from functools import wraps

def functionify(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    required_params = []
    type_names = {
        str: "string",
        int: "integer",
        float: "float",
        bool: "boolean",
        list: "list",
        tuple: "tuple",
        dict: "dictionary",
        set: "set",
        type(None): "None",
        type: "type",
    }

    wrapper.meta = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": inspect.getdoc(func) or "",
            "parameters": {},
            "required": [],
        }
    }

    sig = inspect.signature(func)
    for param_name, param in sig.parameters.items():
        if param.default == inspect.Parameter.empty:
            required_params.append(param_name)

        param_type = param.annotation if param.annotation != inspect.Parameter.empty else None
        param_info = {
            "type": type_names.get(param_type, str(param_type)),
            "description": inspect.getdoc(func) or "",
        }
        
        wrapper.meta["function"]["parameters"][param_name] = param_info
    wrapper.meta["function"]["required"] = required_params

    return wrapper