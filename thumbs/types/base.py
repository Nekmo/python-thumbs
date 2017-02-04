import os
import subprocess
import tempfile

from thumbs.exceptions import ThumbNotAvailable

DEFAULT_DIMENSIONS = (128, 128)
TEMP_FILE_PREFIX = 'python_thumb_'


def buffer_to_file(buffer, file):
    with open(file, 'wb') as f:
        for piece in iter(lambda: buffer.read(1024 * 8), ''):
            f.write(piece)


def get_temp_file():
    return tempfile.NamedTemporaryFile(prefix=TEMP_FILE_PREFIX)


class ThumbTypeBase(object):

    def is_availabile(self):
        raise NotImplementedError

    def create(self, input_file, output_file=None, dimensions=None, format='jpeg', page=1):
        raise NotImplementedError


class CmdThumbTypeBase(ThumbTypeBase):
    cmds = ()
    args = ()
    buffer_output = False
    file_output = False

    def __init__(self):
        assert self.buffer_output or self.file_output, "Output is required."

    def is_availabile(self):
        return bool(self.get_cmd())

    def get_cmd(self):
        for cmd in self.cmds:
            if os.path.exists(cmd):
               return cmd

    def get_args(self, cmd, input_file, output_file, dimensions, tformat, **kwargs):
        return self.args

    def parse_args(self, cmd, input_file, output_file, dimensions, tformat, **kwargs):
        params = {x: y for x, y in dict(locals(), **kwargs).items() if x not in ['self', 'kwargs']}
        return [x.format(**params) for x in self.get_args(**params)]

    def create(self, input_file, output_file=None, dimensions=None, tformat='jpeg', **kwargs):
        cmd = self.get_cmd()
        if cmd is None:
            raise ThumbNotAvailable
        i_file = input_file  # Sólo para subprocess
        buffer = None
        if not input_file and not self.buffer_output:
            # Buffer no disponible. Debo usar un archivo temporal
            buffer = get_temp_file()
            i_file = buffer.name
        p = subprocess.Popen([cmd] + self.parse_args(cmd, i_file, output_file, dimensions, tformat, **kwargs),
                             stdout=subprocess.PIPE)
        if input_file and not self.file_output:
            # Se requiere un archivo, pero sólo hay buffer
            p.communicate()
            buffer_to_file(p.stdout, output_file)
        if input_file:
            p.communicate()
            return open(output_file, 'rb')
        else:
            return buffer or p.stdout
