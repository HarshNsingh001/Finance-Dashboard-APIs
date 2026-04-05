from typing import Any


def success_response(
    data: Any = None,
    message: str = "Success",
    meta: dict | None = None,
) -> dict:
    response = {
        "success": True,
        "message": message,
        "data": data,
    }
    if meta:
        response["meta"] = meta
    return response


def paginated_response(
    data: list,
    total: int,
    page: int,
    limit: int,
    message: str = "Success",
) -> dict:
    total_pages = (total + limit - 1) // limit
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }
