# This branch will handle setting up the payment portal and database
### Initialise the Database
- Before running the application, activate the virtual environment and navigate to project directory
- In the terminal type 'flask db init'
- Then 'flask db migrate -m "Initial migration"
- Then 'flask db upgrade'
- This will initialise the database and you can then run the program

### To Run
- Make sure you have flask installed
- Run the bash script build.sh with ./build.sh
- It should run on http://127.0.0.1:5000
- Add the route /paymentForm

### To view the database
- Go to http://127.0.0.1:5000/admin/

[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-f4981d0f882b2a3f0472912d15f9806d57e124e0fc890972558857b51b24a6f9.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=10177624)
