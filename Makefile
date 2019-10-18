all: spider

spider:
	python3 spiders.py

depends:
	pip3 install scrapy sqlalchemy pandas requests

