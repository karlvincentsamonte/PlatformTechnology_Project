def lru(pages, frame_size):
    frames = []
    recent = []

    hits = 0
    faults = 0

    print("\n========== LRU ALGORITHM ==========")
    print(f"{'Page':<10}{'Frames':<25}{'Status'}")
    print("-" * 50)

    for page in pages:

        # Check if the page is already in memory
        if page in frames:
            status = "HIT"
            hits += 1

            # Update its recent usage
            recent.remove(page)
            recent.append(page)

        else:
            status = "FAULT"
            faults += 1

            # Add page if there is an empty frame
            if len(frames) < frame_size:
                frames.append(page)

            else:
                # Find the least recently used page
                oldest = recent.pop(0)

                # Replace the oldest page
                replace_index = frames.index(oldest)
                frames[replace_index] = page

            # Mark the new page as recently used
            recent.append(page)

        # Display current frame contents
        print(f"{page:<10}{str(frames):<25}{status}")

    print("-" * 50)
    print("Total Hits  :", hits)
    print("Total Faults:", faults)

    # Return results for other Python files
    return hits, faults, frames