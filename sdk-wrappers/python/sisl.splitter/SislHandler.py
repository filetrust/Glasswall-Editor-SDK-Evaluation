import os
import re
import time
import zipfile
import CommandLineParser as cmd

from SislDefragmentation import defragment
from SislFragmentation import fragment
from SislUtils import process_files, delete_tree, \
    remove_last_el_eof, create_directory, write_to_file, read_file, remove_directory


def walk_directory(dir, file_ext):
    list_of_files = []
    for (this_dir, dirs_here, files_here) in os.walk(dir, topdown=True):
        for f in files_here:
            if process_files(f, file_ext):
                list_of_files.append(f)
            # If no file_ext then all files will return
            elif file_ext == "":
                list_of_files.append(f)
    return list_of_files


def key_map_list(file_list):
    files_map = dict()
    for file_path in file_list:
        match = re.match(r"(Id_\d+_[^_]+_\d+)", os.path.basename(file_path))
        if match:
            if match.group(1) in files_map.keys():
                files_map[match.group(1)].append(file_path)
            else:
                files_map[match.group(1)] = [file_path]
    return files_map.items()


class SislHandler:
    zips_input_dir = ""
    output_fragmented_dir = "frag_output"
    output_defragmented_dir = "defrag_output"
    validate_sisl_inforamation = True
    sisl_split_size = 0

    def __init__(self, zips_input_dir="", output_fragmented_dir="", output_defragmented_dir="",
                 validate_sisl_information=True, sisl_split_size=0):
        self.zips_input_dir = zips_input_dir
        self.output_fragmented_dir = output_fragmented_dir
        self.output_defragmented_dir = output_defragmented_dir
        self.validate_sisl_inforamation = validate_sisl_information
        self.sisl_split_size = sisl_split_size

    def execute_fragmentation(self):
        zips_input_dir = self.zips_input_dir

        output_minimized_dir = self.output_fragmented_dir

        sisl_split_size = self.sisl_split_size

        zip_list = walk_directory(zips_input_dir, ".zip")

        for z in zip_list:
            f_path = os.path.join(zips_input_dir, z)
            fragment(f_path, output_minimized_dir, sisl_split_size)

        if self.validate_sisl_inforamation:
            sisl_information_file_path = os.path.join(self.output_fragmented_dir, "sisl_information_0.sisl")
            new_content = remove_last_el_eof(read_file(sisl_information_file_path))
            write_to_file(sisl_information_file_path, new_content)

    def execute_defragmentation(self):
        output_defragmented_dir = self.output_defragmented_dir
        output_fragmented_dir = self.output_fragmented_dir

        # temp_copy_dir = os.path.join(output_defragmented_dir, "copy")
        #
        # create_directory(temp_copy_dir)
        #
        # copy_tree(src=output_fragmented_dir, dst=temp_copy_dir)

        zip_list = walk_directory(output_fragmented_dir, ".zip")

        for index, z in enumerate(zip_list):
            with zipfile.ZipFile(os.path.join(output_fragmented_dir, z), 'r') as zip:
                temp_extract_path = os.path.join(output_defragmented_dir, str(index))
                create_directory(temp_extract_path)
                zip.extractall(temp_extract_path)
                sisl_list = walk_directory(temp_extract_path, ".sisl")
                sorted_list = sorted(sisl_list, key=lambda value: int(re.search(r"_(\d+)\.sisl$", value).group(1)))
                all_files_list = walk_directory(temp_extract_path, "")
                regex = re.compile(r"(.wmf|.jpg|.png|.bmp|.gif|.emf|.json|.unknown|.icc|.idx|.jpeg)$")

                images_list = list(filter(regex.search, all_files_list))

                file_list = []
                for f_name in sorted_list:  # non-dir files
                    f_path = os.path.join(temp_extract_path, f_name)
                    file_list.append(f_path)
                file_list = key_map_list(file_list)
                defragment(output_defragmented_dir, file_list, images_list, z, temp_extract_path)
                delete_tree(temp_extract_path)
        # delete_tree(temp_copy_dir)

    def defragmentation_initial_clean(self):
        remove_directory(self.output_defragmented_dir)
        create_directory(self.output_defragmented_dir)

    def fragmentation_initial_clean(self):
        remove_directory(self.output_fragmented_dir)
        create_directory(self.output_fragmented_dir)


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins % 60
    print("Time Lapsed = {0}: {1} : {2}".format(int(hours), int(mins), sec))


i, ss_validate, dir_frag, dir_defrag, ss_mode, s_size = cmd.getCommandLineArgs()

if dir_frag:
    dir_frag = os.path.abspath(dir_frag)
    print(dir_frag)
if dir_defrag:
    dir_defrag = os.path.abspath(dir_defrag)
    print(dir_defrag)

obj = SislHandler(zips_input_dir=i,
                  output_fragmented_dir=dir_frag,
                  output_defragmented_dir=dir_defrag,
                  validate_sisl_information=ss_validate,
                  sisl_split_size=s_size)

start_time = time.time()
# cProfile.run('re.compile("execute_fragmentation|execute_defragmentation")')

if ss_mode:
    obj.defragmentation_initial_clean()
    obj.execute_defragmentation()

else:
    obj.fragmentation_initial_clean()
    obj.execute_fragmentation()

end_time = time.time()

time_lapsed = end_time - start_time
time_convert(time_lapsed)
