from core.database import get_session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models import BandRead
from schema import Band
from service.band import get_band_list
from sqlmodel import select

router = APIRouter()


@router.get(
    "",
    description="Get the list of bands in the database.",
)
async def get_bands(session=Depends(get_session)):
    bands = session.exec(select(Band)).all()
    data = [BandRead.model_validate(band.model_dump()).model_dump() for band in bands]
    return JSONResponse(
        content=data,
        media_type="application/json; charset=utf-8",
    )


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


@router.delete(
    "/{band_id}",
    description="Delete a band from the database.",
)
async def delete_band(band_id: str, session=Depends(get_session)):
    db_band = session.get(Band, band_id)
    if not db_band:
        raise HTTPException(
            status_code=404, detail=f"Band not found in database (id: {band_id})"
        )
    session.delete(db_band)
    session.commit()
    return {"band_id": band_id}


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
    return JSONResponse(
        content=band_list,
        media_type="application/json; charset=utf-8",
    )
