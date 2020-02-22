import scrapy

from kspider.items import EventItem


class EventSpider(scrapy.Spider):
    name = "EventSpider"

    def start_requests(self):
        yield scrapy.Request('https://www.kicker.de/{}/spieltag/{}/{}'.format(self.league, self.season, self.start))

    def parse(self, response):

        for match in response.css('.kick__v100-gameList__gameRow'):
            matchURL = match.css(
                '.kick__v100-gameList__gameRow__stateCell a::attr(href)').get()
            if matchURL is not None:
                kickID = matchURL.split('/')[1]
                yield response.follow('/{}/schema/'.format(kickID), callback=self.parseSchema)

        if self.recursive:
            for a in response.css('.kick__pagination__cell-go-forward a'):
                yield response.follow(a, callback=self.parse)

    def parseSchema(self, response):

        def extract_with_css(query):
            datapoint = response.css(query).get(default='').strip()
            if datapoint == "-":
                return ""
            return datapoint

        goals = response.css('.::text').getall()
        for g in goals:
            g.strip()
        e = EventItem()
        e['eventType'] = goals
        e['matchID'] = response.url.split('/')[-3]

        yield e
