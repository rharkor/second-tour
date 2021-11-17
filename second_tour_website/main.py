from website import main_website


def main():
    test()
    main_website.run(debug_mode=True)

def test():
    from function import main_test_dependance
    # insert_user.inser_admin()
    pass

if __name__ == "__main__":
    main()
