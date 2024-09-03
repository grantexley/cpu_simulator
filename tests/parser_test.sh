#!/bin/bash

# Define the input file, expected output file, and the Python script
INPUT_FILE="input"
OUTPUT_FILE="outpy"
PYTHON_SCRIPT="your_script.py"

# Run the input through the Python script and capture the output
python3 "$PYTHON_SCRIPT" < "$INPUT_FILE" > temp_output

# Compare the generated output with the expected output
if [[ -e "$OUTPUT_FILE" && -e "temp_output" ]]; then
    if diff -q temp_output "$OUTPUT_FILE" > /dev/null; then
        echo "Test Passed: Output matches the expected output."
        exit 0
    else
        echo "Test Failed: Output does not match the expected output."
        diff temp_output "$OUTPUT_FILE"
        exit 1
    fi
else
    echo "Error: One or both of the files do not exist."
    exit 1
fi

# Clean up temporary output file
rm temp_output