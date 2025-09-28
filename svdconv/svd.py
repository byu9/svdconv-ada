from lxml import etree

from .ada import create_ada_package_spec


def _create_message(el, message):
    el_path = el.getroottree().getpath(el)
    return f'{el_path}: {message}'


def _read_text_from_child(el, child_el_name: str):
    child_el = el.find(child_el_name)

    if child_el is None:
        raise ValueError(_create_message(el, f'Cannot find child element "{child_el_name}".'))

    return child_el.text.strip()


def _read_integer_from_child(el, child_el_name: str):
    integer_literal = _read_text_from_child(el, child_el_name)

    if integer_literal.startswith('0b'):
        integer_val = int(integer_literal.lstrip('0b'), base=2)

    elif integer_literal.startswith('#'):
        integer_val = int(integer_literal.lstrip('#'), base=2)

    elif integer_literal.startswith('0x'):
        integer_val = int(integer_literal.lstrip('0x'), base=16)

    else:
        integer_val = int(integer_literal, base=10)

    return integer_val


def _write_spec_for_interrupts(device_el, output_folder: str):
    # Sort interrupts by their numbers
    interrupt_els = sorted(
        device_el.xpath('.//interrupt'),
        key=lambda el: _read_integer_from_child(el, 'value')
    )

    with create_ada_package_spec('Ada.Interrupts.Names', output_folder=output_folder) as spec:
        for interrupt_el in interrupt_els:
            spec.write_comment(_read_text_from_child(interrupt_el, 'description'))
            spec.add_object_decl(
                identifier=_read_text_from_child(interrupt_el, 'name'),
                subtype_mark='Interrupt_ID',
                constant=True,
                init_expr=_read_integer_from_child(interrupt_el, 'value')
            )
            spec.write_line()


def write_spec_for_device(svd_filename, output_folder):
    xml_tree = etree.parse(svd_filename)
    device_el = xml_tree.getroot()

    _write_spec_for_interrupts(device_el, output_folder=output_folder)
