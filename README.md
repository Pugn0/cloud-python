# Overview
This repository contains a collection of Python scripts designed for text file manipulation, including listing .txt files in a directory, removing duplicate lines from text files, and filtering lines based on specific words or URLs. These scripts are intended for various use cases such as data organization, dataset cleaning, or text analysis. The functionalities are made accessible through an interactive interface, catering to users with varying levels of programming expertise.

## Scripts Description

1. Listing .txt Files

### Description
A script for listing all .txt files in the current directory.

### Usage
This script was conceptually discussed but not explicitly implemented here. Generally, this can be accomplished with a simple for loop and the `glob.glob('*.txt')` function in Python.

2. Removing Duplicate Lines

### Description
Enables the user to choose between processing a single text file or all .txt files within a specified directory. It removes duplicate lines from each processed file and saves the result in a new file in a specified directory, preserving the original file's name.

### Usage
1. Run the script.
2. Choose to process a single file or all files in a directory when prompted.
3. If processing a single file, select the desired file.
4. The script will process the file(s) and save the results in the specified directory without duplicates, preserving the original filenames.

3. Text Filtering Based on Words or URLs

### Description
An interactive script that filters lines from one or several .txt files based on specific words or URLs provided by the user. The user has the option to process a single file or all files within a directory and to save the filtered lines in an output file.

### Usage
1. Execute the script.
2. Enter the target words or URLs when prompted.
3. Specify the output file name (if you wish to save the results).
4. Choose to process a single file or all files in a directory.
5. The script will filter lines based on the provided words or URLs.
6. If chosen, the result will be saved in the specified output file.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- This project was inspired by common data processing tasks that require efficient and user-friendly text manipulation tools.
- Thanks to the open-source community for providing a vast array of resources that facilitate the development of such tools.

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact
Pugno - @pugno_fc - pugnopix@gmail.com

[Project Link](https://github.com/Pugn0/cloud-python)
