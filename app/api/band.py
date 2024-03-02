from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.core.database import get_session
from app.models import BandRead
from app.schema import Band
from app.service.band import get_band_list

router = APIRouter()


@router.get(
    "",
    description="Get the list of bands in the database.",
    response_model=list[BandRead],
)
async def get_bands(session=Depends(get_session)):
    bands = session.exec(select(Band)).all()
    return [BandRead.model_validate(band.dict()) for band in bands]


@router.post("", description="Add a new band info to the database from user input.")
async def add_band(band: Band, session=Depends(get_session)):
    db_band = session.get(Band, band.id)
    if db_band:
        raise HTTPException(
            status_code=400,
            detail=f"Band already exists in database (id: {band.id}, name: {band.name})",
        )
    session.add(band)
    session.commit()
    session.refresh(band)
    return {"band_id": band.id, "band_name": band.name}


@router.post(
    "/from_band_us",
    name="Add band from band.us",
    description="Get the list of bands that the user is a member of from band.us",
)
async def add_band_from_band(
    band_list=Depends(get_band_list), session=Depends(get_session)
):
    for band in band_list:
        db_band = session.get(Band, band["band_id"])
        if db_band:
            continue
        session.add(Band(**band))

    return band_list
