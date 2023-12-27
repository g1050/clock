class ChineseUnicodeConverter:
    def __init__(self, input_file=None, output_file=None):
        self.input_file = input_file
        self.output_file = output_file

    def _convert_to_unicode(self, input_str):
        unicode_str = ""
        for char in input_str:
            unicode_char = hex(ord(char))[2:]
            unicode_str += "\\u" + unicode_char.zfill(4)
        return unicode_str

    def _replace_unicode_format(self, unicode_str):
        # 将类似\u963f替换成0x963f
        return unicode_str.replace("\\u", "0x")

    def convert_file(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                unicode_content = self._convert_to_unicode(content)
                formatted_content = self._replace_unicode_format(unicode_content)

            with open(self.output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(formatted_content)

            print(f"Conversion successful. Formatted content written to {self.output_file}")
        except FileNotFoundError:
            print(f"Error: File not found - {self.input_file}")
        except Exception as e:
            print(f"Error: {str(e)}")

# 示例使用
converter = ChineseUnicodeConverter(input_file='character/common3500.txt', output_file='txt/output.txt')
converter.convert_file()
