from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

from .schema import AssignmentSchema, AssignmentGradeSchema

student_assignments_resources = Blueprint('student_assignments_resources', __name__)

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principal_assignments = Assignment.get_assignments_by_principal()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)
    return APIResponse.respond(data={"error": "An error occurred while fetching assignments"})


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):

    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


    '''
    """Grades an assignment"""
    try:
        assignment_id = incoming_payload.get('id')
        grade = incoming_payload.get('grade')

        # Ensure grade is valid
        if grade not in [GradeEnum.A.value, GradeEnum.B.value, GradeEnum.C.value, GradeEnum.D.value, GradeEnum.F.value]:
            return APIResponse.respond(data={"error": "Invalid grade"}, status_code=400)

        assignment = Assignment.query.get(assignment_id)

        if not assignment:
            return APIResponse.respond(data={"error": "Assignment not found"}, status_code=404)

        if assignment.state == AssignmentStateEnum.DRAFT:
            return APIResponse.respond(data={"error": "Assignment is in draft state and cannot be graded"}, status_code=400)

        assignment.grade = GradeEnum(grade)
        assignment.state = AssignmentStateEnum.GRADED
        db.session.commit()

        assignment_dump = AssignmentSchema().dump(assignment)
        return APIResponse.respond(data=assignment_dump, status_code=200)
    
    except Exception as e:
        print(f"Error grading assignment: {e}")
        return APIResponse.respond(data={"error": "An error occurred while grading the assignment"}, status_code=500)
        '''



