import time, logging, datetime


class WebCrawler():

    def __init__(self,driver,options):
        self.driver = driver
        self.ntrial = options['NTRIAL']
        self.buffer = options['BUFFER']
        self.jit = options['BUFFER_JIT']
        self.crawlpath = []

    def Main(self):
        while True:
            time.sleep(self.buffer + self.jit)
            self.timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            print(self.timestamp)
            self.Crawl()

    def Crawl(self):

        for interaction in self.crawlpath:
            trial = self.InteractWPage(interaction)
            if trial >= self.ntrial:
                break

    def InteractWPage(self,func):
        logging.info(f"[{self.timestamp}] interacting with {func.__name__}")
        isloaded = False
        trial = 0            
        while trial < self.ntrial and not isloaded:
            trial+=1
            time.sleep(self.buffer + self.jit)      
            try:
                isloaded = func()
            except Exception as e:
                logging.info(e)
                continue
        return trial
