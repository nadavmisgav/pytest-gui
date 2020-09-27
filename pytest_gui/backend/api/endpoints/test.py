from pytest_gui.pytest.pytest_wrapper import worker

def select(test):
    module = test["module"]
    name = test["name"]
    selected = test["selected"]
    
    for idx, test in enumerate(worker.modules[module]):
        if test["name"] == name:
            worker.modules[module][idx]["selected"] = selected

def get():
    return worker.modules
            
    
    