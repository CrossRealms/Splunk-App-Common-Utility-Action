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




class ConfigFileHandler(BaseFileHandler):

    def _util_write_config_option(self, writer_parser: configparser.ConfigParser, sect, key, value):
        if not writer_parser.has_section(sect):
            writer_parser.add_section(sect)
        writer_parser.set(sect, key, value)


    def get_config_parser_object(self):
        config = configparser.ConfigParser(interpolation=None)
        # config.optionxform = str
        config.optionxform = lambda option: option
        return config


    def validate_config(self):
        input_content = self.get_input_file_content()
        temp_file = '{}_temp'.format(self.input_file_path)
        with open(temp_file, 'w') as f:
            f.write(input_content)

        input_parser = self.get_config_parser_object()
        input_parser.read(temp_file)

        output_parser = self.get_config_parser_object()
        if os.path.isfile(self.output_file_path):
            output_parser.read(self.output_file_path)

        is_changed = False

        for sect in input_parser.sections():
            for key, value in input_parser.items(sect):
                # print("stanza={} - key={} - value={}".format(sect, key, value))
                try:
                    already_present_value = output_parser.get(sect, key)
                    if already_present_value != value:
                        is_changed = True
                        self._util_write_config_option(output_parser, sect, key, value)
                except:
                    is_changed = True
                    self._util_write_config_option(output_parser, sect, key, value)
        
        if is_changed:
            print("File changed - file={}".format(self.output_file_path))
            self.create_output_directory_path_if_not_exist()
            fp=open(self.output_file_path, 'w')
            output_parser.write(fp)
            fp.close()



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
