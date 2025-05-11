import time
import os

def print_refresh(lines, final=False):
    """
    Prints multiple lines and refreshes the terminal output.
    
    Args:
        lines (list): A list of strings to be printed on separate lines.
    """
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print all lines
    for line in lines:
        print(line)

    if final:
        pass
    else:
        # Move the cursor back up to the beginning of the block of lines
        print(f"\033[{len(lines)}A", end='')

# Example usage
example_lines = ["Processing step 1...", "Processing step 2...", "Processing step 3..."]

for i in range(10):
    updated_lines = [f"Step {i+1}: {line}" for line in example_lines]
    print_refresh(updated_lines)
    
    time.sleep(0.5)
