from functions.write_file import write_file

testcases = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]


def main():
    for testcase in testcases:
        result = write_file(testcase[0], testcase[1], testcase[2])
        print(result)


main()
