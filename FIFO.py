
def fifo(pages, frame_size):
    frames = []
    pointer = 0

    hits = 0
    faults = 0

    print("\n========== FIFO ALGORITHM ==========")
    print(f"{'Page':<10}{'Frames':<25}{'Status'}")
    print("-" * 50)

    for page in pages:

        # Check page is TRUE or False
        if page in frames:
            status = "HIT"
            hits += 1

        else:
            status = "FAULT"
            faults += 1

            # Add page if there is an empty frame
            if len(frames) < frame_size:
                frames.append(page)

            else:
                # Replace the oldest page
                frames[pointer] = page

                # Move pointer to the next frame
                pointer = (pointer + 1) % frame_size

        # Display current frame contents
        print(f"{page:<10}{str(frames):<25}{status}")

    print("-" * 50)
    print("Total Hits  :", hits)
    print("Total Faults:", faults)

    # Return results for other Python files
    return hits, faults, frames
