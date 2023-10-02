#!/bin/bash

# Loop through lectures 1 to 14
for i in {1..14}
do
  # Create the directory for the lecture
  mkdir -p docs/lec$i
  
  # Create the required files within the lecture directory
  touch docs/lec$i/index.md
  touch docs/lec$i/$i.1.md
  touch docs/lec$i/$i.2.md
  touch docs/lec$i/$i.3.md
  touch docs/lec$i/$i.4.md
done

echo "Directories and files created successfully!"
