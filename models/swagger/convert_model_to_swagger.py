import glob


def convert_to_jsdoc(f, is_property_file):
    jsdoc = []
    prefix = ' *    '

    if is_property_file:
        ref_path = '\"#/components/properties/'
    else:
        ref_path = '\"#/components/'

    for line in f:
        if line.startswith('$schema'):
            break

    for line in f:
        if line == '\n':
            break

    for line in f:
        if line.startswith('title: '):
            jsdoc_line = ''.join(
                [line[len('title: '):-1], ':\n', prefix, '  ', line])

        elif (array_ref_start := line.find('- $ref: ')) > 0:
            array_ref_len = len('- $ref: ')
            jsdoc_line = ''.join([
                '  ', line[:array_ref_start + array_ref_len], ref_path,
                line[array_ref_start + array_ref_len:-1], "\"\n"
            ])
        elif (ref_start := line.find('$ref: ')) > 0:
            ref_len = len('$ref: ')
            jsdoc_line = ''.join([
                '  ', line[:ref_start + ref_len], ref_path,
                line[ref_start + ref_len:-1], "\"\n"
            ])
        else:
            jsdoc_line = ''.join(['  ', line])

        if jsdoc_line == '  \n':
            jsdoc.append(' *\n')
        else:
            jsdoc.append(''.join([prefix, jsdoc_line]))

    jsdoc.append(' *\n')
    return jsdoc


def main():

    model_file_lines = []

    new_properties_lines = []
    for filename in sorted(glob.glob('../properties/*.yaml')):
        with open(filename) as in_file:
            new_properties_lines.extend(convert_to_jsdoc(in_file, True))

    new_schema_lines = []
    for filename in sorted(glob.glob('../*.yaml')):
        with open(filename) as in_file:
            new_schema_lines.extend(convert_to_jsdoc(in_file, False))

    model_file_lines.extend(['/**\n', ' *@swagger\n', ' *components:\n'])
    model_file_lines.extend([' *  properties:\n'])
    model_file_lines.extend(new_properties_lines)
    model_file_lines.extend([' *  schemas:\n'])
    model_file_lines.extend(new_schema_lines)
    model_file_lines.extend(['*/\n'])

    with open('models.js', 'w') as out_file:
        for line in model_file_lines:
            out_file.write(line)

    print('Creation of swagger jsdoc complete!')


if __name__ == '__main__':
    main()