#!/bin/bash

# Check if pygmentize is installed
if ! command -v pygmentize &> /dev/null; then
    echo "pygmentize could not be found. Please install Pygments."
    exit 1
fi

# Check if jupyter nbconvert is installed
if ! command -v jupyter &> /dev/null; then
    echo "jupyter nbconvert could not be found. Please install Jupyter Notebook."
    exit 1
fi

# Directory containing the .py and .ipynb files
DIR="."

# Convert .py files to HTML
for file in "$DIR"/*.py; do
    # Check if there are any .py files
    if [ ! -e "$file" ]; then
        echo "No .py files found in the directory."
        break
    fi

    # Get the base name of the file without the extension
    base_name=$(basename "$file" .py)
    
    # Convert the .py file to .html
    pygmentize -f html -O full -o "$DIR/$base_name.html" "$file"
    
    echo "Converted $file to $base_name.html"
done

# Convert .ipynb files to HTML
for file in "$DIR"/*.ipynb; do
    # Check if there are any .ipynb files
    if [ ! -e "$file" ]; then
        echo "No .ipynb files found in the directory."
        break
    fi

    # Convert the .ipynb file to .html
    jupyter nbconvert --to html "$file"
    
    echo "Converted $file to HTML using Jupyter nbconvert"
done

echo "Conversion completed."

