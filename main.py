from scenario.user_scenario import create_user_scenario
from scenario.folder_scenario import create_folder_for_dummy_user

def main():
    result = create_user_scenario()
    create_folder_for_dummy_user()


if __name__ == "__main__":
    main()
