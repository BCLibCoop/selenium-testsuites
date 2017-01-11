# selenium-testsuites
Requires:
Firefox 47.0.1+
Python 3.4+
selenium for Python > 2.53.5
Geckodriver

Recommended:
virtualenv, virtualenvwrapper

#Install
gecko
'wget https://github.com/mozilla/geckodriver/releases/download/v0.13.0/geckodriver-v0.13.0-linux64.tar.gz'
'tar -xvzf geckodriver-v0.13.0-linux64.tar.gz'
'chmod +x geckodriver'
'sudo cp geckodriver /usr/local/bin/'

#Testing
To run the suites, copy config.example.conf to config.conf, fill in with credentials from [private wiki](https://wiki.libraries.coop/doku.php?id=coopweb:automating-regression-testing:credentials) and simply run each script with `python script.py`. 

The output should be self explanatory (. for success, E for error).
