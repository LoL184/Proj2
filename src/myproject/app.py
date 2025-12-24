from utils import greet, fetch_status
from utils import day_advice


def main():
    # print(greet("Kiwi"))
    # fetch_status("https://example.com")
    print(day_advice()['advice'])


if __name__ == "__main__":
    main()
