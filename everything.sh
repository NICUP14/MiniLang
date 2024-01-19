#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 folder_name path"
    exit 1
fi

folder_name="$1"
output_file="$2/everything.ml"
order=(
    "$folder_name/cstdlib.ml"
    "$folder_name/stddef.ml"
    "$folder_name/va_utils.ml"
    "$folder_name/alloc.ml"
    "$folder_name/debug.ml"
    "$folder_name/misc.ml"
    "$folder_name/algorithm.ml"
)

if [ ! -d "$folder_name" ]; then
    echo "Error: Folder '$folder_name' does not exist."
    exit 1
fi

if [ -f "$output_file" ]; then
    echo "Error: Output file '$output_file' already exists."
    exit 1
fi

for file in "${order[@]}"; do
    if [ -f "$file" ]; then
        # Remove the file suffix from the basename
        filename=$(basename "$file")
        filename_no_suffix="${filename%.ml}"
        echo "import \"$folder_name/$filename_no_suffix\"" >> "$output_file"
    fi
done
echo 'end' >> "$output_file"

echo "Include statements written to $output_file"