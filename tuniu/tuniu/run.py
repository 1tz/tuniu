from scrapy import cmdline

name = 'tn'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
