import io
import os
import zipfile

from SislParser import SislParser
from SislUtils import create_directory, validate_sisl, create_manifest, \
    create_and_write_file, create_and_write_img_file, write_to_file, zip_up_files


# noinspection PyBroadException
def fragment(zips_input_dir, output_fragmented_dir, sisl_split_size):
    data = ""
    temp_data = ""

    with zipfile.ZipFile(zips_input_dir, 'r') as zip:

        sisl_parser = SislParser()

        files_info = zip.infolist()

        i = 0
        for file_info in files_info:
            new_stream = True
            if not file_info.filename.endswith('/'):
                file_name_without_ext, file_extension = os.path.splitext(str(file_info.filename))

                # create_directory(output_fragmented_dir)

                if file_extension.__eq__(".sisl"):
                    input_data = zip.read(file_info.filename).decode("ascii")
                    tokens = sisl_parser.tokenize_sisl(input_data)
                    file_name_without_ext = os.path.normpath(file_name_without_ext)

                    i += 1
                    if file_info.file_size > sisl_split_size:
                        for index, token in enumerate(tokens):
                            try:
                                data += token.get_data(input_data)

                                if index == len(tokens) - 1:
                                    file_name = file_name_without_ext + "_" + str(index)
                                    file_path_name = os.path.join(output_fragmented_dir, file_name + file_extension)
                                    validated_sisl = validate_sisl(data=data)
                                    create_and_write_file(file_path_name, validated_sisl)
                                    zip_up_files(file_path_name, zip.filename, output_fragmented_dir)

                                    create_manifest(output_fragmented_dir=output_fragmented_dir,
                                                    stream_finalise=True,
                                                    new_stream=new_stream,
                                                    file_name=file_name + file_extension)
                                    new_stream = False
                                    data = ""

                                if token.type == sisl_parser.SislTokenType.ST_GROUP_END:
                                    temp_data += tokens[index + 1].get_data(input_data)
                                    temp_data += tokens[index + 2].get_data(input_data)
                                    temp_data += tokens[index + 3].get_data(input_data)
                                    temp_data += tokens[index + 4].get_data(input_data)
                                    temp_data += tokens[index + 5].get_data(input_data)

                                    if len(data) >= sisl_split_size and not temp_data.__contains__(
                                            "data") and not temp_data.__contains__("children"):
                                        file_name = file_name_without_ext + "_" + str(index)
                                        file_path_name = os.path.join(output_fragmented_dir, file_name + file_extension)
                                        validated_sisl = validate_sisl(data=data)
                                        create_and_write_file(file_path_name, validated_sisl)
                                        zip_up_files(file_path_name, zip.filename, output_fragmented_dir)

                                        data = ""
                                        create_manifest(output_fragmented_dir=output_fragmented_dir,
                                                        stream_finalise=False,
                                                        new_stream=new_stream,
                                                        file_name=file_name + file_extension)
                                        new_stream = False
                                temp_data = ""
                            except:
                                continue
                    else:
                        file_path_name = os.path.join(output_fragmented_dir, file_name_without_ext) + file_extension
                        data = input_data
                        create_and_write_file(file_path_name, data)
                        zip_up_files(file_path_name, zip.filename, output_fragmented_dir)

                        data = ""
                else:
                    input_data = zip.read(file_info.filename)
                    img = io.BytesIO(input_data)
                    file_path_name = os.path.join(output_fragmented_dir, file_name_without_ext) + file_extension
                    create_and_write_img_file(file_path_name, img.read())
                    zip_up_files(file_path_name, zip.filename, output_fragmented_dir)

                    create_manifest(output_fragmented_dir=output_fragmented_dir,
                                    stream_finalise=False,
                                    new_stream=new_stream,
                                    file_name=file_info.filename)

        zip.close()
