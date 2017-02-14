import subprocess

import os

from thumbs.types.base import CmdThumbTypeBase


DEFAULT_SS = '3'
DEFAULT_SS_PCNT = 20
MEDIAINFO = '/usr/bin/mediainfo'


class VideoThumbType(CmdThumbTypeBase):
    file_output = True
    cmds = ['/usr/bin/ffmpeg']
    args = [
        # '-v', 'quiet',
        '-ss', '{{ss}}',
        '-i', '{input_file}',
        '-frames:v', '5',
        '-r', '1/10',
        '-y',  # Overwrite
        '-vsync', 'vfr',
        # '-f', '{tformat}',
        '{output_file}',
    ]

    def get_duration(self, input_file):
        if not os.path.exists(MEDIAINFO):
            return
        output = subprocess.check_output([MEDIAINFO, '--Inform=General;%Duration%', input_file])
        duration = output.strip()
        if not duration.isdigit():
            return
        return int(duration) / 1000

    def parse_args(self, cmd, input_file, output_file, dimensions, tformat, **kwargs):
        tformat = {'jpeg': 'jpg'}.get(tformat, tformat)
        args = super(VideoThumbType, self).parse_args(cmd, input_file, output_file, dimensions, tformat, **kwargs)
        duration = self.get_duration(input_file)
        ss = (duration / 100) * DEFAULT_SS_PCNT if duration else DEFAULT_SS
        args = [x.format(ss=ss) for x in args]
        return args
