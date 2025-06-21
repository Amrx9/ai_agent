from functions.write_file import write_file


def test():

    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print('result for writing "wiat, this isnt lorem ipsum" to file: "lorem.txt"')
    print(result)

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print('result for writing "lorem ipsum dolor sit amet" to file: "pkg/morelorem.txt"')
    print(result)

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print('result for writing "this should not be allowed" to file: "/tmp/temp.txt"')
    print(result)


if __name__ == "__main__":
    test()