from six import BytesIO

from thumbs.types.base import CmdThumbTypeBase
from thumbs.types.pdf import PdfThumbType


class DocsThumbType(CmdThumbTypeBase):
    file_output = True
    buffer_output = True
    cmds = ['/usr/bin/unoconv']
    args = [
        '-f', 'pdf',
        '-e', 'PageRange=1-1',
        # '--output={output_file}',
        '--stdout',
        '{input_file}',
    ]

    def create(self, input_file, output_file=None, dimensions=None, tformat='jpeg', **kwargs):
        buffer = super(DocsThumbType, self).create(input_file, None, dimensions, tformat, **kwargs)
        PdfThumbType().create(buffer, output_file, dimensions, tformat, **kwargs)