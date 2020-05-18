SislFragmentation/SislDefragmentation:

Overview:
SislFragmentation:
    - Splits out sisls that are greater than 1MB and creates sisls in n size chunks or less.
    - Creates a manifest which describes which sisl files that need grouping to be Maximized. A new directory within the directory of the minimized files output is created called "/sisl_information_0"
    - Compresses the sisls into a file of the original compressed file name.
SislDefragmentation:
    - The fragmented files are placed into the output directory specified by the user.
    - Traverses the minimized files and reconstructs the minimized sisl files back to a single file in its original form.
    - The defragmented files are placed into the output specified by the user.
    - Compresses the sisls into a file of the original compressed file name.

SislUtils:
    - The utils contains any methods that are non fragmenting and defragmenting specific.

Executing the software:
Please note that you must be running python3 or later for the SislFragmentation and SislDefragmentation to work.
    Command line arguments:
    -i(String) = input file zip directory
    -m(String) = fragmented output
    -o(String) = deframentation output directory
    -z(int 1|0) = fragment or defragment
    -s(bytes) = size to split sisls
        1) You must have an input file inside of an input folder at a directory of your choice.
        2) Run SislFragmentation:
            python3.5 SislHandler.py -i exp_output -m frag_output -z 0 -s 500000
        3) Run SislDefragmentation:
            python3.5 SislHandler.py -m frag_output -o defrag_output -z 1
            
Blog Posts:
https://medium.com/glasswall-engineering/glasswalls-sisl-splitter-d7925e39b3e5
https://medium.com/glasswall-engineering/glasswall-sisl-splitter-in-action-82d80908d6d9
