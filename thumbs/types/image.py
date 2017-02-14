from thumbs.types.base import CmdThumbTypeBase


class ImageThumbtype(CmdThumbTypeBase):
    file_output = True
    image_formats = ['jpeg', 'png', 'gif']
    dimensions = True

    cmds = ['/usr/bin/convert']
    args = [
        '{input_file}',
        '-quality', '95',
        '{output_file}',
    ]

    def get_args(self, cmd, input_file, output_file, dimensions, tformat, **kwargs):
        args = super(ImageThumbtype, self).get_args(cmd, input_file, output_file, dimensions, tformat, **kwargs)
        if dimensions:
            width, height = dimensions.get('width', ''), dimensions.get('height', '')
            resize_action = dimensions.get('resize', 'exact')
            resize = '{}x{}'.format(width, height)
            if resize_action == 'max':
                resize += '^'
            if resize_action == 'exact':
                assert width and height
            args = ['-resize', resize] + args
        return args

