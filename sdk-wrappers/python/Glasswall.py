import ctypes as ct
import os


# noinspection SpellCheckingInspection
class GwMemReturnObj:
    """A result from Glasswall containing the return status along with the file buffer with the buffer and buffer length"""

    def __init__(self):
        pass

    return_status = 0  # type: int
    file_buffer = None  # type: bytearray or bytes or None
    buffer = 0  # type: bytes
    buffer_length = 0  # type: bytes


# noinspection SpellCheckingInspection
class GwFileTypeEnum:
    """A result from Glasswall containing the determined file type value."""

    def __init__(self):
        pass

    enum_value = 0  # type: int
    file_buffer = None  # type: bytearray or None


# noinspection SpellCheckingInspection,PyMethodMayBeStatic,PyPep8Naming,PyIncorrectDocstring
class Glasswall:
    """
        A Python API wrapper around the Glasswall Core 2 library.
    """

    gw_library = None
    glasswall_file_session_status = 0

    """Python dictionaries keeping track of memory buffers"""
    session_export_memory_tracker = dict()
    session_output_memory_tracker = dict()
    session_analysis_memory_tracker = dict()
    session_policy_memory_tracker = dict()

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
                    if file.__contains__("glasswall_core2.dll"):
                        path_to_lib = os.path.join(cwd, "glasswall_core2.dll")
                        break
                    elif file.__contains__("libglasswall_core2.so"):
                        path_to_lib = os.path.join(cwd, "libglasswall_core2.so")
                        break

            self.gw_library = ct.cdll.LoadLibrary(path_to_lib)

        except Exception as e:
            raise Exception("Failed to load Glasswall library. Exception: {0}".format(e))

    def create_array_from_buffer(self, buffer, bufferLength):
        """
        Convert output buffer to python byte array
        :param buffer: output buffer
        :param bufferLength: output buffer length
        :return: custom object containing return status, buffers and filebuffer
        """

        if buffer == 0 or bufferLength == 0:
            return 0

        gw_return = GwMemReturnObj

        file_buffer = (ct.c_byte * bufferLength.value)()
        ct.memmove(file_buffer, buffer.value, bufferLength.value)

        gw_return.file_buffer = bytearray(file_buffer)

        return gw_return

    def assign_export_buffer(self, session,  buffer, buffer_length):
        """
        Registers the export memory to the session passed through and then adds the returned result to a custom export dict().
        :param session: the current session.
        :return: Nothing returned.
        """
        return_obj = self.register_export_memory(session, buffer, buffer_length)

        self.session_export_memory_tracker[session] = return_obj

    def assign_output_buffer(self, session,  buffer, buffer_length):
        """
        Registers the output memory to the session passed through and then adds the returned result to a custom output dict().
        :param session: the current session.
        :return: Nothing returned.
        """
        return_obj = self.register_output_memory(session, buffer, buffer_length)

        self.session_output_memory_tracker[session] = return_obj
        # return returnObj

    def assign_analysis_buffer(self, session, buffer, buffer_length):
        """
        Registers the analysis memory to the session passed through and then adds the returned result to a custom analysis dict().
        :param session: the current session.
        :return: Nothing returned.
        """
        return_obj = self.register_analysis_memory(session, buffer, buffer_length)

        self.session_analysis_memory_tracker[session] = return_obj

    def assign_policies_memory(self, session,  buffer, buffer_length):
        """
        Registers the policies memory to the session passed through and then adds the returned result to a custom policies dict().
        :param session: the current session.
        :return: Nothing returned.
        """
        return_obj = self.register_policies_memory(session, buffer, buffer_length)

        self.session_policy_memory_tracker[session] = return_obj

    def get_export_bytes(self, session):
        """
        Retrieves the session ID to get the array from the export buffer data.
        :param session: The session to retrieve array of export data from.
        :return: Byte Array
        """
        if session in self.session_export_memory_tracker:
            return_obj = self.session_export_memory_tracker[session]
            array = self.create_array_from_buffer(return_obj.buffer, return_obj.buffer_length)

            self.session_export_memory_tracker.pop(session)
            return array
        else:
            return None

    def get_output_bytes(self, session):
        """
        Retrieves the session ID to get the array from the output buffer data.
        :param session: The session to retrieve array of output data from.
        :return: Byte Array
        """
        if session in self.session_output_memory_tracker:
            return_obj = self.session_output_memory_tracker[session]
            array = self.create_array_from_buffer(return_obj.buffer, return_obj.buffer_length)

            self.session_output_memory_tracker.pop(session)
            return array
        else:
            return None

    def get_analysis_bytes(self, session):
        """
        Retrieves the session ID to get the array from the analysis buffer data.
        :param session: The session to retrieve array of analysis data from.
        :return: Byte Array
        """
        if session in self.session_analysis_memory_tracker:
            return_obj = self.session_analysis_memory_tracker[session]
            array = self.create_array_from_buffer(return_obj.buffer, return_obj.buffer_length)

            self.session_analysis_memory_tracker.pop(session)
            return array
        else:
            return None

    def get_policy_buffer(self, session):
        """
        Retrieves the session ID to get the array from the policy buffer data.
        :param session: The session to retrieve array of policy data from.
        :return: Byte Array
        """
        if session in self.session_policy_memory_tracker:
            return_obj = self.session_policy_memory_tracker[session]
            array = self.create_array_from_buffer(return_obj.buffer, return_obj.buffer_length)

            return array
        else:
            return None

    def determine_file_type_from_file(self, ct_path):
        """Returns a vaue indicaing th file type determined by glasswall.

        :param: str path: The file path to the input file.
        :return: A result indicating the determined file type
        :rtype: int
        """

        # API function declaration
        self.gw_library.GW2DetermineFileTypeFromFile.argtype = [ct.c_char_p]

        # Variable initialisation
        ct_path = ct.c_char_p(ct_path.encode("utf-8"))

        # API call
        gw_return_status = self.gw_library.GW2DetermineFileTypeFromFile(ct_path)
        return gw_return_status

    def determine_file_type_from_memory(self, ct_input_file_buffer, ct_input_length):
        """Returns a vaue indicaing th file type determined by glasswall.

        :param: bytearray inputFileBuffer: The input buffer containing the file to be determined
        :param: inputLength: length of the input file buffer data.
        :return: A result indicating the determined file type
        :rtype: GwFiletypeEnum()
        """

        # API function declaration
        self.gw_library.GW2DetermineFileTypeFromMemory.argtypes = [
            ct.c_char_p,
            ct.c_size_t
        ]

        # Variable function declaration
        ct_input_file_buffer = ct.c_char_p(ct_input_file_buffer)
        ct_input_length = ct.c_size_t(ct_input_length)

        # Return Object
        gw_return_status = GwFileTypeEnum()

        # API Call
        gw_return_status.enum_value = self.gw_library.GW2DetermineFileTypeFromMemory(ct_input_file_buffer, ct_input_length)
        return gw_return_status

    def lib_version(self):
        """Returns the Glasswall library version

        :return: A result with the Glasswall library version
        :rtype: str
        """

        # Declare the return type
        self.gw_library.GW2LibVersion.restype = ct.c_char_p

        # Return Object
        # API Call
        version = self.gw_library.GW2LibVersion()

        gw_return_status = ct.string_at(version).decode()
        return gw_return_status

    def open_session(self):
        """
            Open a new Glasswall session
            :rtype: int
        """

        # API Call
        gw_return_status = self.gw_library.GW2OpenSession()
        return gw_return_status

    def close_session(self, session):
        """
          Close the Glasswall session
        :param session: the session to close
        :return: Status object with return status.
        :rtype: int
        """

        # API function declaration
        self.gw_library.GW2CloseSession.argtypes = [ct.c_size_t]

        # Variable initialisation
        ct_session = ct.c_size_t(session)

        # API Call
        gw_return_status = self.gw_library.GW2CloseSession(ct_session)
        return gw_return_status

    def register_policies_file(self, session, filename, file_format):
        """
        Registers the policies to be used by Glasswall when processing files

        :param session: session to register policy to.
        :param filename: the file path of file to register
        :param file_format: the format of the policy e.g. XML
        :return: Status object with return status.
        :rtype: int
        """
        # API function declaration
        self.gw_library.GW2RegisterPoliciesFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
            ct.c_int,
        ]

        # Variable initialisation
        ct_session = ct.c_size_t(session)
        ct_filename = ct.c_char_p(filename.encode("utf-8"))
        ct_file_format = ct.c_int(file_format)

        gw_return_status = self.gw_library.GW2RegisterPoliciesFile(ct_session, ct_filename, ct_file_format)
        return gw_return_status

    def register_policies_memory(self, session, policy_buffer, policy_buffer_length):
        """
        Registers the policies in memory to be used bt Glasswall when processing files.

        :param  session: the session to register the ct_policy to.
        :return: Status object with return status.
        :rtype: GwStatusReturnObj()
        """

        # API function declaration
        self.gw_library.GW2RegisterPoliciesMemory.argtype = [
            ct.c_size_t,
            ct.c_char_p,
            ct.c_int
        ]

        # Variable initialisation
        ct_session = ct.c_size_t(session)
        ct_policy = ct.c_char_p(policy_buffer)
        policy_buffer_length = ct.c_size_t(policy_buffer_length)
        policy_format = ct.c_int(0)

        # Return Object
        gw_return_status = GwMemReturnObj()

        # API Call
        gw_return_status.return_status = self.gw_library.GW2RegisterPoliciesMemory(ct_session, ct_policy,
                                                                                   policy_buffer_length,
                                                                                   policy_format)
        gw_return_status.buffer = ct_policy
        gw_return_status.buffer_length = policy_buffer_length

        return gw_return_status

    def get_policy_settings(self, session, buffer, buffer_length):
        """
        Retrieves policy settings used by Glasswall for the session

        :param session: the session to get the policy settings from.
        :return: Object with return status and buffer info.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2GetPolicySettings.argtypes = [
            ct.c_size_t,
            ct.c_void_p,
        ]

        # Variable initialisation
        session = ct.c_size_t(session)
        # policy_buffer = ct.c_void_p()
        # policy_buffer_length = ct.c_size_t()

        # Return Object
        gw_return_status = GwMemReturnObj()

        # API Call
        gw_return_status.return_status = self.gw_library.GW2GetPolicySettings(session, ct.byref(buffer),
                                                                              ct.byref(buffer_length))
        gw_return_status.buffer = buffer
        gw_return_status.buffer_length = buffer_length

        return gw_return_status

    def register_input_file(self, session, inputFilePath):
        """
        Register an input file with the session.

        :param session: The session to register the input file to.
        :param inputFilePath: The file path to the file to be processed.
        :return: An object with the result indicating the file process status.
        :rtype: int
        """

        # API function declaration
        self.gw_library.GW2RegisterInputFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        session = ct.c_size_t(session)
        input_path = ct.c_char_p(inputFilePath.encode("utf-8"))

        # API Call
        gw_return_status = self.gw_library.GW2RegisterInputFile(session, input_path)
        return gw_return_status

    def register_input_memory(self, session, input_file_buffer, input_file_buffer_length):
        """Registers the input file in memory

        :param session: The session to register the input file to.
        :param: bytearray inputFileBuffer: The input buffer containing the file to be processed.
        :param: intputFileBufferLength: length of the input file buffer data.
        :return: An object with the result indicating the file process status and buffers.
        :rtype: GwMemReturnObj()
        """

        # API function declaration
        self.gw_library.GW2RegisterInputMemory.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
        ]

        # Variable initialisation
        session = ct.c_size_t(session)
        input_file_buffer = ct.c_char_p(input_file_buffer)
        input_file_buffer_length = ct.c_size_t(input_file_buffer_length)

        gw_return_status = GwMemReturnObj()

        # API Call
        gw_return_status.return_status = self.gw_library.GW2RegisterInputMemory(session, input_file_buffer,
                                                                                input_file_buffer_length)
        gw_return_status.buffer = input_file_buffer
        gw_return_status.buffer_length = input_file_buffer_length

        return gw_return_status

    def register_out_file(self, session, output_file_path):
        """
        Register an output file location with the session (Where to store the output file)

        :param session: The session to register the output file to.
        :param: str outputFilePath: the file path where the file containing the Glasswall output is placed
        :return: An object with the result indicating the file process status.
        :rtype: int
        """

        # API function declaration
        self.gw_library.GW2RegisterOutFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        session = ct.c_size_t(session)
        output_file_path = ct.c_char_p(output_file_path.encode("utf-8"))

        # API Call
        gw_return_status = self.gw_library.GW2RegisterOutFile(session, output_file_path)
        return gw_return_status

    def register_output_memory(self, session, buffer, buffer_length):
        """
        Registers a block of memory where the managed file is to be loaded into.

        :param session: The session to register the output file to.
        :return: An object with the result indicating the file process status.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2RegisterOutputMemory.argtypes = [
            ct.c_size_t,
            ct.c_void_p,
        ]

        session = ct.c_size_t(session)
        # output_buffer = ct.c_void_p()
        # output_buffer_length = ct.c_size_t()

        gw_return_status = GwMemReturnObj()

        gw_return_status.return_status = self.gw_library.GW2RegisterOutputMemory(session, ct.byref(buffer),
                                                                                 ct.byref(buffer_length))
        gw_return_status.buffer = buffer
        gw_return_status.buffer_length = buffer_length

        return gw_return_status

    def register_analysis_file(self, session, analysis_file_path_name):
        """
         Registers the analysis file in File to file analysis mode.

        :param session: The session to register the analysis file to.
        :param analysis_file_path_name:  The file path to the file to be analysed.
        :return: An object with the result indicating the file process status.
        :rtype: int
        """
        self.gw_library.GW2RegisterAnalysisFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
            ct.c_int,
        ]

        session = ct.c_size_t(session)
        analysis_file_path_name = ct.c_char_p(analysis_file_path_name.encode("utf-8"))
        analysis_file_format = ct.c_int()

        gw_return_status = self.gw_library.GW2RegisterAnalysisFile(session, analysis_file_path_name,
                                                                   analysis_file_format)
        return gw_return_status

    def register_analysis_memory(self, session, buffer, buffer_length):
        """
           Registers the analysis file in memory to memory analysis mode.

        :return: An object with the result indicating the file process status and buffers.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2RegisterAnalysisMemory.argtypes = [
            ct.c_size_t,
            ct.c_void_p
        ]

        session = ct.c_size_t(session)
        # analysis_file_buffer = ct.c_void_p()
        # analysis_output_length = ct.c_size_t()

        gw_return_status = GwMemReturnObj()

        gw_return_status.status = self.gw_library.GW2RegisterAnalysisMemory(session, ct.byref(buffer),
                                                                            ct.byref(buffer_length))
        gw_return_status.buffer = buffer
        gw_return_status.buffer_length = buffer_length

        return gw_return_status

    def register_import_file(self, session, input_file_path):
        """
          Registers the file to be imported in File to File Import mode.
         The imported file will not be created if the output directory does not exist or the file is non-conforming.

         :param session: The session to register the imported file to.
         :param input_file_path: The file path to the exported file archive.
         :return: An object with the result indicating the file process status.
         :rtype: int
         """

        # API function declaration
        self.gw_library.GW2RegisterImportFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        session = ct.c_size_t(session)
        input_file_path = ct.c_char_p(input_file_path.encode("utf-8"))

        # API Call
        gw_return_status = self.gw_library.GW2RegisterImportFile(session, input_file_path)
        return gw_return_status

    def register_import_memory(self, session, import_file_buffer, import_file_buffer_length):
        """
            Registers the file to be imported in Memory to Memory Import mode.
            The imported file will not be created if the output directory does not exist or the file is non-conforming.

        :param session: The session to register the imported file to.
        :param import_file_buffer: The buffer to store the imported file in.
        :param import_file_buffer_length: The length of the buffer.
        :return: An object with the result indicating the file process status and buffers.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2RegisterImportMemory.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
        ]

        session = ct.c_size_t(session)
        import_file_buffer = ct.c_char_p(import_file_buffer)
        import_file_buffer_length = ct.c_size_t(import_file_buffer_length)

        gw_return_status = GwMemReturnObj()

        gw_return_status.return_status = self.gw_library.GW2RegisterImportMemory(session, import_file_buffer,
                                                                                 import_file_buffer_length)
        gw_return_status.buffer = import_file_buffer
        gw_return_status.buffer_length = import_file_buffer_length

        return gw_return_status

    def register_export_file(self, session, exportFilePath):
        """
        Registers the file to be exported in File to File Export mode.

        :param session: The session to register the exported file to.
        :param exportFilePath: The path of the file file to be exported.
        :return: An object with the result indicating the file process status.
        :rtype: int
        """

        # API function declaration
        self.gw_library.GW2RegisterExportFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        session = ct.c_size_t(session)
        output_path = ct.c_char_p(exportFilePath.encode("utf-8"))

        # API Call
        gw_return_status = self.gw_library.GW2RegisterExportFile(session, output_path)
        return gw_return_status

    def register_export_memory(self, session, buffer, buffer_length):
        """
         Registers the file to be exported in Memory to Memory Export mode.

        :param session: The session to register the exported file to.
        :return: An object with the result indicating the file process status with buffers.
        :rtype: GwMemReturnObj()
        """
        self.gw_library.GW2RegisterExportMemory.argtypes = [
            ct.c_size_t,
            ct.c_void_p
        ]

        session = ct.c_size_t(session)
        # export_file_buffer = ct.c_void_p()
        # export_buffer_length = ct.c_size_t()

        gw_return_status = GwMemReturnObj()

        gw_return_status.return_status = self.gw_library.GW2RegisterExportMemory(session, ct.byref(buffer),
                                                                                 ct.byref(buffer_length))
        gw_return_status.buffer = buffer
        gw_return_status.buffer_length = buffer_length

        return gw_return_status

    def register_report_file(self, session, report_file_path_name):

        """
         Registers the report file in File to File mode.

        :param session: The session to register the report file to.
        :param report_file_path_name: The file path of the report file.
        :return: An object with the result indicating the file process status.
        :rtype: GwStatusReturnObj()
        """

        self.gw_library.GW2RegisterReportFile.argtsypes = [
            ct.c_size_t,
            ct.c_char_p,
        ]

        ct_session = ct.c_size_t(session)
        ct_report_file_path_name = ct.c_char_p(report_file_path_name.encode("utf-8"))

        gw_return_status = self.gw_library.GW2RegisterReportFile(ct_session, ct_report_file_path_name)
        return gw_return_status

    def run_session(self, session):
        """
          Run the Glasswall session (start processing the file)

        :param session: The session to register the report file to.
        :return: An object with the result indicating the file process status along with output depending on the actions registered.
        :rtype: int
        """

        # API function declaration
        self.gw_library.GW2RunSession.argtypes = [ct.c_size_t]

        # Variable initialisation
        ct_session = ct.c_size_t(session)

        # API Call
        gw_return_status = self.gw_library.GW2RunSession(ct_session)

        return gw_return_status

    def get_id_info(self, session, issue_id, buffer, buffer_length):
        """
        Gets the issue by id. e.g. issue id 96 returns "Document Processing Instances"

        :param session: The session used when getting issue by id.
        :param issue_id: The issue id.
        :return: An object with the result indicating the file process status and buffers.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2GetIdInfo.argtypes = [
            ct.c_size_t,
            ct.c_void_p
        ]

        ct_session = ct.c_size_t(session)
        ct_issue_id = ct.c_size_t(issue_id)
        # ct_buffer_length = ct.c_size_t()
        # ct_output_buffer = ct.c_void_p()

        gw_return_status = GwMemReturnObj()

        gw_return_status.return_status = self.gw_library.GW2GetIdInfo(ct_session, ct_issue_id.value, ct.byref(buffer_length),
                                                                      ct.byref(buffer))
        gw_return_status.buffer_length = buffer_length
        gw_return_status.buffer = buffer

        return gw_return_status

    def get_all_id_info(self, session, buffer, buffer_length):
        """
        Gets all possible issues and ids.

        :param session: The session used when getting all issues.
        :return: An object with the result indicating the file process status and buffers.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2GetAllIdInfo.argtypes = [
            ct.c_size_t,
            ct.c_void_p
        ]

        ct_session = ct.c_size_t(session)
        # ct_analysis_buffer_length = ct.c_size_t()
        # ct_analysis_buffer = ct.c_void_p()

        gw_return_status = GwMemReturnObj()

        gw_return_status.return_status = self.gw_library.GW2GetAllIdInfo(ct_session, ct.byref(buffer_length),
                                                                         ct.byref(buffer))
        gw_return_status.buffer = buffer
        gw_return_status.buffer_length = buffer_length

        return gw_return_status

    def file_session_status(self, session, buffer, buffer_length):
        """
        Get the file session status.

        :param session: The session used when getting the session status.
        :return: An object with the result indicating the file process status and buffers.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2FileSessionStatus.argtypes = [
            ct.c_size_t,
            ct.c_void_p
        ]

        # Variable initialisation
        ct_session = ct.c_size_t(session)
        self.glasswall_file_session_status = ct.c_size_t()
        # ct_status_msg_buffer = ct.c_void_p()
        # ct_status_buffer_length = ct.c_size_t()

        gw_return_status = GwMemReturnObj()

        gw_return_status.return_status = self.gw_library.GW2FileSessionStatus(ct_session,
                                                                              ct.byref(
                                                                                  self.glasswall_file_session_status),
                                                                              ct.byref(buffer),
                                                                              ct.byref(buffer_length))
        gw_return_status.buffer = buffer
        gw_return_status.buffer_length = buffer_length

        return gw_return_status

    def file_error_msg(self, session, buffer, buffer_length):
        """
        The error message returned from a file by session.

        :param session: The session used when returning the file error message.
        :return: An object with the result indicating the file process status and buffers.
        :rtype: GwMemReturnObj()
        """

        self.gw_library.GW2FileErrorMsg.argtypes = [ct.c_size_t, ct.c_void_p]

        gw_return = GwMemReturnObj()

        # Variables initialisation
        ct_session = ct.c_size_t(session)

        gw_return.return_status = self.gw_library.GW2FileErrorMsg(ct_session, ct.byref(buffer),
                                                                  ct.byref(buffer_length))

        gw_return.buffer_length = buffer
        gw_return.buffer = buffer_length

        return gw_return
