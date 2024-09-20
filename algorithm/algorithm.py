def create_seq(num):
    """Выводит n первых элементов последовательности 1223334444..."""
    res = ''
    for i in range(1, num + 1):
        str_i = str(i)
        res += i * str_i
        if len(res) >= num:
            break
    print(res[:num])


def main():
    create_seq(0)
    create_seq(5)
    create_seq(10)
    create_seq(15)
    create_seq(30)

if __name__ == '__main__':
    main()
