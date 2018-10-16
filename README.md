# TVseries-Updater

TVseries-Updater is a python web scraping script for updating you about release dates of next episode/season of your favorite TV Series.

## Installation

### Requirements
* Linux/Windows
* Python 3.3 and up
* MYSQL
#### Python Libraries
* Beautiful Soup  
`$ pip install beautifulsoup4`  

* Requests  
`$ pip install requests`

* MySQL Connector Python  
`$ pip install mysql-connector-python`

* SMTP Library  
`$ pip install smtplib`

### Installing
* Clone/Download this repository as zip file on your local machine.
* Extract the zip file in your working directory.
* In [emailinfo.txt](emailinfo.txt), enter space separated email id and password from which you want to recieve mail and save it.
* In [sqlinfo.txt](sqlinfo.txt), enter space separated username and password of your Mysql database and save it.
## Running
Open command prompt(for windows) or terminal(for linux) in the present directory, and run the [updater.py](updater.py) file.  
Example:  
`C:\Users\Vikas\Desktop>python updater.py`


## Authors

* **Vikas Chandak** - *Initial work* - [Vikas Chandak](https://github.com/vikaschandak)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
