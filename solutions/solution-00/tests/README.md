# How to run the tests

To run the tests, the API must be running on localhost:5000, the tests directory doesn't need to be in the same directory as the API, could be anywhere in the system.

> [!IMPORTANT]
> **In order to run the tests you need to be in the tests parent directory.**
>
> The only requirement is that you have to have installed the requests library, you can install it with the following command:

```bash
pip3 install requests
```

## You can run the tests in two ways

### 1. Running the tests individually

There is a test for each task:

- 3. users
- 4. countries
- 5. amenities
- 6. places
- 7. reviews

> `python3 -m tests.test_{entity_name}`

```bash
$ ls -1 .
...
tests/
$ python3 -m tests.test_users
Test to retrieve all users: OK
Test to create a new user: OK
Test to retrieve a specific user by ID: OK
Test to update an existing user: OK
Test to delete an existing user: OK
Total tests: 5, OK: 5, FAIL: 0
```

### 2. Run all the tests at once

```bash
$ ls -1 .
...
tests/
$ python3 -m tests.run_all
# ------------------------- #
Results (Passed/Total):
Implement the User Management Endpoints (5/5):
Score: 100.0%
Implement the Country and City Management Endpoints (8/8):
Score: 100.0%
Implement the Amenity Management Endpoints (5/5):
Score: 100.0%
Implement the Places Management Endpoints (5/5):
Score: 100.0%
Implement the Review Management Endpoints (6/6):
Score: 100.0%
```
