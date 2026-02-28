from functions.get_file_content import get_file_content

testcases = [
    ("calculator", "lorem.txt"),
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py"),
]


def main():
    for testcase in testcases:
        result = get_file_content(testcase[0], testcase[1])
        print(result)


main()
