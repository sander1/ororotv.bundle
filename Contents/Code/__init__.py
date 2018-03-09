NAME = 'ORORO.TV'
ICON = 'icon-default.png'
ART = 'art-default.jpg'

BASE_URL = 'https://ororo.tv'
CHANNELS_URL = '%s/en/channels' % (BASE_URL)
YT_URL = 'https://www.youtube.com/watch?v=%s'

RE_CHANNELS_JSON = Regex('"items":(\[.+?\])\};')

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

####################################################################################################
@handler('/video/ororotv', NAME, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	page = HTTP.Request(CHANNELS_URL).content
	json = RE_CHANNELS_JSON.search(page).group(1)
	json_obj = JSON.ObjectFromString(json)

	for channel in json_obj:

		oc.add(DirectoryObject(
			key = Callback(Channel, url=channel['url'], title=channel['title']),
			title = channel['title'],
			summary = channel['description'],
			thumb = channel['image'].replace('/thumb_', '/')
		))

	return oc

####################################################################################################
@route('/video/ororotv/channel')
def Channel(url, title):

	oc = ObjectContainer(title2=title)
	html = HTML.ElementFromURL('%s%s' % (BASE_URL, url))

	videos = html.xpath('//a[@class="js-episode"]')

	for video in videos:

		yt_id = video.xpath('./@href')[0].strip('#')
		title = video.xpath('./img/@alt')[0]
		thumb = video.xpath('./img/@data-original')[0]

		oc.add(VideoClipObject(
			url = YT_URL % (yt_id),
			title = title,
			thumb = thumb
		))

	return oc
