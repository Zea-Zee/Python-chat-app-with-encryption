from fastapi import APIRouter
from fastapi import Depends

from base_config import current_user
from tasks.tasks import send_email_report

router = APIRouter(prefix='/report', tags=['Report'])


@router.get('/report')
async def get_report(user=Depends(current_user)):
    send_email_report.delay(user.username)
    return {
        'OK': True,
        'status': 200,
        'data': 'email has been send',
        'details': None
    }
