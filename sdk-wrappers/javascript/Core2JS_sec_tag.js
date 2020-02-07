// Glasswall Core 2 Library JavaScript Security Tagging Wrapper

const path = require('path');

class glasswall {
    constructor(pathToLibrary) {

        // Import JavaScript libraries
        let ffi = require('ffi');
        this.ref = require('ref');

        // API Binding
        this.bool = this.ref.types.bool;
        this.CString = this.ref.types.CString;

        let declarations = {

        // Security tagging API functions
        'GWSecuTag_TagFile': [this.bool, [this.CString, this.CString, this.CString]],  // TODO confirm equiv. of BOOL
        'GWSecuTag_RetrieveTagFile': [this.bool, [this.CString, this.CString]],  // TODO confirm equiv. of BOOL
        };

        process.chdir(path.dirname(pathToLibrary.toLowerCase()));

        // Load Glasswall Library
        this.gw = ffi.Library(pathToLibrary, declarations);
    };

    /**
	 * This function requests that the specified session uses the polices in the specified file. 
	 * @param {string} sourcefilepath The name of the file to be tagged
	 * @param {string} tagsinfilepath The name of the XML file containing data to be used for tagging
	 * @param {string} destfilepath format The name of the file containing the tagged data
	 */
    GWSecuTag_TagFile(sourcefilepath, tagsinfilepath, destfilepath) {
        //console.log("~~ Call to wrapper function GWSecuTag_TagFile ~~");
        return this.gw.GWSecuTag_TagFile(sourcefilepath, tagsinfilepath, destfilepath);
        // bool GWSecuTag_TagFile(const char *sourcefilepath, const char *tagsinfilepath, const char *destfilepath);
    }

    /**
	 * This function loads a file containing security tagging and extracts it
	 * @param {string} sourcefilepath The name of the file containing the security tagging
	 * @param {string} tagsoutfilepath The name of the XML file in which the extracted security tagging data will be placed
	 */
    GWSecuTag_RetrieveTagFile(sourcefilepath, tagsoutfilepath) {
        //console.log("~~ Call to wrapper function GWSecuTag_RetrieveTagFile ~~");
        return this.gw.GWSecuTag_RetrieveTagFile(sourcefilepath, tagsoutfilepath);
        // GWSecuTag_RetrieveTagFile(const char *sourcefilepath, const char *tagsoutfilepath);
    }
}

module.exports = glasswall