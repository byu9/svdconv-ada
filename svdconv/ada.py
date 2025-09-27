from contextlib import contextmanager


class AdaUnitWriter:
    def __init__(self, file):
        self._file = file

    def write_line(self, line_text: str):
        print(line_text, file=self._file)

    def write_comment(self, text: str):
        for line in text.splitlines():
            self.write_line(f'--  {line}')

    def start_package_spec(self, unit_name: str):
        self.write_line(f'package {unit_name}')
        self.write_line('is')

    def end_package_spec(self, unit_name: str):
        self.write_line(f'end {unit_name};')

    def add_object_decl(self, identifier: str, subtype_mark: str, init_expr=None,
                        aliased=False, constant=False):

        self.write_line(identifier)
        if aliased:
            self.write_line('aliased')

        if constant:
            self.write_line('constant')

        self.write_line(f': {subtype_mark}')

        if init_expr is not None:
            self.write_line(f':= {init_expr}')

        self.write_line(';')


@contextmanager
def create_ada_unit_file(filename):
    with open(filename, 'w') as file:
        writer = AdaUnitWriter(file=file)

        try:
            yield writer

        finally:
            pass
