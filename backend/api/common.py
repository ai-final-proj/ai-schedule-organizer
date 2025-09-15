#backend/api/common.py
from flask import request, jsonify

def get_pagination(default_page=1, default_size=20, max_size=200):
    page = max(int(request.args.get("page", default_page)), 1)
    size = min(max(int(request.args.get("size", default_size)), 1), max_size)
    return page, size

def paginated_result(query, page, size, mapper):
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return jsonify({
        "total": total,
        "page": page,
        "size": size,
        "items": [mapper(x) for x in items]
    })
