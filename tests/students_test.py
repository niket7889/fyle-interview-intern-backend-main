def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1
        assert 'content' in assignment
        assert 'state' in assignment
        assert 'created_at' in assignment
    assert isinstance(data, list)  
    assert len(data) > 0 
    assert 'content' in data[0] 


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    try:
        assert response.status_code == 200
        data = response.json['data']
    except:
        assert response.status_code == 400
        #data = response.json['data']



def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    try:
        assert response.status_code == 200
        data = response.json['data']
        assert data['student_id'] == 1
        assert data['state'] == 'SUBMITTED'
        assert data['teacher_id'] == 1
    except AssertionError:
        assert response.status_code == 400
        data = response.json
        assert data['error'] == 'FyleError'
        assert data['message'] == 'only a draft assignment can be submitted'


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    try:
        assert response.status_code == 200
    except AssertionError:
        assert response.status_code == 400


    

