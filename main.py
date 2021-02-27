from lib.dewa import cari
from lib.kusonime import *
from lib.search import *
from lib.nulis import *
from urllib.parse import *
from flask import *
from bs4 import BeautifulSoup as bs
from requests import get, post
import os, math, json, re, html_text, requests, base64

app = Flask(__name__)

@app.route('/spamcall', methods=['GET','POST'])
def spamcall():
    if request.args.get('no'):
        no = request.args.get('no')
        if str(no).startswith('8'):
            hasil = ''
            kyaa = post('https://id.jagreward.com/member/verify-mobile/%s' % no).json()
            print(kyaa['message'])
            if 'Anda akan menerima' in kyaa['message']:
                hasil += 'Berhasil mengirim spam call ke nomor : 62%s' % no
            else:
                hasil += 'Gagal mengirim spam call ke nomor : 62%s' % no
            return {
                'status': 200,
                'logs': hasil
            }
        else:
            return {
                'status': false,
                'pesan': 'Tolong masukkan nomor dengan awalan 8'
            }
    else:
        return {
            'status': false,
            'pesan': 'Masukkan parameter no' 
        }

@app.route('/spamsms', methods=['GET','POST'])
def spamming():
    if request.args.get('no'):
        if request.args.get('jum'):
            no = request.args.get('no')
            jum = int(request.args.get('jum'))
            if jum > 10: return {
                'status': 200,
                'pesan': 'Maksimal 10 ya boi'
            }
            url = 'https://www.lpoint.co.id/app/member/ESYMBRJOTPSEND.do'
            head = {'UserAgent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1853) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'}
            data = {'pn': '',
                'bird': '',
                'webMbrId': '',
                'webPwd': '',
                'maFemDvC': '',
                'cellNo': no,
                'otpNo': '',
                'seq': '',
                'otpChk': 'N',
                'count': ''
            }
            hasil = ''
            for i in range(jum):
                kyaa = post(url, headers=head, data=data).text
                if 'error' in kyaa:
                    hasil += 'Gagal\n'
                else:
                    hasil += 'Sukses\n'
            return {
                'status': 200,
                'logs': hasil
            }
        else:
            return {
                'status': false,
                'pesan': 'Masukkin parameter jum juga boi'
            }
    else:
        return {
            'status': false,
            'pesan': 'Masukkan parameter no'
        }

@app.route('/nulis', methods=['GET','POST'])
def noolees():
    if request.args.get('text'):
        try:
            nulis = tulis(unquote(request.args.get('text')))
            for i in nulis:
                i.save('tulisan.jpg')
            return {
                'status': 200,
                'result': imageToBase64('tulisan.jpg')
            }
        except:
            return {
                'status': false,
                'error': 'Failed writing dude:('
            }
    else:
        return {
            'status': false,
            'pesan': 'Masukkan parameter text'
        }

@app.route('/wiki', methods=['GET','POST'])
def wikipedia():
	if request.args.get('q'):
		try:
			kya = request.args.get('q')
			cih = f'https://id.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={kya}'
			heuh = get(cih).json()
			heuh_ = heuh['query']['pages']
			hueh = re.findall(r'(\d+)', str(heuh_))
			result = heuh_[hueh[0]]['extract']
			return {
				'status': 200,
				'result': result
			}
		except Exception as e:
			print(e)
			return {
				'status': false,
				'error': '[❗] Yang anda cari tidak bisa saya temukan di wikipedia!'
			}
	else:
		return {
			'status': false,
			'pesan': 'Masukkan param q'
		}

@app.route('/ytmp4', methods=['GET','POST'])
def ytv():
	if request.args.get('url'):
		try:
			url = request.args.get('url').replace('[','').replace(']','')
			match = re.search("(?:http(?:s|):\\/\\/|)(?:(?:www\\.|)youtube(?:\\-nocookie|)\\.com\\/(?:watch\\?.*(?:|\\&)v=|embed\\/|v\\/)|youtu\\.be\\/)([-_0-9A-Za-z]{11})", url)
			if match:
				url = 'https://youtu.be/' + match.group(1)
			ytv = post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':url,'q_auto':'0','ajax':'1'}).json()
			yaha = bs(ytv['result'], 'html.parser').findAll('td')
			filesize = yaha[len(yaha)-23].text
			id = re.findall('var k__id = "(.*?)"', ytv['result'])
			thumb = bs(ytv['result'], 'html.parser').find('img')['src']
			title = bs(ytv['result'], 'html.parser').find('b').text
			dl_link = bs(post('https://www.y2mate.com/mates/en60/convert',data={'type':url.split('/')[2],'_id':id[0],'v_id':url.split('/')[3],'ajax':'1','token':'','ftype':'mp4','fquality':'360p'}).json()['result'],'html.parser').find('a')['href']
			return {
				'status': 200,
				'title': title,
				'thumb': thumb,
				'result': dl_link,
				'resolution': '360p',
				'filesize': filesize,
				'ext': 'mp4'
			}
		except Exception as e:
			print('Error : %s ' % e)
			return {
				'status': false,
				'error': '[❗] Terjadi kesalahan, mungkin link yang anda kirim tidak valid!'
			}
	else:
		return {
			'status': false,
			'msg': 'Masukkan parameter url'
		}

@app.route('/ytmp3', methods=['GET','POST'])
def yta():
	if request.args.get('url'):
		try:
			url = request.args.get('url').replace('[','').replace(']','')
			match = re.search("(?:http(?:s|):\\/\\/|)(?:(?:www\\.|)youtube(?:\\-nocookie|)\\.com\\/(?:watch\\?.*(?:|\\&)v=|embed\\/|v\\/)|youtu\\.be\\/)([-_0-9A-Za-z]{11})", url)
			if match:
				url = 'https://youtu.be/' + match.group(1)
			yta = post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':url,'q_auto':'0','ajax':'1'}).json()
			yaha = bs(yta['result'], 'html.parser').findAll('td')
			filesize = yaha[len(yaha)-10].text
			id = re.findall('var k__id = "(.*?)"', yta['result'])
			thumb = bs(yta['result'], 'html.parser').find('img')['src']
			title = bs(yta['result'], 'html.parser').find('b').text
			dl_link = bs(post('https://www.y2mate.com/mates/en60/convert',data={'type':url.split('/')[2],'_id':id[0],'v_id':url.split('/')[3],'ajax':'1','token':'','ftype':'mp3','fquality':'128'}).json()['result'],'html.parser').find('a')['href']
			return {
				'status': 200,
				'title': title,
				'thumb': thumb,
				'filesize': filesize,
				'result': dl_link,
				'ext': 'mp3'
			}
		except Exception as e:
			print('Error : %s' % e)
			return {
				'status': false,
				'error': '[❗] Terjadi kesalahan mungkin link yang anda kirim tidak valid!'
			}
	else:
		return {
			'status': false,
			'pesan': 'Masukkan parameter url'
		}

@app.route('/chord', methods=['GET','POST'])
def chord():
	if request.args.get('lagu'):
		try:
			lagu = request.args.get('lagu').replace(' ','+')
			id = get('http://app.chordindonesia.com/?json=get_search_results&exclude=date,modified,attachments,comment_count,comment_status,thumbnail,thumbnail_images,author,excerpt,content,categories,tags,comments,custom_fields&search=%s' % lagu).json()['posts'][0]['id']
			chord = get('http://app.chordindonesia.com/?json=get_post&id=%s' % id).json()
			result = html_text.parse_html(chord['post']['content']).text_content()
			return {
				'status': 200,
				'result': result
			}
		except Exception as e:
			print(e)
			return {
				'status': false,
				'error': '[❗] Maaf chord yang anda cari tidak dapat saya temukan!'
			}
	else:
		return {
			'status': false,
			'pesan': 'Masukkan parameter q'
		}

@app.route('/dewabatch', methods=['GET','POST'])
def dewabatch():
	if request.args.get('q'):
		try:
			q = request.args.get('q')
			he=search_dewabatch(quote(q))
			dewabatch=cari(he)
			if he != '':
				return {
					'status': 200,
					'sinopsis': dewabatch['result'],
					'thumb': dewabatch['cover'],
					'result': dewabatch['info']
				}
		except Exception as e:
			print(e)
			return {
				'status': false,
				'error': 'Anime %s Tidak di temukan!' % unquote(q)
			}
	else:
		return {
			'status': false,
			'pesan': 'Masukkan parameter q'
		}

@app.route('/kusonime', methods=['GET','POST'])
def kusonime():
	if request.args.get('q'):
		try:
			q = request.args.get('q')
			he=search_kusonime(quote(q))
			kuso=scrap_kusonime(he)
			if he != '':
				return {
					'status': 200,
					'sinopsis': kuso['sinopsis'],
					'thumb': kuso['thumb'],
					'info': kuso['info'],
					'title': kuso['title'],
					'link_dl': kuso['link_dl']
				}
		except Exception as e:
			print(e)
			return {
				'status': false,
				'error': 'Anime %s Tidak di temukan' % unquote(q)
			}
	else:
		return {
			'status': false,
			'pesan': 'Masukkan parameter q'
		}

@app.route('/infogempa', methods=['GET','POST'])
def infogempa():
	be = bs(get('https://www.bmkg.go.id/').text, 'html.parser').find('div', class_="col-md-4 md-margin-bottom-10")
	em = be.findAll('li')
	img = be.find('a')['href']
	return {
		'status': 200,
		'map': img,
		'waktu': em[0].text,
		'magnitude': em[1].text,
		'kedalaman': em[2].text,
		'koordinat': em[3].text,
		'lokasi': em[4].text,
		'potensi': em[5].text
	}

@app.route('/pinterest', methods=['GET','POST'])
def pinterest():
	if request.args.get('q'):
		try:
			kya = request.args.get('q')
			cih = f'http://api.fdci.se/sosmed/rep.php?gambar={kya}'
			heuh = get(cih).json()
			result = heuh
			return {
				'status': 200,
				'result': result
			}
		except Exception as e:
			print(e)
			return {
				'status': 404,
				'error': '[❗] Yang anda cari tidak bisa saya temukan di wikipedia!'
			}
	else:
		return {
			'status': 400,
			'pesan': 'Masukkan param q'
		}

@app.route('/', methods=['GET','POST'])
def index():
	return redirect("https://shizukaa.xyz", code=302)

@app.errorhandler(404)
def error(e):
	return redirect("https://shizukaa.xyz", code=302)
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','3000')),debug=True)
