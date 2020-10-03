from pytest_gui.pytest.pytest_wrapper import worker


def select(test):
    module = test.get("module", None)
    name = test.get("name", None)
    selected = test["selected"]
    found_idx = 0

    if module is None:  # All modules
        for m in worker.modules:
            for idx, test in enumerate(worker.modules[m]):
                worker.modules[module][idx]["selected"] = selected
        return worker.modules
    else:
        for idx, test in enumerate(worker.modules[module]):
            # Filter by name or name == None - all tests
            if test["name"] == name or name is None:
                worker.modules[module][idx]["selected"] = selected
                found_idx = idx
        return worker.modules[found_idx]


def get():
    return worker.modules


def run():
    worker.run_tests()
    return


def stop():
    worker.stop_tests()
    return
