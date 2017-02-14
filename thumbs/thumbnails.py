import mimetypes
from thumbs.exceptions import ThumbNotAvailable

mimetypes.add_type('application/x-yaml', '.yml')
mimetypes.add_type('application/x-php', '.php')
mimetypes.add_type('text/plain', '.init')
mimetypes.init()


FORMATS = {
    'jpg': 'jpeg',
    'png': 'png',
    'gif': 'gif',
}


def thumb(input_file, output_file=None, dimensions=None, tformat=None, **kwargs):
    from thumbs.filetypes import get_type_class
    if tformat is None:
        tformat = FORMATS.get(output_file.split('.')[-1])
    mimetype = mimetypes.guess_type(input_file)[0]
    if mimetype is None:
        raise ThumbNotAvailable
    type_class = get_type_class(mimetype)
    if type_class is None:
        raise ThumbNotAvailable
    return type_class().create(input_file, output_file, dimensions, tformat, **kwargs)