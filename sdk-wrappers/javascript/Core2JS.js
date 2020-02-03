// Glasswall Core2 Library JavaScript Wrapper

const path = require('path');

class glasswall {
    constructor(pathToLibrary) {
        // Import JavaScript libraries
        let ffi = require('ffi');
        this.ref = require('ref');

        // API Binding
        this.int = this.ref.types.int;
        this.uint_ptr = this.ref.refType(this.ref.types.uint);
        this.CString = this.ref.types.CString;
        this.CString_ptr = this.ref.refType(this.ref.types.CString);
        this.size_t = this.ref.types.size_t;
        this.size_t_ptr = this.ref.refType(this.ref.types.size_t);

        let intPtr = this.ref.refType('int');

        let declarations = {
            // Configuration and Library information API functions

            // Library Management Methods
            'GW2LibVersion': [this.CString, []],
            'GW2OpenSession': [this.int, []],
            'GW2CloseSession': [this.int, [this.int]],
            'GW2DetermineFileTypeFromFile': [this.int, [this.CString]],
            'GW2DetermineFileTypeFromMemory': [this.int, [this.CString, this.size_t]],

            // Policy Methods
            'GW2RegisterPoliciesFile': [this.int, [this.int, this.CString, this.int]],						    // Confirm correct dataype of 'format'
            'GW2RegisterPoliciesMemory': [this.int, [this.int, this.CString, this.size_t, this.int]],			// Confirm correct datatype of 'format'
            'GW2GetPolicySettings': [this.int, [this.int, this.CString_ptr, this.size_t_ptr, this.int]],

            // Operation Methods
            'GW2RegisterInputFile': [this.int, [this.int, this.CString]],
            'GW2RegisterInputMemory': [this.int, [this.int, this.CString, this.size_t]],
            'GW2RegisterOutFile': [this.int, [this.int, this.CString]],
            'GW2RegisterOutputMemory': [this.int, [this.int, this.CString_ptr, this.size_t_ptr]],
            'GW2RegisterAnalysisFile': [this.int, [this.int, this.CString, this.int]], 						    // Confirm correct datatype of 'format'
            'GW2RegisterAnalysisMemory': [this.int, [this.int, this.CString_ptr, this.size_t_ptr, this.int]],	// Confirm correct datatype of 'format'
            'GW2RegisterImportFile': [this.int, [this.int, this.CString]],
            'GW2RegisterImportMemory': [this.int, [this.int, this.CString, this.size_t]],
            'GW2RegisterExportFile': [this.int, [this.int, this.CString]],
            'GW2RegisterExportMemory': [this.int, [this.int, this.CString_ptr, this.size_t_ptr]],
            'GW2RegisterReportFile': [this.int, [this.int, this.CString]],

            // Additional Library Management Methods
            'GW2RunSession': [this.int, [this.int]],
            'GW2GetIdInfo': [this.int, [this.int, this.size_t, this.size_t_ptr, this.CString_ptr]],
            'GW2GetAllIdInfo': [this.int, [this.int, this.size_t_ptr, this.CString_ptr]],

            'GW2FileSessionStatus': [this.int, [this.int, intPtr, this.CString_ptr, this.size_t_ptr]],

            'GW2FileErrorMsg': [this.int, [this.int, this.CString_ptr, this.size_t_ptr]]
        };

        process.chdir(path.dirname(pathToLibrary.toLowerCase()));

        // Load Glasswall Library
        this.gw = ffi.Library(pathToLibrary, declarations);
    }

    /**
     * This function retrieves the version string of the Glasswall Library
     * @returns {string} The Glasswall library version.
     */

    GW2LibVersion() {
        //console.log("~~ Call to wrapper function GW2LibVersion ~~");
        return this.gw.GW2LibVersion();
    }

    /**
	 * This function requests the creation of a new glasswall session.
	 * @returns {number} The handle to the new session, as a small positive integer. Failure returns 0.
	 */

    GW2OpenSession() {
        //console.log("~~ Call to wrapper function GW2OpenSession ~~");
        
        return this.gw.GW2OpenSession();
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT Session GW2OpenSession(void );
    }

    /**
	 * This function requests the closure of a session. 
	 * @param {number} session The ID of the session to be closed
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2CloseSession(session) {
        //console.log("~~ Call to wrapper function GW2CloseSession ~~")
        return this.gw.GW2CloseSession(session);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2CloseSession(Session session);
    }

    /**
	 * This function determines the file type for a given file provided it is supported by Glasswall. Notice this is not related to a session.
	 * @param {string} path The path to the provided file.
	 * @returns {number} The determined file type, as enumerated in the C source header file filetypes.h.
	 */

    GW2DetermineFileTypeFromFile(path) {
        //console.log("~~ Call to wrapper function GW2DetermineFileTypeFromFile ~~");
        //return this.gw.GW2DetermineFileTypeFromFile(path);

        return this.gw.GW2DetermineFileTypeFromFile(path);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT ft_t GW2DetermineFileTypeFromFile(const char * path);
    }

    /**
	 * This function determines the file type for a given file provided it is supported by Glasswall. Notice this is not related to a session.
	 * @param {string} path The path to the provided file.
	 * @returns {number} The determined file type, as enumerated in the C source header file filetypes.h.
	 */

    GW2DetermineFileTypeFromMemory(inputFileBuffer, inputLength) {
        //console.log("~~ Call to wrapper function GW2DetermineFileTypeFromFile ~~");
        //return this.gw.GW2DetermineFileTypeFromFile(path);
        return this.gw.GW2DetermineFileTypeFromMemory(inputFileBuffer, inputLength);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterInputMemory(Session session, const char * inputFileBuffer, size_t inputLength);
    }

    /**
	 * This function requests that the specified session uses the polices in the specified file. 
	 * @param {number} session The ID of the session.
	 * @param {string} filename The filename from which to load policy settings.
	 * @param {number} format - The format of the policy to be registered.
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterPoliciesFile(session, filename, format) {
        //console.log("~~ Call to wrapper function GW2RegisterPoliciesFile ~~");
        return this.gw.GW2RegisterPoliciesFile(session, filename, format);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterPoliciesFile(Session session, const char * filename, Policy_format format);
    }

    /**
	 * This function requests that the specified session uses the polices stored in a specified memory buffer.
	 * @param {number} session The ID of the session.
	 * @param {string} policies A pointer to the policy data buffer.
	 * @param {number} policiesLength The length of the data in the policy buffer.
	 * @param {number} format The format of the policy.
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterPoliciesMemory(session, policies, policylength, format) {
        //console.log("~~ Call to wrapper function GW2RegisterPoliciesMemory ~~");
        return this.gw.GW2RegisterPoliciesMemory(session, policies, policylength, format);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterPoliciesMemory(Session session, char * policies, size_t policiesLength, Policy_format format);
    }

    /**
	 * This function returns the policy settings used for the specified session
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} policiesBuffer The pointer to the policy buffer.
	 * @param {number} policiesLength The size of the data in the policy buffer
	 * @param {number} format The format of the policy.
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2GetPolicySettings(session, policiesBuffer, policiesLength, format) {
        //console.log("~~ Call to wrapper function GW2GetPolicySettings ~~");
        return this.gw.GW2GetPolicySettings(session, policiesBuffer, policiesLength, format);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2GetPolicySettings(Session session, char ** policiesBuffer, size_t * policiesLength, Policy_format format);
    }

    /**
	 * This function registers a specified file as the input file for a specified session
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} inputFilePath The path of the file to be registered
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterInputFile(session, inputFilePath) {
        //console.log("~~ Call to wrapper function GW2RegisterInputFile ~~");
        return this.gw.GW2RegisterInputFile(session, inputFilePath);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterInputFile(Session session, const char * inputFilePath);
    }

    /**
	 * This function registers a file stored in memory as the input file for a specified session
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} inputFileBuffer A buffer holding the file data
	 * @param {number} inputLength The size of the file buffer
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterInputMemory(session, inputFileBuffer, inputLength) {
        //console.log("~~ Call to wrapper function GW2RegisterInputMemory ~~");
        return this.gw.GW2RegisterInputMemory(session, inputFileBuffer, inputLength);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterInputMemory(Session session, const char * inputFileBuffer, size_t inputLength);
    }

    /**
	 * This function registers a destination file for the managed file produced by Glasswall.
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} outputFilePath The specified output path. Must be different to the specified input file path.
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterOutFile(session, outputFilePath) {
        //console.log("~~ Call to wrapper function GW2RegisterOutFile ~~");
        return this.gw.GW2RegisterOutFile(session, outputFilePath);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterOutFile(Session session, const char * outputFilePath);
    }

    /**
	 * This function registers where the managed content is to be placed, and where to place the size variable of the content.
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} outputBuffer The specified output path. Must be different to the specified input file path.
	 * @param {string} outputLength The size of the file buffer
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterOutputMemory(session, outputBuffer, outputLength) {
        //console.log("~~ Call to wrapper function GW2RegisterOutputMemory ~~");
        return this.gw.GW2RegisterOutputMemory(session, outputBuffer, outputLength);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterOutputMemory(Session session, char ** outputBuffer, size_t * outputLength);
    }

    /**
	 * This function registers a specified file with a specified session, in line with a specified format
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} analysisFilePathName The path of the file to be registered.
	 * @param {number} format The specified format.
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterAnalysisFile(session, analysisFilePathName, format) {
        //console.log("~~ Call to wrapper function GW2RegisterAnalysisFile ~~");
        return this.gw.GW2RegisterAnalysisFile(session, analysisFilePathName, format);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterAnalysisFile(Session session, const char * analysisFilePathName, Analysis_format format);
    }

    /**
	 * This function stores a pointer to the analysis reeport produced by a successful run of runSession.
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} analysisFileBuffer The pointer to the location of the analysis report.
	 * @param {string} analysisoutputLength The size of the analysis report.
	 * @param {number} format The specified format.
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterAnalysisMemory(session, analysisFileBuffer, analysisoutputLength, format) {
        //console.log("~~ Call to wrapper function GW2RegisterAnalysisMemory ~~");
        return this.gw.GW2RegisterAnalysisMemory(session, analysisFileBuffer, analysisoutputLength, format);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterAnalysisMemory(Session session, char ** analysisFileBuffer, size_t * analysisoutputLength, Analysis_format format);
    }

    /**
	 * This function registers an import file path against a specified session.
	 * 
	 * @param {number} session The ID of the session.
	 * @param {string} importFilePath The path of the file to be registered.
	 * @returns {number} Status of the operation; 0 for success, non-zero for failure.
	 */

    GW2RegisterImportFile(session, importFilePath) {
        //console.log("~~ Call to wrapper function GW2RegisterImportFile ~~");
        return this.gw.GW2RegisterImportFile(session, importFilePath);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterImportFile(Session session, const char * importFilePath);
    }

    /**
	* This function registers an import memory location against a specified session.
	* 
	* @param {number} session The ID of the session.
	* @param {string} importFileBuffer A pointer to the specified memory location.
	* @param {number} importLength The size of the file buffer.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*/

    GW2RegisterImportMemory(session, import_File_Buffer, import_File_Buffer_Length) {
        //console.log("~~ Call to wrapper function GW2RegisterImportMemory ~~");
        return this.gw.GW2RegisterImportMemory(session, import_File_Buffer, import_File_Buffer_Length);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterImportMemory(Session session, char * importFileBuffer, size_t importLength);
        // NB This procedure was modified from API specification to remove pointers for file buffer and import length
    }

    /**
	* This function registers a specified export file with a specified session
	* 
	* @param {number} session The ID of the session.
	* @param {string} exportFilePath The path of the file to be registered.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*/

    GW2RegisterExportFile(session, exportFilePath) {
        //console.log("~~ Call to wrapper function GW2RegisterExportFile ~~");
        return this.gw.GW2RegisterExportFile(session, exportFilePath);
        //extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterExportFile(Session session, const char * exportFilePath);
    }

    /**
	* This function registers an export memory location against a specified session.
	* 
	* @param {number} session The ID of the session.
	* @param {string} exportFileBuffer A pointer to the specified memory location.
	* @param {number} exportLength The size of the file buffer.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*/

    GW2RegisterExportMemory(session, exportFileBuffer, exportLength) {
        //console.log("~~ Call to wrapper function GW2RegisterExportMemory ~~");
        return this.gw.GW2RegisterExportMemory(session, exportFileBuffer, exportLength);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterExportMemory(Session session, char ** exportFileBuffer, size_t * exportLength);
    }

    /**
	* This function registers the name of the file where the engineering log file is to be placed.
	* 
	* @param {number} session The ID of the session.
	* @param {string} reportFilePathName The path of the file to be registered.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*/

    GW2RegisterReportFile(session, reportFilePathName) {
        //console.log("~~ Call to wrapper function GW2RegisterReportFile ~~");
        return this.gw.GW2RegisterReportFile(session, reportFilePathName);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2RegisterReportFile(Session session, const char * reportFilePathName);
    }

    /**
	* This function runs the specified session.
	* 
	* @param {number} session The ID of the session to be run.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*/

    GW2RunSession(session) {
        return this.gw.GW2RunSession(session);
    }

    /**
	* This function places a pointer to a description of a specified IssueID in a specified location.
	* 
	* @param {number} session The ID of the session.
	* @param {number} issueId The ID of the issue.
	* @param {number} bufferLength The length of the buffer.
	* @param {string} outputBuffer The location of the output buffer.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*/

    GW2GetIdInfo(session, issueId, bufferLength, outputBuffer) {
        //console.log("~~ Call to wrapper function GW2GetIdInfo ~~")
        return this.gw.GW2GetIdInfo(session, issueId, bufferLength, outputBuffer);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2GetIdInfo(Session session, size_t issueId, size_t * bufferLength, char ** outputBuffer);
    }

    /**
	* This function places a pointer in a specified location to XML data populated with Glasswall Issue ID descriptions and value ranges, for a specified session.
	* 
	* @param {number} session The ID of the session.
	* @param {number} bufferLength The length of the buffer.
	* @param {string} outputBuffer The location of the output buffer.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*/

    GW2GetAllIdInfo(session, bufferLength, outputBuffer) {
        //console.log("~~ Call to wrapper function GW2GetAllIdInfo ~~")
        return this.gw.GW2GetAllIdInfo(session, bufferLength, outputBuffer);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT int GW2GetAllIdInfo(Session session, size_t * bufferLength, char ** outputBuffer);
    }

    /**
	* This function retrieves the Glasswall Session Status. This status gives a high level indication of the processing that was carried out on the last document processed by the library
	* 
	* @param {number} session The ID of the session.
	* @param {number} glasswallSessionStatus To be defined.
	* @returns {number} Status of the operation; To be defined.
	*
	*/

    GW2FileSessionStatus(session, glasswallSessionStatus, statusMsgBuffer, statusBufferLength) {
        //console.log("~~ Call to wrapper function GW2FileSessionStatus ~~")
        return this.gw.GW2FileSessionStatus(session, glasswallSessionStatus, statusMsgBuffer, statusBufferLength);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT const char * GW2FileSessionStatus(Session session, unsigned int * glasswallSessionStatus);
    }

    /**
	* This function retrieves the error message reported by Glasswall. If more than one error is reported, only one will be returned.
	* 
	* @param {number} session The ID of the session.
	* @returns {number} Status of the operation; 0 for success, non-zero for failure.
	*
	*/

    ///* This function retrieves the Glasswall Session Process error message.  */
    GW2FileErrorMsg(session, errorMsgBuffer, errorMsgBufferLength) {
        //console.log("~~ Call to wrapper function GW2FileErrorMsg ~~")
        return this.gw.GW2FileErrorMsg(session, errorMsgBuffer, errorMsgBufferLength);
        // extern "C" GLASSWALL_CORE2SHARED_EXPORT const char * GW2FileErrorMsg(Session session); 
    }
}
module.exports = glasswall