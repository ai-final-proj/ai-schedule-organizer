import enum

class RoleCode(enum.Enum):
    instructor = "instructor"
    learner = "learner"
    admin = "admin"
    replacement_instructor = "replacement_instructor"
    visiting_instructor = "visiting_instructor"

class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class PeriodCategory(enum.Enum):
    virtual_reality = "virtual_reality"
    face_to_face = "face_to_face"
    assessment = "assessment"
    learning_course = "learning_course"
    other = "other"
