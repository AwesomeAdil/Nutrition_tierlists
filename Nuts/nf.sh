#!/bin/bash

# Check if a file name is provided as a parameter
if [ $# -eq 0 ]; then
    echo "Usage: $0 <output_file>"
    exit 1
fi

# Template file
template_file="template.txt"

# Output file (parameter)
output_file="$1.txt"

# Check if the template file exists
if [ ! -f "$template_file" ]; then
    echo "Template file not found: $template_file"
    exit 1
fi

# Check if the output file already exists
if [ -e "$output_file" ]; then
    read -p "File $output_file already exists. Do you want to overwrite it? (y/n): " overwrite
    if [ "$overwrite" != "y" ]; then
        echo "Aborted."
        exit 1
    fi
fi

# Copy the contents of the template file to the output file
cat "$template_file" > "$output_file"

# Open the output file in Vim
lvim "$output_file"

