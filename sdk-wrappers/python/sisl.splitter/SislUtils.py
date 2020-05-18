import os
import subprocess
import shutil
import zipfile

"""Copy directory and all it's files to a specified destination. 
   Return a duplicate directory at a location."""


def copy_tree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy(s, d)


"""Delete an entire directory and all its files."""


def delete_tree(src):
    shutil.rmtree(src)


"""Rem"""


def remove_newlines_sof(content):
    file_str = str(content.read())
    first_el_str = file_str[0]
    if first_el_str == "\n":
        file_str.strip("\r\n")
    return file_str


def write_to_file(file, content):
    with open(file, "w") as f:
        f.write(content)
        f.close()


def read_file(file_path_name):
    with open(file_path_name, "r+") as f:
        content = f.read()
        f.close()
        return content


def validate_start_write(content):
    first_el_str = content[0]
    second_el_str = content[1]
    if not first_el_str == "{" and '_' in first_el_str and '_' in second_el_str:
        # new_content = content.replace(first_el_str, '{', 1)
        new_content = '{' + content
        return new_content
    return content


def remove_commas_at_start_write(content):
    first_el_str = content[0]
    second_el_str = content[1]
    if first_el_str == ",":
        new_content = content.replace(first_el_str, '', 1)
        return new_content
    elif second_el_str == ",":
        new_content = content.replace(second_el_str, '', 1)
        return new_content
    return content


def sisl_end_write(content):
    last_chr = content[-1]
    sec_last_chr = content[-2]
    third_last_chr = content[-3]
    if last_chr == "}" and not (sec_last_chr == "}" or third_last_chr == "}"):
        content += "}"
    elif not last_chr == "}":
        content += "}}"
    return content


def add_closing_to_eof(content):
    content += "}"
    return content


def add_comma_to_eof(content):
    content += ","
    return content


def remove_last_el_eof(content):
    if content[-1] == "," or content[-1] == "}":
        new_content = content[:-1]
        return new_content
    return content


def remove_first_el_sof(content):
    if '{' in content[0] or '}' in content[0]:
        content = content[1::]
        if '_' in content[0] and '_' not in content[1]:
            content = '_' + content
    return content


def single_sisl_grammar_checker(file, tester_tool_dir):
    arg = tester_tool_dir + '"' + str(file) + '"'
    test_output = subprocess.run(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return test_output.stderr


def split_list(lst, size):
    newseq = []
    split_size = 1.0 / size * len(lst)
    for i in range(size):
        newseq.append(lst[int(round(i * size)):int(round((i + 1) * split_size))])
    return newseq


def closest(lst, k):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - k))]


def create_and_write_file(file_path_name, data):
    fo = open(file_path_name, "w")
    fo.write(data)
    fo.close()


def create_and_write_img_file(file_path_name, data):
    fo = open(file_path_name, "wb")
    fo.write(data)
    fo.close()


def append_sisl(file_path_name, data):
    fo = open(file_path_name, "a")
    fo.write(data)
    fo.close()


def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def remove_directory(dir_name):
    if os.path.exists(dir_name):
        delete_tree(dir_name)


def all_sisl_grammar_checker(root_dest, tester_tool_dir):
    total_files_validated = 0
    total_files_failed = 0
    for (thisDir, dirsHere, filesHere) in os.walk(root_dest, topdown=True):
        for f_name in filesHere:  # non-dir files
            f_path = os.path.join(thisDir, f_name)
            file_name_without_ext, file_extension = os.path.splitext(str(f_name))
            if file_extension.__eq__(".sisl"):
                arg = tester_tool_dir + '"' + str(f_path) + '"'
                test_output = subprocess.run(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if str(test_output.stdout).__contains__("PASS"):
                    total_files_validated += 1
                else:
                    total_files_failed += 1


def sisl_info_start():
    return ("{ \n __Files_to_be_maximized: !fragmented { "
            "\n __files: !__ {")


def sisl_info_start_append():
    return ("\n\n __Files_to_be_maximized: !fragmented { "
            "\n __files: !__ {")


def sisl_info_start_append_img():
    return ("\n\n __Images_: !fragmented { "
            "\n __files: !__ {")


def sisl_info_mid(file_path_name):
    return "\n file: !__ " + '"' + file_path_name + '"'


def sisl_stream_end():
    return "\n } \n },"


def sisl_info_end():
    return "\n } \n }}"


def validate_sisl(data):
    validated_sisl = remove_commas_at_start_write(data)
    validated_sisl = remove_first_el_sof(validated_sisl)
    validated_sisl = validate_start_write(validated_sisl)
    validated_sisl = sisl_end_write(validated_sisl)

    return validated_sisl

    # layer of validation - returns error if sisl not valid - check most common errors
    # three_time_validation(test_tool_dir, file_path_name)


# perform a three time validation if invalid sisl
# def three_time_validation(test_tool_dir, file_path_name):
#     i = 1
#     while i < 3:
#         sisl_error = single_sisl_grammar_checker(file_path_name, tester_tool_dir=test_tool_dir)
#         if str(sisl_error).__contains__("b''"):
#             break
#         if str(sisl_error).__contains__("EOF too early"):
#             add_closing_to_eof(file_path_name)
#         elif str(sisl_error).__contains__("Negative nesting in NEST_END"):
#             remove_last_el_eof(file_path_name)
#         i += 1


def create_manifest(output_fragmented_dir, stream_finalise, new_stream, file_name):
    # create manifest
    # stream_finalise refers to the file that is being fragmented
    # is_last_zip refers to all files being fragmented to the very end.

    file_name_without_ext, file_extension = os.path.splitext(str(file_name))

    sisl_info_dest_file_path = os.path.join(output_fragmented_dir, "sisl_information_0.sisl")
    if new_stream and not os.path.exists(sisl_info_dest_file_path):
        create_and_write_file(sisl_info_dest_file_path,
                              sisl_info_start() + sisl_info_mid(file_name))
        add_comma_to_eof(read_file(sisl_info_dest_file_path))
    elif new_stream and os.path.exists(sisl_info_dest_file_path) and file_extension.__eq__(".sisl"):
        append_sisl(sisl_info_dest_file_path,
                    sisl_info_start_append() + sisl_info_mid(file_name))
        add_comma_to_eof(read_file(sisl_info_dest_file_path))
    elif new_stream and os.path.exists(sisl_info_dest_file_path) and not file_extension.__eq__(".sisl"):
        append_sisl(sisl_info_dest_file_path,
                    sisl_info_start_append_img() + sisl_info_mid(file_name))
        append_sisl(sisl_info_dest_file_path, sisl_stream_end())
    else:
        append_sisl(sisl_info_dest_file_path, sisl_info_mid(file_name))
        if not stream_finalise:
            add_comma_to_eof(read_file(sisl_info_dest_file_path))
        else:
            append_sisl(sisl_info_dest_file_path, sisl_stream_end())


def process_files(f_name, f_ext):
    if str(f_name).endswith(f_ext):
        return True
    else:
        return False


def file_zip(file_path_name, zip_name, dir):
    zip_file_path = os.path.join(dir, os.path.basename(zip_name))
    if not os.path.exists(zip_file_path):
        with zipfile.ZipFile(zip_file_path, "w") as zip:
            zip.write(file_path_name, os.path.basename(file_path_name))
        zip.close()
    else:
        with zipfile.ZipFile(zip_file_path, "a") as zip:
            zip.write(file_path_name, os.path.basename(file_path_name))
        zip.close()


def delete_file(file_path_name):
    os.remove(file_path_name)


def zip_up_files(file_path_name, zip_filename, output_fragmented_dir):
    file_zip(file_path_name, zip_filename, output_fragmented_dir)
    delete_file(file_path_name)
