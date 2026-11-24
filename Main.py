
# Import functions from other Python files
from FIFO import fifo
from LRU import lru
from Optimal import optimal
from Result import display_results, compare_results


def get_frame_size():
    while True:
        try:
            frame_size = int(input("\nEnter number of page frames: "))

            if frame_size > 0:
                return frame_size

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input! Please enter a whole number.")


def get_page_reference():
    while True:
        page_input = input(
            "\nEnter page reference string (separated by spaces or commas): "
        )

        pages = page_input.replace(",", " ").split()

        if pages:
            return pages

        print("Page reference string cannot be empty.")


def main():

    print("=" * 50)
    print("          PAGE REPLACEMENT SIMULATOR")
    print("=" * 50)

    print("\nAvailable Algorithms:")
    print("[1] FIFO - First In, First Out")
    print("[2] LRU - Least Recently Used")
    print("[3] Optimal - Optimal Page Replacement")
    print("[4] Run All Algorithms")
    print("[5] Exit")

    while True:

        print("\n" + "-" * 50)
        choice = input("Choose an option (1-5): ")

        if choice == "5":
            print("\nThank you for using the simulator!")
            break

        elif choice in ["1", "2", "3", "4"]:

            # Get user input
            frame_size = get_frame_size()
            pages = get_page_reference()

            print("\n" + "=" * 50)
            print("             SIMULATION STARTED")
            print("=" * 50)

            if choice == "1":

                result = fifo(pages, frame_size)

                display_results(
                    "FIFO", result, len(pages)
                )

            elif choice == "2":

                result = lru(pages, frame_size)

                display_results(
                    "LRU", result, len(pages)
                )

            elif choice == "3":

                result = optimal(pages, frame_size)

                display_results(
                    "OPTIMAL", result, len(pages)
                )

            elif choice == "4":

                # Run all three algorithms
                fifo_result = fifo(pages, frame_size)
                lru_result = lru(pages, frame_size)
                optimal_result = optimal(pages, frame_size)

                # Display individual results
                display_results(
                    "FIFO", fifo_result, len(pages)
                )

                display_results(
                    "LRU", lru_result, len(pages)
                )

                display_results(
                    "OPTIMAL", optimal_result, len(pages)
                )

                # Compare all algorithms
                compare_results(
                    fifo_result,
                    lru_result,
                    optimal_result
                )

        else:
            print("Invalid choice! Please select 1-5.")


# Run the program
if __name__ == "__main__":
    main()
