from tests.conftest import *

# TODO: more modular separation of tests, now just indicated in comments
@pytest.mark.usefixtures('live_server')
class TestLiveServerInteraction:
# SETTING UP
    def test_creates_db(self):
        # To save time, we will just create all and drop all, neither migrate, nor proper test-transaction handling
        db.create_all()

    def test_seeds_the_database(self):
        books_to_add = [Book(title=f'Great Book Title {i}') for i in range(100)]
        db.session.add_all(books_to_add)
        db.session.commit()

# ADD REQUESTS TEST
    def test_non_json_request_gets_rejected(self):
        resp = requests.post(url_for('api.add_request', _external=True))
        assert resp.status_code == 400, "Invalid status code"

    def test_nonmatching_json_gets_rejected(self):
        resp = requests.post(url_for('api.add_request', _external=True), json={"testing": "this"})
        string_found = "'email' is a required" in resp.json()['error']
        assert resp.status_code == 422 and string_found, "Invalid status code or error"

    def test_title_missing_from_json_returns_error(self):
        resp = requests.post(url_for('api.add_request', _external=True), json={"email": "fake@email.com"})
        string_found = "'title' is a required" in resp.json()['error']
        assert resp.status_code == 422 and string_found, "Invalid status code or error"

    def test_malformed_email_in_json_returns_error(self):
        resp = requests.post(url_for('api.add_request', _external=True), json={"title": "this", "email": "what?"})
        string_found = "Failed validating 'pattern' in schema['properties']['email']" in resp.json()['error']
        assert resp.status_code == 422 and string_found, "Invalid status code or error"

    def test_wrong_type_supplied_returns_type_error(self):
        resp = requests.post(url_for('api.add_request', _external=True), json={"title": 1.5253,
                                                                               "email": "fake@email.com"})
        string_found = "is not of type 'string'" in resp.json()['error']
        assert resp.status_code == 422 and string_found, "Invalid status code or error"

    def test_correct_json_element_returns_without_error(self):
        resp = requests.post(url_for('api.add_request', _external=True), json={"title": "this",
                                                                               "email": "fake@email.com"})
        assert resp.status_code == 204, "Invalid status code"

    # TODO: Test Server error(s) by mocking - skipping, due to time constraints

    def test_existing_title_creates_request(self):
        resp = requests.post(url_for('api.add_request', _external=True), json={"title": "Great Book Title 1",
                                                                               "email": "fake@email.com"})
        assert resp.status_code == 201, "Invalid status code or error"

    def test_existing_requests_returns_old_request(self):
        resp = requests.post(url_for('api.add_request', _external=True), json={"title": "Great Book Title 1",
                                                                               "email": "fake@email.com"})
        assert resp.status_code == 200, "Invalid status code or error"

# GET REQUESTS
    def test_get_request_with_no_json_responds_with_error(self):
        resp = requests.get(url_for('api.get_request', _external=True))
        assert resp.status_code == 400, "Invalid status code or error"

    def test_get_request_with_existing_responds_correctly(self):
        resp = requests.get(url_for('api.get_request', _external=True, id=1), json={"email": "fake@email.com"})
        assert resp.status_code == 200, "Invalid status code or error"

    def test_get_request_with_nonexistent_id_responds_correctly(self):
        resp = requests.get(url_for('api.get_request', _external=True, id=99), json={"email": "fake@email.com"})
        assert resp.status_code == 404, "Invalid status code or error"

# DELETE REQUESTS
    def test_delete_request_with_nonexistent_id_responds_correctly(self):
        resp = requests.delete(url_for('api.delete_request', _external=True, id=99), json={"email": "fake@email.com"})
        assert resp.status_code == 404, "Invalid status code or error"

    def test_delete_request_with_existing_id_deletes_record(self):
        request_before = db.session.query(BookRequest).filter(BookRequest.id == 1).first()
        resp = requests.delete(url_for('api.delete_request', _external=True, id=1), json={"email": "fake@email.com"})
        request_after = db.session.query(BookRequest).filter(BookRequest.id == 1).first()
        assert request_before and not request_after and resp.status_code == 200, 'Request was not deleted correctly'

    def test_teardown_database_correctly(self):
        # This is where transaction would be rolled back, connection closed etc.
        db.drop_all()
