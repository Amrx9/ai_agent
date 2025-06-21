from functions.run_python import run_python_file

def test():

    result = run_python_file("calculator", "main.py")
    print("result for running main.py from calculator dir")
    print(result)

    result = run_python_file("calculator", "tests.py")
    print("result for running test.py from calculator dir")
    print(result)

    result = run_python_file("calculator", "../main.py")
    print("result for running '../main.py' from calculator dir")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print("result for running nonexistent.py from calculator dir")
    print(result)

if __name__ == "__main__":
    test()