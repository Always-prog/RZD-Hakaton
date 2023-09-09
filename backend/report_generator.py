import aspose.pdf as ap
from io import BytesIO
import pandas as pd
import functions_for_boxes


def get_rpz_report(wares: pd.DataFrame) -> bytes:
    """
    return: a full РПЗ PDF file
    wares: Данные о грузах
    """

    replacements = {
        'gravity_height': 'gravity_height',
        'func_4_1': 'func_4_1'
    }
    # Load the template
    document = ap.Document("files/503р-template.pdf")

    for for_replace, target_replace in replacements.items():
        # Replace the replacements
        txt_absorber = ap.text.TextFragmentAbsorber(for_replace)
        document.pages.accept(txt_absorber)

        text_fragment_collection = txt_absorber.text_fragments

        for text_fragment in text_fragment_collection:
            text_fragment.text = target_replace

    # Return the file in bytes
    output = BytesIO()
    document.save(output)
    output.seek(0)
    return output.read()