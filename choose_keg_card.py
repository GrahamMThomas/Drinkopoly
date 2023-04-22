
import random


def main():
    # open a file and choose a line at random
    with open("community_keg/cards.txt") as f:
        lines = f.readlines()
        print(random.choice(lines))

if __name__ == "__main__":
    main()