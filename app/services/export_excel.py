import pandas as pd
from pathlib import Path
from typing import List
from fastapi.responses import StreamingResponse

async def transform_dict_to_df(aggregated_data: dict):
    aggregated_df = pd.DataFrame(aggregated_data)
    aggregated_df.insert(0, 'No', range(1, len(aggregated_df)+1))

    return aggregated_df

async def create_excel_file(file_path: Path, data_frames: List[pd.DataFrame]):
    kecamatan_df, kelurahan_df, rt_df, surveyor_df = data_frames

    with pd.ExcelWriter(file_path) as writer:
        kecamatan_df.to_excel(writer, sheet_name="Kecamatan", index=False)
        kelurahan_df.to_excel(writer, sheet_name="Kelurahan", index=False)
        rt_df.to_excel(writer, sheet_name="RT", index=False)
        surveyor_df.to_excel(writer, sheet_name="Surveyor", index=False)

    return file_path

def return_excel_file(file_path: Path, file_name: str):
    return  StreamingResponse(
                open(file_path, mode="rb"),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename={file_name}"}
            )