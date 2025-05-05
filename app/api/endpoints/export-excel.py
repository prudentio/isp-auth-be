from fastapi import APIRouter, Depends, Query, status
from app.infrastructure.db.session import get_db_dashboard
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.services.region_aggregate import get_aggregated_region_data
from app.services.surveyor_aggregate import get_aggregated_surveyor_data
from app.exceptions import CustomHTTPException
import pandas as pd
from app.infrastructure.config import settings
from fastapi.responses import StreamingResponse
from app.services.cache_manager import CacheManager
from datetime import datetime
from app.services.export_excel import transform_dict_to_df, create_excel_file, return_excel_file

cache_manager = CacheManager()
router = APIRouter()

@router.get("")
async def export_excel(
    db: AsyncSession = Depends(get_db_dashboard),
    kec_id: Optional[List[str]] = Query(None),
    kel_id: Optional[List[str]] = Query(None),
    rw_id: Optional[List[str]] = Query(None),
    rt_id: Optional[List[str]] = Query(None),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    if not start_date or not end_date:
        today = date.today()
        start_date = start_date or today
        end_date = end_date or today
    
    filters = [kec_id, kel_id, rw_id, rt_id, start_date, end_date]

    cache_data = cache_manager.get_cache(filters)
    
    if cache_data:
        file_path, file_name = cache_data

        return return_excel_file(file_path, file_name)
    
    aggregated_region_data = await get_aggregated_region_data(
            db,
            kec_id=kec_id,
            kel_id=kel_id,
            rw_id=rw_id,
            rt_id=rt_id,
            start_date=start_date,
            end_date=end_date,
            is_for_export_excel=True
        )

    if not aggregated_region_data:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="there is no aggregated region data found"
            )
    
    aggregated_surveyor_data = await get_aggregated_surveyor_data(
            db,
            kec_id=kec_id,
            kel_id=kel_id,
            rw_id=rw_id,
            rt_id=rt_id,
            start_date=start_date,
            end_date=end_date,
            is_for_export_excel=True
        )

    if not aggregated_surveyor_data:
            raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="there is no aggregated surveyor data found"
        )

    #Aggregate Kecamatan
    aggregated_kecamatan_df = await transform_dict_to_df(aggregated_region_data["kecamatan"])

    #Aggregate Kelurahan
    aggregated_kelurahan_df = await transform_dict_to_df(aggregated_region_data["kelurahan"])

    #Aggregate RT
    aggregated_rt_df = await transform_dict_to_df(aggregated_region_data["rt"])

    #Aggregate Surveyor
    aggregated_surveyor_dicts = [data.dict() for data in aggregated_surveyor_data]
    aggregated_surveyor_df = await transform_dict_to_df(aggregated_surveyor_dicts)

    #Create an excel file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"survey_report_{timestamp}.xlsx"
    file_path = settings.EXCEL_EXPORTS_DIR_PATH  / file_name

    if file_path.exists():
        file_path.unlink()

    data_frames = [
        aggregated_kecamatan_df, 
        aggregated_kelurahan_df, 
        aggregated_rt_df, 
        aggregated_surveyor_df
    ]

    await create_excel_file(file_path ,data_frames)

    cache_manager.set_cache(filters, file_path, file_name)

    return return_excel_file(file_path, file_name)