import mimetypes
from thumbs.exceptions import ThumbNotAvailable

mimetypes.init()


def thumb(input_file, output_file=None, dimensions=None, tformat='jpeg', **kwargs):
    from thumbs.filetypes import get_type_class
    mimetype = mimetypes.guess_type(input_file)[0]
    if mimetype is None:
        raise ThumbNotAvailable
    type_class = get_type_class(mimetype)
    return type_class().create(input_file, output_file, dimensions, tformat, **kwargs)