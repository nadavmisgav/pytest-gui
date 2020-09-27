from pytest_gui.pytest.pytest_wrapper import worker

def select(test):
    module = test.get("module", None)
    name = test.get("name", None)
    selected = test["selected"]
    found_idx = 0
    
    if module == None: # All modules
        for m in worker.modules:
            for idx, test in enumerate(worker.modules[m]):
                worker.modules[module][idx]["selected"] = selected
    else:
        for idx, test in enumerate(worker.modules[module]):
            # Filter by name or name == None - all tests
            if test["name"] == name or name == None:
                worker.modules[module][idx]["selected"] = selected
                found_idx = idx
                
    return worker.modules

def get():
    return worker.modules

def run():
    pass
            
    
    