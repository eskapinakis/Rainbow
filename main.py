from rainbow import Rainbow


R = Rainbow.Rainbow()


def interact():
    option = input("choose an option: ")
    if option == "exit":
        return
    else:
        x1 = int(input("first element: "))
        x2 = int(input("second element: "))
        print(R.operation(x1, x2, option))
        interact()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    interact()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
