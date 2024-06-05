from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database import get_async_session
from backend.src.stations.models import station
from backend.src.stations.schemas import StationCreate, StationUpdate

router = APIRouter(
    prefix="/stations",
    tags=["stations"],
)

@router.post("/", response_model=StationCreate)
async def create_station(station_create: StationCreate,
                         session: AsyncSession = Depends(get_async_session)):
    """
    Create a new station
    """
    try:
        stmt = insert(station).values(**station_create.dict())
        await session.execute(stmt)
        await session.commit()
        return station_create
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{station_id}")
async def get_station(station_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get a station by ID
    """
    try:
        query = select(station).where(station.c.id == station_id)
        result = await session.execute(query)
        data = result.mappings().all()
        if not data:
            raise HTTPException(status_code=404, detail="Station not found")
        return dict(data[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{station_id}")
async def update_station(station_id: int, updated_station: StationUpdate,
                         session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Update a station by ID
    """
    try:
        existing_station = await get_station(station_id, session)
        update_data = updated_station.dict(exclude_unset=True)

        if "type" in update_data and update_data["type"] not in ["pc", "ps", "vr"]:
            raise HTTPException(status_code=400, detail="Invalid station type. Must be one of: pc, ps, vr")

        updated_data = {**existing_station, **update_data}

        stmt = (
            update(station)
            .where(station.c.id == station_id)
            .values(**{k: v for k, v in updated_data.items() if k != "id"})  # Исключаем столбец "id" из обновления
        )
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "ok",
            "data": updated_data,
        }
    except HTTPException as e:
        return {
            "status": "error",
            "data": str(e.detail),
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.delete("/{station_id}")
async def delete_station(station_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a station by ID
    """
    try:
        await get_station(station_id, session)
        stmt = delete(station).where(station.c.id == station_id)
        await session.execute(stmt)
        await session.commit()
        return {"message": "Station deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=str(e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
