from myproject.utils import greet, fetch_status


def main():
    print(greet("World"))
    fetch_status("https://example.com")


if __name__ == "__main__":
    main()
