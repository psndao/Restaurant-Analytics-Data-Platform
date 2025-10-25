from fastapi import Query

def pagination_defaults(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    return {"skip": skip, "limit": limit}
