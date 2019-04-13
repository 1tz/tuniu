#!/bin/bash
scrapy crawl -s LOG_FILE=spot.log spot
scrapy crawl -s LOG_FILE=review.log review
