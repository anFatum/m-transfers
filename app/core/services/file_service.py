import io

import pandas as pd
from flask import send_file

from app.core.utils.abc import EnumWithValues


class FileFormat(EnumWithValues):
    XLSX = "xlsx"


def download_xlsx_file(generated_df: pd.DataFrame):
    return_data = io.BytesIO()
    with pd.ExcelWriter(return_data) as excel_file:
        generated_df.to_excel(excel_file, index=False)
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)

    return send_file(return_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     attachment_filename='download_filename.xlsx')
