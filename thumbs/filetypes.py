from thumbs.types.docs import DocsThumbType
from thumbs.types.image import ImageThumbtype
from thumbs.types.pdf import PdfThumbType
from thumbs.types.sourcecode import SourceCodeThumbType
from thumbs.types.video import VideoThumbType

mimetypes = {
    'application/pdf': PdfThumbType,
    'application/vnd.oasis.opendocument.text': DocsThumbType,
    'application/x-yaml': SourceCodeThumbType,
    'application/x-php': SourceCodeThumbType,
    'application/xml': SourceCodeThumbType,
    'application/json': SourceCodeThumbType,

    'text': SourceCodeThumbType,
    'image': ImageThumbtype,
    'video': VideoThumbType,
}


def get_type_class(mimetype):
    part1, part2 = mimetype.split('/')
    return mimetypes.get(mimetype) or mimetypes.get(part1)
