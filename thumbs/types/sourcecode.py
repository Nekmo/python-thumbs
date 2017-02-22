import io

from thumbs.exceptions import ThumbNotAvailable
from thumbs.types.base import ThumbTypeBase


class SourceCodeThumbType(ThumbTypeBase):
    file_output = False
    buffer_output = True
    image_formats = ['png']

    def is_availabile(self):
        try:
            import pygments
        except ImportError:
            return False
        return True

    def create_base(self, input_file, output_file=None, dimensions=None, tformat='jpeg', **kwargs):
        if not self.is_availabile():
            raise ThumbNotAvailable
        from pygments import highlight
        from pygments.lexers.python import PythonLexer
        from pygments.formatters.img import ImageFormatter
        lines = kwargs.get('lines', 25)
        try:
            o = open(input_file).readlines()
        except (UnicodeDecodeError, IOError):
            raise ThumbNotAvailable
        lines = ''.join(o[:lines])
        output = highlight(lines, PythonLexer(), ImageFormatter(font_name='NimbusMonoPS-Regular.otf',
                                                                line_numbers=False, image_format='png'))
        return io.BytesIO(output)
