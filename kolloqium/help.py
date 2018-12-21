with open("BlackFriday.csv") as f:
    with open("test.csv", 'w') as f2:
        for num in range(0, 500):
            f2.write(f.readline())
