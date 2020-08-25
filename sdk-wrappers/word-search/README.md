# Word search

The Glasswall engine provides deep-file inspection, remediation, sanitisation, and reporting. 

The engine deconstructs a file to its structural components and builds an internal tree-like representation of the file. It walks each node of the tree, inspecting, repairing, and sanitising content items before reconstructing a new file. 

The Glasswall engine also provides the ability to export and import the engine's internal representation of a file structure in an intermediate format such as XML. This allows internal components of a file to be made available to external programs for additional processing, before recomposing the file to include those externally modified components.

Glasswalls Word Search engine is built on top of the export and import capability, performing text searching in the content and metadata of a file. Search strings, content management, and redaction rules are configured via an XML file. A user-configurable character substitution map defined in JSON form is used to provide support for text obfuscation. The engine also comes with built-in regular expression support.


## Word search configuration

The word search configuration specifies the text or regular expression that should be searched for and how it should be treated when found within the document. The word search configuration is an extension to the Glasswall content management.

### XSD

```xml
<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="config" type="configType"/>
  <xs:complexType name="textSettingType">
    <xs:simpleContent>
      <xs:extension base="xs:string">
        <xs:attribute type="xs:string" name="replacementChar" use="optional"/>
      </xs:extension>
    </xs:simpleContent>
  </xs:complexType>
  <xs:complexType name="textItemType">
    <xs:sequence>
      <xs:element type="xs:string" name="text" minOccurs="0"/>
      <xs:element type="xs:string" name="regex" minOccurs="0"/>
      <xs:element type="textSettingType" name="textSetting"/>
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="textListType">
    <xs:sequence>
      <xs:element type="textItemType" name="textItem" maxOccurs="unbounded" minOccurs="0"/>
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="textSearchConfigType">
    <xs:sequence>
      <xs:element type="textListType" name="textList"/>
    </xs:sequence>
    <xs:attribute type="xs:string" name="libVersion"/>
  </xs:complexType>
  <xs:complexType name="configType">
    <xs:sequence>
      <xs:element type="textSearchConfigType" name="textSearchConfig"/>
    </xs:sequence>
  </xs:complexType>
</xs:schema>
```
### Example word search configuration

Here is an example of a word search configuration:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <wordConfig>
        <embedded_files>sanitise</embedded_files>
        <internal_hyperlinks>sanitise</internal_hyperlinks>
        <external_hyperlinks>sanitise</external_hyperlinks>
        <macros>sanitise</macros>
        <metadata>sanitise</metadata>
        <review_comments>allow</review_comments>
    </wordConfig>
    <sysConfig>
        <interchange_type>xml</interchange_type>
    </sysConfig>
    <textSearchConfig libVersion="core2">
        <textList>
            <textItem>
                <text>cats</text>
                <textSetting replacementChar="*">allow</textSetting>
            </textItem>
            <textItem>
                <regex>l\S+e</regex>
                <textSetting replacementChar="!">redact</textSetting>
            </textItem>
            <textItem>
                <regex>hello</regex>
                <textSetting replacementChar="!">disallow</textSetting>
            </textItem>
        </textList>
    </textSearchConfig>
</config>
```

In this example we are searching for the text "cats" and allowing it, searching for the regular expression "l\S+e" and redacting it, and searching for the text "hello" and disallowing it. The `textSetting` element accepts the following options:
* `allow` - Allowing an item will not apply redaction, but will mention the item in the word search report if it is found
* `disallow` - Disallowing an item will flag the document as non-conforming if the item is found
* `redact` - Redacting an item will replace the text with the replacement character specified. For example, "cats" will be replaced with "****"

## API

Each of the APIs returns a `Status` type, which is defined as follows:

```c++
enum Status {
    eFail,
    eSuccess
};
```
### GwWordSearch

This is used to call the word search engine, process the specified input file and produce an output file along with a word search report.

```c++
Status GwWordSearch(
    void* input_buffer, 
    size_t input_buffer_len, 
    void** output_buffer, 
    size_t* output_buffer_len, 
    void** output_report_buffer, 
    size_t* output_report_buffer_len, 
    const char* homoglpyhs, 
    const char* xml_config_string
)
```

Name | Type | Direction | Description
---- | ---- | --------- | -----------
input_buffer | `void *` | In | A pointer to the buffer containing the input file to be processed
input_buffer_len | `size_t` | In | The size of the input file buffer
output_buffer | `void **` | Out | A pointer to a pointer to a buffer that will be populated with the processed file buffer. This buffer is allocated by the word search engine
output_buffer_len | `size_t *` | Out | A pointer to the size of the output file buffer. This will be set by the word search engine
output_report_buffer | `void **` | Out | A pointer to a pointer to a buffer that will be populated with the word search report buffer. This buffer is allocated by the word search engine
output_report_buffer_len | `size_t *` | Out | A pointer to the size of the word search report. This will be set by the word search engine
homoglyphs | `const char *` | In | A pointer to the buffer containing the homoglyphs file. This buffer needs to be null terminated
xml_config_string | `const char *` | In | A pointer to the buffer containing the content management XML file. This buffer needs to be null terminated

### GWWordSearchDone

This is used to release any resources that have been allocated by the word search engine. This function needs to be called after each call made to the `GwWordSearch` function otherwise memory leaks will occur.

```c++
Status GwWordSearchDone(
    void** output_buffer,
    size_t* output_buffer_len, 
    void** output_report_buffer, 
    size_t* output_report_buffer_len
);
```

Name | Type | Direction | Description
---- | ---- | --------- | -----------
output_buffer | `void **` | Out | A pointer to a pointer to the buffer containing the processed file that will be freed by the word search library
output_buffer_len | `size_t *` | Out | A pointer to the size of the output file buffer
output_report_buffer | `void **` | Out | A pointer to a pointer to the buffer containing the word search report that will be freed by the word search library
output_report_buffer_len | `size_t *` | Out | A pointer to the size of the word search report

## Usage example

Here we have an example C++ application that takes an input file, processes it using the Glasswall Word Search engine, and then produces an output file alongside a word search analysis report. This example application expects the following commandline parameters:

1. Path to the content management configuration XML.
2. Path to the homoglyphs file.
3. Path to the input file to be processed.
4. Path to the output file where the processed file will be stored.

```c++
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstddef>
#include <stdexcept>

#include "api.h"

using namespace std;

// Read the file into a buffer
vector<uint8_t> readFile(ifstream &fileHandle, const string &filePath, bool nullTerminator)
{
    fileHandle.exceptions(ifstream::failbit | ifstream::badbit);
    fileHandle.open(filePath.c_str(), ios::binary | ios::ate);

    vector<uint8_t> data;
    streamsize size = fileHandle.tellg();
    fileHandle.seekg(0, ios::beg);

    data.resize(size + 1);
    fileHandle.read(reinterpret_cast<char *>(data.data()), size);

    if (nullTerminator)
    {
        data.push_back(0);
    }

    return data;
}

int main(int argc, char **argv)
{
    if (argc != 5)
    {
        cout << "Usage: <Path to XML Config> <Path to Homoglyphs> <Input file> <Output file>" << endl;
        return -1;
    }

    // Read commandline arguments
    string xmlFilePath(argv[1]);
    string homoglyphsFilePath(argv[2]);
    string inputFilePath(argv[3]);
    string outputFilePath(argv[4]);

    // Create file handles for input files
    ifstream xmlFileHandle;
    ifstream homoglyphsFileHandle;
    ifstream inputFileHandle;

    // Read files into buffers
    vector<uint8_t> xmlBuffer = readFile(xmlFileHandle, xmlFilePath, true);                         // Buffer containing the XML content management settings. This is null terminated
    vector<uint8_t> homoglyphsBuffer = readFile(homoglyphsFileHandle, homoglyphsFilePath, true);    // Buffer containing the homoglyphs. This is null terminated
    vector<uint8_t> inputBuffer = readFile(inputFileHandle, inputFilePath, false);                  // Buffer containing the input file to be processed

    // Create variables for output buffers
    void * outputBuffer = nullptr;          // Output buffer for processed file
    size_t outputBufferSize = 0;            // Output buffer size
    void * outputReportBuffer = nullptr;    // Output buffer for report file
    size_t outputReportBufferSize = 0;      // Output report buffer size

    // Run word search and redact
    Status status = GwWordSearch(inputBuffer.data(), inputBuffer.size(), &outputBuffer, &outputBufferSize, &outputReportBuffer, &outputReportBufferSize, reinterpret_cast<const char*>(homoglyphsBuffer.data()), reinterpret_cast<const char *>(xmlBuffer.data()));

    if (status == Status::eSuccess)
    {
        // Write out the processed output file if the word search and redact was successful
        ofstream outputFileHandle(outputFilePath, ios::binary | ios::trunc);

        if (outputFileHandle.is_open())
        {
            outputFileHandle.write(static_cast<const char *>(outputBuffer), outputBufferSize);
        }

        outputFileHandle.close();
    }

    // Write out the report file
    ofstream analysisFileHandle(outputFilePath + ".xml", ios::binary | ios::trunc);

    if (analysisFileHandle.is_open())
    {
        analysisFileHandle.write(static_cast<const char *>(outputReportBuffer), outputReportBufferSize);
    }

    analysisFileHandle.close();

    // Call done to release any allocated resources
    GwWordSearchDone(&outputBuffer, &outputBufferSize, &outputReportBuffer, &outputReportBufferSize);

    return 0;
}
```

## Common Issues

### Word search is not processing files

If word search is not processing files correctly then there may be a few reasons that can cause this:
* When running word search please ensure that all the Glasswall libraries are located in the same directory, which also needs to be set as the current working directory. Glasswall searches within the current working directory for it's dependencies and if they are not found then files will not be processed correctly.
* Check whether the license has expired. Unfortunately at this time there is no function to retrieve the remaining time on the license, but it can be done by processing a file in Analysis mode and then checking the analysis report for a license expiration issue.

### Running word search on Centos 7

When running the word search engine in Centos 7 please ensure that `libstdc++.so.6` library that is located within this repo is placed within the same directory as the word search library. This is a temporary work around to enable the word search library to work on Centos 7, while a proper fix is implemented. 
