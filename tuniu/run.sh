#!/bin/bash
scrapy crawl spot -s JOBDIR=job_info/001
scrapy crawl review -s JOBDIR=job_info/002
