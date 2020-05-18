import io
import os

from SislUtils import remove_first_el_sof, \
    remove_last_el_eof, \
    add_comma_to_eof, create_and_write_file, append_sisl, write_to_file, create_and_write_img_file, zip_up_files


def defragment(defragmentation_dir, file_list, images_list, original_zip_name, temp_extract_path):
    for index, file in enumerate(file_list):
        # print(index)
        # print(file)
        # print(len(file[1]) > 1)
        i = 0
        if len(file[1]) > 1:
            while i < len(file[1]):
                with open(file[1][i], "r+") as f:
                    file_str = f.read()
                    last_chr = file_str[-1]
                    file_list_length = len(file[1])
                    f_len_sub_one = file_list_length - 1
                    if not i == 0:
                        file_str = remove_first_el_sof(file_str)
                    if i < f_len_sub_one:
                        if file_str:
                            file_str = remove_last_el_eof(file_str)
                        else:
                            file_str = remove_last_el_eof(file_str)
                        if not last_chr == ",":
                            file_str = add_comma_to_eof(file_str)
                    write_to_file(file[1][i], file_str)
                    file_path_name = os.path.join(defragmentation_dir, file[0] + ".sisl")
                    if not os.path.exists(file_path_name):
                        create_and_write_file(file_path_name, file_str)
                    else:
                        append_sisl(file_path_name, file_str)
                    i += 1
                f.close()
            zip_up_files(os.path.join(defragmentation_dir, file[0] + ".sisl"), original_zip_name, defragmentation_dir)
        else:
            with open(file[1][0], "r+") as f:
                file_str = f.read()
                file_path_name = os.path.join(defragmentation_dir, file[0] + ".sisl")
                if not os.path.exists(file_path_name):
                    create_and_write_file(file_path_name, file_str)
                    zip_up_files(file_path_name, original_zip_name, defragmentation_dir)
                else:
                    append_sisl(file_path_name, file_str)
                    zip_up_files(file_path_name, original_zip_name, defragmentation_dir)
                f.close()
    if len(images_list) > 0:
        for img in images_list:
            input_file_path = os.path.join(temp_extract_path, img)
            with open(input_file_path, 'rb') as img_file:
                img_byte_array = io.BytesIO(img_file.read())
                file_path_name = os.path.join(defragmentation_dir, img)
                create_and_write_img_file(file_path_name, img_byte_array.read())
                zip_up_files(file_path_name, original_zip_name, defragmentation_dir)
