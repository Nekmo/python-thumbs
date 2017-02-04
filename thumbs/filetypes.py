from thumbs.types.docs import DocsThumbType
from thumbs.types.video import VideoThumbType

mimetypes = {
    'application/vnd.oasis.opendocument.text': DocsThumbType,

    'video': VideoThumbType,
}


def get_type_class(mimetype):
    part1, part2 = mimetype.split('/')
    return mimetypes.get(mimetype) or mimetypes.get(part1)
