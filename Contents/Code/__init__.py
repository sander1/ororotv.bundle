import ssl, urllib2

NAME = 'ORORO.TV'
ICON = 'icon-default.png'
ART = 'art-default.jpg'

BASE_URL = 'https://ororo.tv'
CHANNELS_URL = '%s/en/channels' % (BASE_URL)
YT_URL = 'https://www.youtube.com/watch?v=%s'

RE_CHANNELS_JSON = Regex('"items":(\[.+?\])\};')

HTTP_HEADERS = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME

####################################################################################################
@handler('/video/ororotv', NAME, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	page = GetData(CHANNELS_URL)
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
	page = GetData('%s%s' % (BASE_URL, url))
	html = HTML.ElementFromString(page)

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

####################################################################################################
@route('/video/ororotv/getdata')
def GetData(url):

	# Quick and dirty workaround
	# Do not validate ssl certificate
	# http://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed-error
	req = urllib2.Request(url, headers=HTTP_HEADERS)
	ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	data = urllib2.urlopen(req, context=ssl_context).read()

	return data
