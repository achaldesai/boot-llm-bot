from functions.run_python_file import run_python_file

testcases = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt"),
]


def main():
    for testcase in testcases:
        result = run_python_file(*testcase)
        print(result)


main()
