import json
import sys
import collections

# Function to load unique IDs from a JSON file
def load_unique_ids(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        ids = [item['id'].lower() for item in data if 'id' in item]
        unique_ids = set(ids)
        duplicate_counter = collections.Counter(ids)
        duplicates = [id for id, count in duplicate_counter.items() if count > 1]

        if duplicates:
            print(f"Duplicate IDs found in '{file_path}': {duplicates}")

        return unique_ids, len(unique_ids)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file '{file_path}': {e}")
        sys.exit(1)

# Function to compare two sets of IDs to find added and removed
def compare_ids(ids1, ids2):
    added_ids = list(ids2 - ids1)  # New in updated file
    removed_ids = list(ids1 - ids2)  # Missing from updated file
    return added_ids, removed_ids

# Main function to compare two JSON files for changes in IDs
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 compareids.py original.json updated.json")
        sys.exit(1)

    original_file = sys.argv[1]
    updated_file = sys.argv[2]

    # Load unique IDs from each JSON file
    original_ids, original_count = load_unique_ids(original_file)
    updated_ids, updated_count = load_unique_ids(updated_file)

    # Output ID counts for each file
    print(f"Number of unique IDs in '{original_file}': {original_count}")
    print(f"Number of unique IDs in '{updated_file}': {updated_count}")

    # Compare the IDs to identify added and removed
    added_ids, removed_ids = compare_ids(original_ids, updated_ids)

    # Output removed IDs
    if removed_ids:
        print("\nIDs removed:")
        print(removed_ids)
    else:
        print("\nNo IDs were removed.")

    # Output added IDs
    print("\nIDs added:")
    if added_ids:
        print(added_ids)
    else:
        print("None")

    # Issue warning if the total count stays the same but IDs are removed
    if original_count == updated_count and removed_ids:
        print("Warning: Total count remains the same, but IDs have been removed. This could indicate ID switching.")

if __name__ == "__main__":
    main()
