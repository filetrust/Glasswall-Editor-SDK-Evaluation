from SislParser import SislParser


def return_error(error):
    return error


def validate(sisl_file):
    sisl_file = ""
    group_counter = 0
    has_reached_eof = False

    sisl_parser = SislParser()
    tokens = sisl_parser.tokenize_sisl(sisl_file)

    for index, token in enumerate(tokens):
        if token.type == sisl_parser.SislTokenType.ST_GROUP_BEGIN:
            group_counter += 1
        if token.type == sisl_parser.SislTokenType.ST_GROUP_END:
            group_counter -= 1
        if token.type == sisl_parser.SislTokenType.ST_EOF:
            has_reached_eof = True

    if groupCounter != 0:
        return_error("EOF too early")
