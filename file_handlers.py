import os
import configparser
import pathlib


class BaseFileHandler:
    def __init__(self, input_file_path, output_file_path, words_for_replacement=dict(), create_directory_structure_if_not_exist=True) -> None:
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.words_for_replacement: dict = words_for_replacement

    def get_input_file_content(self):
        input_content = None
        with open(self.input_file_path, 'r') as fr:
            input_content = fr.read()
        
        for word, replacement in self.words_for_replacement.items():
            input_content = input_content.replace(word, replacement)

        return input_content
    
    def create_output_directory_path_if_not_exist(self):
        output_dir_path = os.path.dirname(self.output_file_path)
        pathlib.Path(output_dir_path).mkdir(parents=True, exist_ok=True)



class VCustomOutputConfigParser:
    '''
    NOTE - This is not fully custom ConfigParser, only required functions are overridden as needed.
    '''
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        if os.path.isfile(file_path):
            with open(self.file_path, 'r') as file_obj:
                self.file_content = file_obj.read().splitlines()
        else:
            self.file_content = []


    def _get_stanza(self, stanza_name):
        start_line = -1
        end_line = -1

        searching_for_start = True
        for line_no in range(len(self.file_content)):
            line = self.file_content[line_no]
            if not line and line != "":
                if not searching_for_start:
                    end_line = line_no - 1
                break

            line = line.strip()
            if line.strip().startswith('#'):   # comment, ignore
                continue

            if searching_for_start and line == '[{}]'.format(stanza_name):
                start_line = line_no
                searching_for_start = False

            elif not searching_for_start and line.startswith('[') and line.endswith(']'):
                end_line = line_no - 1
                return start_line, end_line

        return start_line, end_line


    def _get_attribute_line_no(self, key_to_search, start_line_no, end_line_no):
        _start_line_no = 0
        if start_line_no >= 0:
            _start_line_no = start_line_no
        
        if end_line_no >= 0:
            _end_line_no = end_line_no
        else:
            _end_line_no = len(self.file_content)

        for _line_no in range(_start_line_no, _end_line_no):
            _key, _value = self._get_key_value(self.file_content[_line_no])
            if _key == key_to_search:
                return _line_no

        return None


    def _get_key_value(self, line_content):
        _key = line_content.split("=")[0].strip()
        _value = "".join(line_content.split("=")[1:]).strip()
        return _key, _value


    def replace_content_with_input_parser(self, input_parser: configparser.ConfigParser):
        new_stanzas = []

        for sect in input_parser.sections():
            start_line_no, end_line_no = self._get_stanza(sect)

            if start_line_no >= 0:
                # For existing stanza

                new_key_value_pairs = []

                for key, value in input_parser.items(sect):
                    # print("stanza={} - key={} - value={}".format(sect, key, value))
                    line_no_to_update = self._get_attribute_line_no(key, start_line_no, end_line_no)
                    
                    if line_no_to_update:
                        # For existing attributes
                        self.file_content[line_no_to_update] = '{} = {}'.format(key, value)
                    else:
                        # For new attributes
                        new_key_value_pairs.append((key, value))

                # For new attributes
                line_no_to_update = end_line_no

                # Move up and add content above all comments and empty lines
                while True:
                    line = self.file_content[line_no_to_update].strip()
                    if line == '' or line.startswith("#"):
                        line_no_to_update -= 1
                        continue
                    break

                for new_key, new_value in new_key_value_pairs:
                    line_no_to_update += 1
                    self.file_content.insert(line_no_to_update, '{} = {}'.format(new_key, new_value))

            else:
                # For new stanzas
                new_stanzas.append(sect)

        # For new stanzas
        new_content = []
        for new_sect in new_stanzas:
            new_content.append('')
            new_content.append('[{}]'.format(new_sect))
            
            for key, value in input_parser.items(new_sect):
                new_content.append('{} = {}'.format(key, value))
        
        self.file_content.extend(new_content)




class ConfigFileHandler(BaseFileHandler):

    def _util_write_config_option(self, writer_parser: configparser.ConfigParser, sect, key, value):
        if not writer_parser.has_section(sect):
            writer_parser.add_section(sect)
        writer_parser.set(sect, key, value)


    def get_config_parser_object(self):
        config = configparser.ConfigParser(interpolation=None)
        # config.optionxform = str
        # comment_prefixes='#', allow_no_value=True --> to avoid removing comments from the file
        config.optionxform = lambda option: option
        return config


    def validate_config(self):
        input_content = self.get_input_file_content()
        temp_file = '{}_temp'.format(self.input_file_path)
        with open(temp_file, 'w') as f:
            f.write(input_content)

        input_parser = self.get_config_parser_object()
        input_parser.read(temp_file)

        output_parser = VCustomOutputConfigParser(self.output_file_path)
        existing_content = "\n".join(output_parser.file_content)

        output_parser.replace_content_with_input_parser(input_parser)
        new_content = "\n".join(output_parser.file_content)

        if existing_content != new_content:
            print("File changed - file={}".format(self.output_file_path))
            self.create_output_directory_path_if_not_exist()
            with open(self.output_file_path, 'w') as fp:
                fp.write(new_content)



class RawFileHandler(BaseFileHandler):

    def validate_file_content(self):
        input_content = self.get_input_file_content()

        already_present_file_content = None
        if os.path.isfile(self.output_file_path):
            with open(self.output_file_path, 'r') as fr:
                already_present_file_content = fr.read()

        if already_present_file_content != input_content:
            print("File changed - file={}".format(self.output_file_path))
            self.create_output_directory_path_if_not_exist()
            with open(self.output_file_path, 'w') as fw:
                fw.write(input_content)
