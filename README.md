## Setup via docker-compose

1. Clone the repository:
    ```sh
    $ git@github.com:Vlad0n20/webcase_test_task.git
    ```
2. Populate env.example and end.db.example files and rename it on .env  and .env.db
3. Build and run containers with command:
    ```sh
    $ make build_containers
    ```
4. Populate the database with command if you want to generate new data:
    ```sh
    $ make populate_db_in_container

5. Create superuser with command if you use docker-compose:
    ```sh
    $ make create_admin_in_container
    ```
## Setup locally
1. Clone the repository:
    ```sh
    $ git@github.com:Vlad0n20/webcase_test_task.git
    ```
2. Populate env.example and end.db.example files and rename it on .env  and .env.db
3. Create virtual environment with command:
    ```sh
    $ python3 -m venv .venv
    ```
4. Activate virtual environment with command:
    ```sh
    $ source .venv/bin/activate
    ```
5. Install requirements with command:
    ```sh
    $ pip install -r requirements.txt
    ```
6. Run project with command:
    ```sh
    $ /bin/bash start
    ```

7. Create superuser with command:
    ```sh
    $ python manage.py createsuperuser
    ```

Now you can use the application. 

By http://0.0.0.0:8000/swagger/ - there is a swagger documentation for app.
