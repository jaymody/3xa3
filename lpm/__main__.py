import time
import random
import argparse

parser = argparse.ArgumentParser(
    description="A tool to help you test your coding lines per minute."
)
args = parser.parse_args()

code_snippets = [
    "doubled_odds = [n * 2 for n in numbers if n % 2 == 1]",
    "number_list = [x ** 2 for x in range(10) if x % 2 == 0]",
    "[i for i in range(20) if i % 3 > 0]",
]


def main():
    print("Welcome to lpm")
    while True:
        new_passage()
        if input("Play again? (y/n) ") == "n":
            break


def new_passage():
    current_passage = code_snippets[random.randint(0, len(code_snippets) - 1)]
    starttime = time.time()
    userInput = input(current_passage + "\n")
    endtime = time.time()

    total_correct = 0
    for i in range(len(userInput)):
        if userInput[i] == current_passage[i]:
            total_correct += 1
    accuracy = round(100 * total_correct / len(current_passage))
    elapsed = endtime - starttime

    print("----\nSTATS")
    print("Accuracy: " + str(accuracy) + "%")
    print("Elapsed Time: " + str(round(elapsed, 2)))
    print("----")


if __name__ == "__main__":
    main()
