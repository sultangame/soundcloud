from fastapi import HTTPException, status


async def detail_or_not_found(detail):
    if detail is not None:
        return detail
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
