import functions.get_files_info

testcases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]


def main():
    for testcase in testcases:
        result = functions.get_files_info.get_file_info(testcase[0], testcase[1])
        print_dir = "Current" if testcase[1] == "." else "'" + testcase[1] + "'"
        print(f"Result for {print_dir} directory")
        print(result)


main()
