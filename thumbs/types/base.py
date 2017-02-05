import os
import subprocess
import tempfile

import six

from thumbs.exceptions import ThumbNotAvailable

DEFAULT_DIMENSIONS = (128, 128)
TEMP_FILE_PREFIX = 'python_thumb_'


def is_buffer(p):
    return not isinstance(p, six.string_types)


def buffer_to_file(buffer, file=None):
    file = file or get_temp_file().name
    with open(file, 'wb') as f:
        for piece in iter(lambda: buffer.read(1024 * 8), b''):
            f.write(piece)
    return file


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
    buffer_input = False
    file_input = True

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
        o_file = output_file
        buffer = None
        stdin = None
        if is_buffer(input_file) and self.buffer_input:
            stdin = input_file
        if is_buffer(input_file) and not self.buffer_input:
            i_file = getattr(input_file, 'file', None) or buffer_to_file(input_file)
        if not output_file and not self.buffer_output:
            # Buffer no disponible. Debo escribir a un archivo temporal
            buffer = get_temp_file()
            o_file = buffer.name
        p = subprocess.Popen([cmd] + self.parse_args(cmd, i_file, o_file, dimensions, tformat, **kwargs),
                             stdout=subprocess.PIPE, stdin=stdin)
        if output_file and not self.file_output:
            # Se requiere un archivo, pero sólo hay buffer
            # p.communicate()
            buffer_to_file(p.stdout, output_file)
        if output_file and is_buffer(output_file):
            # Se ha entregado un buffer para el output. Lo devuelvo.
            return output_file
        elif output_file:
            # Devuelvo el file object del output_file si es lo que se requería
            p.communicate()
            return open(output_file, 'rb')
        else:
            # Si se requería en su lugar el buffer, lo devuelvo
            return buffer or p.stdout
