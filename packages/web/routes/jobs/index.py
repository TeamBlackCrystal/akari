from fastapi import APIRouter

from packages.shared.queues.notfound_fixer import readonly_notfound_fixer_queue

router = APIRouter(prefix='/jobs')

@router.get('')
async def index():
    waiting = await readonly_notfound_fixer_queue.count_jobs()
    running = await readonly_notfound_fixer_queue.count_jobs('running')
    completed = await readonly_notfound_fixer_queue.count_jobs('completed')
    return {'waiting': waiting, 'running': running, 'completed': completed}
