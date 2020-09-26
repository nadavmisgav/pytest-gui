
TESTS = {
    "Farrell": {
        "parent": "Doug",
        "name": "Farrell",
        "selected": True
    },
    "Brockman": {
        "parent": "Kent",
        "name": "Brockman",
        "selected": True
    },
    "Easter": {
        "parent": "Bunny",
        "name": "Easter",
        "selected": True
    }
}

def get():
    return [TESTS[key] for key in sorted(TESTS.keys())]