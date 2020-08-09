# "LEGO Store" Database Application
This project was completed on 07/25/2020 for Fundamentals of Database Systems. Personally, I am not satisfied with the final result; however, it achieved its purpose of demonstrating knowledge of the relevant technologies, and my team received full marks. This assignment is usually given during full semesters at UNT, but my team completed it during a summer semester, which prevented us (and everyone else in the class) from completing every specification. Since my work was rushed, I don't think this project is representative of the quality of my coding.
  
The official assignment description can be seen [here](Assignment%20Details/Project%20Summer%202020.pdf). I created two reports for this project, the first of which is can be seen [here](Assignment%20Details/Phase%201%20Report.pdf). The second is a ~200MB power point including audio and video demonstrations and explanations of the application, and can be downloaded from [here](https://drive.google.com/file/d/1ApWX_2DxjKVF4HquRZJX20SwsUQmpGuX/view?usp=sharing).

### Organization
This application uses a menu-driven interface. In general, upper-level menus (where the user selects an option to navigate through the menus) are in [menus/](menus/). Modules for user interactions that actually affect the database are contained in [menufunctions/](menufunctions/). The modules in [menufunctions/](menufunctions/) use functions defined in [sql.py](sql.py) for performing database operations. The database schema is contained in [legoStoreDB.sql](legoStoreDB.sql).

### Usage
1. Download all project files.
2. In a MySQL8 DBMS, run the SQL script `legoStoreDB.sql` to create the correct database and tables.
3. Optionally, populate the database with `ALL.SQL` found under `test_data/`. Note that currently not all application functions work properly without test data.
4. Optionally, set up a [venv](https://docs.python.org/3/library/venv.html).
5. Run `pip install -r requirements.txt`
6. Run `lego_cli.py`

Notes: 
This currently uses [Python 3.8](https://www.python.org/downloads/) and is **incompatible** with previous versions.

### MySQL
Download: https://dev.mysql.com/downloads/

Should automatically come with [python connector](https://dev.mysql.com/downloads/connector/python/).

