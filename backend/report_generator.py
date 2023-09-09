from io import BytesIO
import functions_for_boxes as bx
import aspose.pdf as ap
import random
from platforms_stuff import select_platforms_by_cargos


def get_rpz_reports(cargos) -> list[bytes]:
    """
    return: a full РПЗ PDF file
    wares: Данные о грузах
    """
    results_pdf_files = []

    platforms = select_platforms_by_cargos(cargos)
    for platform in platforms:

        lst_height = [cargo['height'] for cargo in platform['cargos']]
        lst_weight = [cargo['weight'] for cargo in platform['cargos']]
        # type_hard = random.randint(1,10)
        # if type_hard > 3:
        #     type_hard = True
        # else:
        #     type_hard = False


        replacements = {
            # 'Func_four': str(bx.longitudinal_inertial_force_func_4_1(type_hard, lst_weight)),
            'gravity_height': str(bx.gravity_height(lst_height, lst_weight))
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
        results_pdf_files.append(output.read())
        output.close()

    return results_pdf_files
