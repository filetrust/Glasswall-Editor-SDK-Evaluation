#!/bin/sh
./GWQtCLI -i input -o exp_output -x export
python3.5 SislHandler.py -i exp_output -m frag_output -z 0 -s 500000
python3.5 SislHandler.py -m frag_output -o defrag_output -z 1
./GWQtCLI -i defrag_output -o output -x import

