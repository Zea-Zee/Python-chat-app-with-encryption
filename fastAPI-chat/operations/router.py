from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.operations import operation
from operations.shemas import OperationCreate


router = APIRouter(
    prefix='/operations',
    tags=['Operations']
)


@router.get('/get')
async def get_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return result.all()


@router.post('/add')
async def add_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    operation_data = new_operation.dict()
    operation_data['datetime'] = new_operation.datetime.replace(tzinfo=None)

    # Insert the operation into the database
    statement = insert(operation).values(**operation_data)
    await session.execute(statement)
    await session.commit()
    return 'Success'
