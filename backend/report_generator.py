import aspose.pdf as ap
from io import BytesIO


def get_rpz_report(wares) -> bytes:
    """
    return: a full РПЗ PDF file
    wares: Данные о грузах
    """
    replacements = {
        'total_ct_in_van': 'наша формула успешно отработала'
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