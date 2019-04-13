from scrapy import cmdline

name = 'spot'
cmd = 'scrapy crawl {0} JOBDIR=remain/001'.format(name)
cmdline.execute(cmd.split())
