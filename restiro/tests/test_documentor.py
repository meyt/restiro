import pytest
import locale as lib_locale

from os import makedirs
from os.path import join

from restiro import Documentor
from restiro.helpers import validate_locale_name
from restiro.tests.helpers import stuff_dir, temp_dir


# FIXME: empty spaces and new lines are redundant
excepted_pot = """msgid ""
msgstr ""

msgid ""
msgstr ""

msgid ""
msgstr ""

msgid ""
msgstr ""

msgid "
Delete a product with product ID, but actually its 
                marked as deleted. 
 
                After review the product can delete permanently. 
 
                List of products cannot delete: 
                - Products purchased on time 
                - Products related to a `seller` 
"
msgstr ""

msgid " 
"
msgstr ""

msgid " 
"
msgstr ""

msgid " 
"
msgstr ""

msgid " 
"
msgstr ""

msgid " 
"
msgstr ""

msgid " 
"
msgstr ""

msgid " Access Token 
"
msgstr ""

msgid " Can purchase this product"
msgstr ""

msgid " Product ID 
"
msgstr ""

msgid " Product Model "
msgstr ""

msgid " When product manufactured 
"
msgstr ""

msgid "Delete a product"
msgstr ""

msgid "Delete a seller"
msgstr ""

msgid "Get a seller"
msgstr ""

msgid "Get a seller"
msgstr ""

msgid "Get all products"
msgstr ""

msgid "Get sellers list"
msgstr ""

msgid "Online Store"
msgstr ""

msgid "Update a product"
msgstr ""

"""


def test_documentor():
    online_store_dir = join(stuff_dir, 'online_store')

    destination_dir = join(temp_dir, 'markdown_generator')
    makedirs(destination_dir, exist_ok=True)

    documentor = Documentor(
        title='Online Store',
        source_dir=online_store_dir,
        generator_type='markdown'
    )

    # Try with an invalid generator
    with pytest.raises(ValueError):
        Documentor(
            title='Online Store',
            source_dir=online_store_dir,
            generator_type='blabla'
        ).generate(destination_dir)

    # Generate output
    documentor.generate(destination_dir)

    # Generate output in supported locales
    locales_dir = join(temp_dir, 'locales')
    makedirs(locales_dir, exist_ok=True)

    def add_translation(locale):
        import polib
        locale_dir = join(locales_dir, locale)
        messages_dir = join(locale_dir, 'LC_MESSAGES')
        makedirs(messages_dir)
        locale_po_file = join(messages_dir, 'restiro.po')
        locale_mo_file = join(messages_dir, 'restiro.mo')
        with open(locale_po_file, 'w') as f:
            f.write('')
        po = polib.pofile(locale_po_file)
        po.save_as_mofile(locale_mo_file)

    add_translation('en_US')
    add_translation('fa_IR')
    add_translation('un_kn')
    documentor.generate(destination_dir, locales_dir, 'en_US')
    documentor.generate(destination_dir, locales_dir, 'fa_IR')
    with pytest.raises(lib_locale.Error):
        documentor.generate(destination_dir, locales_dir, 'un_kn')

    # Extract translations template file
    documentor.generate_gettext(temp_dir)

    with open(join(temp_dir, 'restiro.pot'), 'r') as f:
        pot_source = ''.join(f.readlines())
        assert pot_source == excepted_pot


def test_validate_locale_name():
    assert validate_locale_name('en_US')
    assert validate_locale_name('gsw_FR')
    assert not validate_locale_name('gsw-FR')
    assert not validate_locale_name('111')
    assert not validate_locale_name('00_00')
