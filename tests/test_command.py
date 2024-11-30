import io
import contextlib
import unittest
from padam.command import run


@contextlib.contextmanager
def uncloseable(fd):
    '''
    Context manager which turns the fd's close operation to no-op for the duration of the context.
    '''
    close = fd.close
    fd.close = lambda: None
    yield fd
    fd.close = close


class CommandTest(unittest.TestCase):
    def test_ok(self):
        project_yaml = '''
            part:
                shelf:
                    type: panel
                    length: 1600
                    width: 250
                    thickness: 18
        '''
        project = io.StringIO(project_yaml)
        stdout = io.StringIO()
        stderr = io.StringIO()
        output = io.StringIO()
        cutlist = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr), uncloseable(output), uncloseable(cutlist):
            run(project=project, output=output, cutlist=cutlist)
        self.assertIn('shelf', stdout.getvalue())
        self.assertIn('cube(', output.getvalue())
        self.assertIn('shelf', cutlist.getvalue())
