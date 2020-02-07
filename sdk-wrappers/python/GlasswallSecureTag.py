import ctypes as ct
import os


# noinspection SpellCheckingInspection,PyMethodMayBeStatic,PyPep8Naming,PyIncorrectDocstring
class Glasswall:
    """
        A Python API wrapper around the Glasswall Core 2 library.
    """

    gw_library = None

    def __init__(self, path_to_lib):
        """
            Constructor for the Glasswall library
        """

        try:
            # Change working directory to lib directory to find dependencies in Windows

            os.chdir(path_to_lib)

            cwd = os.getcwd()

            for root, dirs, files in os.walk(cwd):
                for file in files:
                    if file.__contains__("gw_securtag.dll"):
                        path_to_lib = os.path.join(cwd, "gw_securtag.dll")
                        break
                    elif file.__contains__("libgw_securtag.so"):
                        path_to_lib = os.path.join(cwd, "libgw_securtag.so")
                        break

            self.gw_library = ct.cdll.LoadLibrary(path_to_lib)

        except Exception as e:
            raise Exception("Failed to load Glasswall library. Exception: {0}".format(e))

    def tag_file(self, source_file_path, tags_in_file_path, dest_file_path):
        """
        Tag file

        :param source_file_path: The path to input file to be tagged.
        :param tags_in_file_path: The fully qualified path to the data to be tagged to the file.
        :param dest_file_path: The output location to output the tagged files to.
        :rtype: bool
        """

        self.gw_library.GWSecuTag_TagFile.argtypes = [
            ct.c_char_p
        ]

        # Variable initialisation
        ct_source_file_path = ct.c_char_p(source_file_path.encode('utf-8'))
        ct_tags_in_file_path = ct.c_char_p(tags_in_file_path.encode('utf-8'))
        ct_dest_file_path = ct.c_char_p(dest_file_path.encode('utf-8'))

        success = self.gw_library.GWSecuTag_TagFile(ct_source_file_path,
                                                    ct_tags_in_file_path,
                                                    ct_dest_file_path)
        return success

    def retrieve_tag(self, source_file_path, tags_out_file_path):
        """
        Retrieve tag from tagged file.

        :param source_file_path: The path to the tagged file.
        :param tags_out_file_path: The location to output the retrieved tag.
        :rtype: bool
        """
        self.gw_library.GWSecuTag_TagFile.argtypes = [
            ct.c_char_p,
        ]

        # Variable initialisation
        ct_source_file_path = ct.c_char_p(source_file_path.encode('utf-8'))
        ct_tags_out_file_path = ct.c_char_p(tags_out_file_path.encode('utf-8'))

        success = self.gw_library.GWSecuTag_RetrieveTagFile(ct_source_file_path,
                                                            ct_tags_out_file_path)

        return success
