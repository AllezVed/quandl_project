# quandl_project




## Python and Environment Setup

The script requires python3 and anaconda to execute successfully. To install python3, anaconda can be used here https://www.anaconda.com

Clone the git repo using:

`git clone https://github.com/AllezVed/quandl_project.git`

Navigate to the repo directory (/quandl_project ) from terminal and create the conda environment from the environment.yml file using the following command

`conda env create -f environment.yml`

Activate the new environment:
`conda activate athanor_env on Linux/MacOS`
`activate athanor_env on Windows`

## MySQL Setup

1. This project uses MySQL Community Server v8.0. Download using https://dev.mysql.com/downloads/mysql/

2. Installation instructions for MacOS can be found https://dev.mysql.com/doc/refman/8.0/en/osx-installation-pkg.html
3. Installation instructions for Windows can be found https://dev.mysql.com/doc/refman/8.0/en/mysql-installer.html
4. Please note the password you entered during the installation for the `root` user.
5. Make sure to start the MySQL server using the following instructions for MacOS using https://dev.mysql.com/doc/refman/8.0/en/osx-installation-prefpane.html and for Windows using https://dev.mysql.com/doc/refman/8.0/en/windows-start-command-line.html


## Project running instructions
1. In `config.py`, set the value of  `db.username` to `root` and `db.password` to the password you entered while installing MySQL server 
2. To create the database and table schema run db_utils.py using `python db_utils.py` from the terminal in the project directory
3. To fetch the data and store the data in the database table run utils.py using `python utils.py` from the terminal in the project directory.
4. To test the functionality of the different functions you can call the analysis functions in the `if __name__ == __main__` block in `app.py` and then run the script using `python app.py`
5. The charting results are stored in `/images/<contract_name>.png`
6. Results for the non-charting functions are returned as dataframes and printed

