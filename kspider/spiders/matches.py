import scrapy
from datetime import datetime
from kspider.items import Match


class MatchSpider(scrapy.Spider):
    name = "matches"

    def start_requests(self):
        yield scrapy.Request('https://www.kicker.de/{}/spieltag/{}/{}'.format(self.league, self.season, self.start))

    def parse(self, response):

        for match in response.css('.kick__v100-gameList__gameRow'):
            matchURL = match.css(
                '.kick__v100-gameList__gameRow__stateCell a::attr(href)').get()
            if matchURL is not None:
                kickID = matchURL.split('/')[1]
                yield response.follow('/{}/spielinfo/'.format(kickID), callback=self.parseSpielinfo)

        if self.recursive:
            for a in response.css('.kick__pagination__cell-go-forward a'):
                yield response.follow(a, callback=self.parse)

    def parseSpielinfo(self, response):

        def extract_with_css(query):
            datapoint = response.css(query).get(default='').strip()
            if datapoint == "-":
                return ""
            return datapoint

        m = Match()

        stadion = response.css('.kick__gameinfo__item--game-preview '
                               ':nth-child(3) p::text').getall()
        if len(stadion) > 1:
            m['stadium'] = " ".join(stadion[1].strip().split())
        else:
            m['stadium'] = ''
        m['matchID'] = response.url.split('/')[-3]

        datestring = extract_with_css('.kick__gameinfo__item--game-preview '
                                      ':nth-child(2) p::text')
        date = datetime.strptime(datestring, '%d.%m.%Y, %H:%M')
        m['datetime'] = date
        m['league'] = self.league
        m['season'] = self.season
        m['matchday'] = extract_with_css('.kick__v100-scoreboardInfo a::text')
        m['homeTeam'] = extract_with_css(
            'div.kick__v100-gameCell__team__name:nth-child(1)::text')
        m['awayTeam'] = extract_with_css(
            'div.kick__v100-gameCell__team__name:nth-child(2)::text')
        m['homeGoals'] = extract_with_css(
            'div.kick__v100-scoreBoard div:nth-child(1) div:nth-child(1)::text')
        m['awayGoals'] = extract_with_css(
            'div.kick__v100-scoreBoard div:nth-child(1) div:nth-child(3)::text')
        m['referee'] = extract_with_css('.kick__gameinfo__person a::text')
        m['attendance'] = extract_with_css(
            '.kick__gameinfo__item--game-preview .kick__tabular-nums p::text')

        tl = response.css('.kick__game-timeline *::text').getall()
        for t in range(len(tl)):
            tl[t] = tl[t].strip()
        tl = list(filter(None, tl))
        m['timeline'] = tl

        yield m
