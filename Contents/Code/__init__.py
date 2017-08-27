NAME = 'ORORO.TV'
ICON = 'icon-default.png'
ART = 'art-default.jpg'

BASE_URL = 'https://ororo.tv'
CHANNELS_URL = '%s/en/channels' % (BASE_URL)
YT_URL = 'https://www.youtube.com/watch?v=%s'

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler('/video/ororotv', NAME, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	html = HTML.ElementFromURL(CHANNELS_URL)

	channels = html.xpath('//div[@class="channel"]')

	for channel in channels:

		url = channel.xpath('.//a/@href')[0]
		title = channel.xpath('.//span[@class="title"]/text()')[0]
		summary = channel.xpath('.//p[@class="desc"]/text()')[0]
		thumb = channel.xpath('.//img/@src')[0]

		oc.add(DirectoryObject(
			key = Callback(Channel, url=url, title=title),
			title = title,
			summary = summary,
			thumb = thumb
		))

	return oc

####################################################################################################
@route('/video/ororotv/channel')
def Channel(url, title):

	oc = ObjectContainer(title2=title)
	html = HTML.ElementFromURL('%s%s' % (BASE_URL, url))

	videos = html.xpath('//div[contains(@class, "js-episode-wrapper")]')[:50]

	for video in videos:

		yt_id = video.xpath('.//a/@href')[0].strip('#')
		title = video.xpath('.//div[@class="name"]/text()')[0]
		thumb = video.xpath('.//img/@src')[0]

		oc.add(VideoClipObject(
			url = YT_URL % (yt_id),
			title = title,
			thumb = thumb
		))

	return oc
