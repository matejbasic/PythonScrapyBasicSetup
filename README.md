# PythonScrapyBasicSetup
Basic setup with random user agents and proxy addresses for [Python Scrapy Framework](http://scrapy.org/).

####Setup
1. Install Scrapy Framework

  ```
  pip install Scrapy
  ```
  [Detailed installation guide](https://doc.scrapy.org/en/1.3/intro/install.html)
2. Install [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup)

  ```
  pip install beautifulsoup4
  ```
  [Detailed installation guide](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

If you get some errors regarding the pyOpenSSL (check this [issue](https://github.com/scrapy/scrapy/issues/2473)), try to downgrade the Twisted engine:
  ```
  pip install Twisted==16.4.1
  ```

####Usage
To see what it does just:
  ```
  python run.py
  ```
Project contains two middleware classes in ```middlewares``` directory. ```ProxyMiddleware``` downloads IP proxy addresses and before every process request chooses one randomly. ```RandomUserAgentMiddleware``` is similar, downloads user agent strings and saves them into  ```'USER_AGENT_LIST'``` settings list. It also selects one UA randomly before every process request. Middlewares are activated in ```settings.py``` file.
This project also contains two spiders just for testing purposes, ```spiders/iptester.py``` and ```spiders/uatester.py```. You can run them individually:
```
scrapy crawl UAtester
scrapy crawl IPtester
```
```run.py``` file is a also good example how to include and run your spiders sequentially from one script.

If you have any questions or problems, feel free to create a new issue!
