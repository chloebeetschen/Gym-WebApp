[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/BsFdJ6lI)
## The Best and Most High Tech **Sports Centre Management System** of All Time

### To Run
- Make sure you have flask installed
- Run build.sh with ./build.sh for normal mode
- Run build.sh with ./build.sh --clean for clean mode (remigrates the database)
- It should run on http://127.0.0.1:5002

### To view the database
- Go to http://127.0.0.1:5000/admin/

### To login as mananger
- Email: admin@admin.com
- Password: password

### To login as employee
- Email: employee1@gymcorp.com
- Password: password

### Important NB: Babel doesn't work out of the box on feng-linux, so you wil need to modify your flask_babel init file
- This can be done in the following path: /home/csunix/<YOUR_USERNAME_HERE>/flask/lib/python3.6/site-packages/flask_babel/__init__.py
- Within this init file, you have to add the following line to your imports: from flask_babel import Babel

[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-f4981d0f882b2a3f0472912d15f9806d57e124e0fc890972558857b51b24a6f9.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=10177624)
