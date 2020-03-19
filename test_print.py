def print_star():
    for i in range(6):
        for j in range(i + 1):
            print('*', end='')
        print()


if __name__ == '__main__':
    print_star()