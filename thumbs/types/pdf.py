from thumbs.types.base import CmdThumbTypeBase


class PdfThumbType(CmdThumbTypeBase):
    file_output = False
    buffer_input = True
    buffer_output = True
    image_formats = ['png']
    cmds = ['/usr/bin/pdftoppm']
    args = [
        # '-f', 'N',
        # '-scale-to', str(2048),
        '-png',
        # '{output_file}',
        # '-f', '{{page}}',
        # '-l', '{{page}}',
    ]
