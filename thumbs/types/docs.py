from thumbs.types.base import CmdThumbTypeBase


class DocsThumbType(CmdThumbTypeBase):
    file_output = True
    cmds = ['/usr/bin/unoconv']
    args = [
        '-f', 'pdf',
        '-e', 'PageRange=1-1',
        '--output={output_file}',
        '{input_file}',
    ]
