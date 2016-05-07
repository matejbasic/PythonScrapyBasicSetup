# PythonScrapyBasicSetup
Basic setup with random user agents and proxy addresses for [Python Scrapy Framework](http://scrapy.org/).

####Setup
1. Install Scrapy Framework
  
  ```
  pip install Scrapy
  ```
  [Detailed installation guide](http://doc.scrapy.org/en/1.0/intro/install.html)
2. Install [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup)
  
  ```
  pip install beautifulsoup4
  ```
  [Detailed installation guide](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) 

####Usage
To see what it does just:
  ```
  python run.py
  ```
Project contains two middleware classes in ```middlewares.py```. ```ProxyMiddleware``` downloads IP proxy addresses and before every process request chooses one randomly. ```RandomUserAgentMiddleware``` is similar, downloads user agent strings and saves them into  ```'USER_AGENT_LIST'``` settings list. It also before every process request selects one randomly. Middlewares are activated in ```settings.py``` file.
This project also contains two spiders just for testin purposes, ```spiders/iptester.py``` and ```spiders/uatester.py```. You can run them individually:
```
scrapy crawl UAtester
scrapy crawl IPtester
```
```run.py``` file is a also good example how to include and run your spiders sequentially from one script.

If you have any question or problem, feel free to ask me via email.
