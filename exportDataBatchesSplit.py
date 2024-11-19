import os
import random

# Path to the original RIS file
input_ris_file = "results/RIS/allJournals_subsample.ris"
output_dir = "results/RIS/batches"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the RIS file
with open(input_ris_file, "r", encoding="utf-8") as file:
    ris_content = file.read()

# Split the file into entries based on the RIS entry delimiter
entries = ris_content.strip().split("\nER  -\n")
entries = [entry + "\nER  -" for entry in entries]  # Re-append the delimiter

# Helper function to extract the journal name from an entry
def get_journal_name(entry):
    for line in entry.split("\n"):
        if line.startswith("JO  -"):  # RIS field for journal name
            return line[5:].strip()
    return ""  # Default if no journal name is found

# Sort entries by journal name
entries.sort(key=get_journal_name)

# Shuffle the sorted entries randomly for batch assignment
random.seed(1)  # For reproducibility; remove or adjust for full randomness
random.shuffle(entries)

# Determine batch size
num_batches = 3
batch_size = len(entries) // num_batches
leftovers = len(entries) % num_batches

# Split randomly shuffled entries into batches
batches = []
start_idx = 0
for i in range(num_batches):
    # Distribute leftover entries evenly across batches
    current_batch_size = batch_size + (1 if i < leftovers else 0)
    batch = entries[start_idx:start_idx + current_batch_size]
    # Sort each batch by journal name
    batch.sort(key=get_journal_name)
    batches.append(batch)
    start_idx += current_batch_size

# Save each batch as a separate RIS file
for i, batch in enumerate(batches, start=1):
    batch_file = os.path.join(output_dir, f"batch_{i}.ris")
    with open(batch_file, "w", encoding="utf-8") as batch_file_out:
        batch_file_out.write("\n\n".join(batch))
    print(f"Batch {i} saved as {batch_file}")
