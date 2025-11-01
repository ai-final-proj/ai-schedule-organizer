# backend/api/__init__.py
from flask import Flask
from flask_smorest import Api

def register_blueprints(app: Flask, api: Api) -> None:
    from .programs import blp as programs_blp
    from .users    import blp as users_blp
    from .cohorts  import blp as cohorts_blp
    from .roles    import blp as roles_blp
    from .schedules import blp as schedules_blp
    from .prompt import blp as prompt_blp

    api.register_blueprint(programs_blp,  url_prefix="/api/programs")
    api.register_blueprint(users_blp,     url_prefix="/api/users")
    api.register_blueprint(cohorts_blp,   url_prefix="/api/cohorts")
    api.register_blueprint(roles_blp,     url_prefix="/api/roles")
    api.register_blueprint(schedules_blp, url_prefix="/api")
    api.register_blueprint(prompt_blp, url_prefix="/api")
