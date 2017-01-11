# selenium-testsuites
## Requires:
Firefox 47.0.1+
python 2.7+

## Recommended:
virtualenv
pip

## Install
`git clone git@github.com:BCLibCoop/selenium-testsuites.git`
Setup virtualenv as needed.

### python packages via pip
`sudo pip install selenium`
`sudo pip install configparser`

### gecko
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v{x.xx.x}/geckodriver-v{x.xx.x}-linux64.tar.gz
tar -xvzf geckodriver-v{x.xx.x}-linux64.tar.gz
chmod +x geckodriver
sudo cp geckodriver /usr/local/bin/
```

## Testing
To run the suites, copy config.example.conf to config.conf, fill in with credentials from [private wiki](https://wiki.libraries.coop/doku.php?id=coopweb:automating-regression-testing:credentials) and simply run each script with `python script.py`. 

The output should be self explanatory (. for success, E for error).
