import click
import os
import json
import traceback
from urllib import parse
from datetime import datetime
from dateutil import tz


audio_map = {
	'm4a': 'audio/mp4',
	'ogg': 'audio/ogg',
	'oga': 'audio/ogg',
	'mp3': 'audio/mp3',
}

video_map = {
	'mp4': 'video/mp4',
	'webm': 'video/webm',
	'mov': 'video/mp4',
}


@click.group()
def cli():
	pass


def cerr(*messages):
	val = ''
	for message in messages:
		val = val + ' ' + str(message)
	click.echo(click.style(val, fg = 'bright_red'))


def csuccess(*messages):
	val = ''
	for message in messages:
		val = val + ' ' + str(message)
	click.echo(click.style(val, fg = 'green'))


def find_asset(assets: list, id: str):
	for asset in assets:
		if asset['identifier'] == id:
			return asset
	return None


def convert_diary(directory: str, diary_name: str, entries: list):
	for entry in entries:
		try:
			# obtain text
			content = entry['text']
			# process assets
			lines = content.split('\n')
			for i in range(len(lines)):
				line = lines[i]
				if str(line).startswith('![](dayone-moment:'):
					asset_src = str(line[18:-1])
					asset_src = asset_src.replace('/', '')
					# audio // Note: this can be done because `u`, `i`, `o` are not in HEX
					if asset_src.startswith('audio'):
						audio = find_asset(entry['audios'], asset_src[5:])
						lines[i] = \
						f'<audio controls="controls">\n' + \
						f'  <source type="{audio_map[audio["format"]]}" src="../audios/{audio["md5"]}.{audio["format"]}"></source>\n' + \
						f'  <p>Your browser does not support the audio element.</p>\n' + \
						f'  <a href="../audios/{audio["md5"]}.{audio["format"]}">You can get audio file here.</a>\n' + \
						f'</audio>'
					# video // Note: this can be done because `v`, `i`, `o` are not in HEX
					elif asset_src.startswith('video'):
						video = find_asset(entry['videos'], asset_src[5:])
						lines[i] = \
						f'<video controls="controls">\n' + \
						f'  <source type="{video_map[video["type"]]}" src="../videos/{video["md5"]}.{video["type"]}"></source>\n' + \
						f'  <p>Your browser does not support the video element.</p>\n' + \
						f'  <a href="../videos/{video["md5"]}.{video["type"]}">You can get video file here.</a>\n' + \
						f'</video>'
					# photo
					else:
						photo = find_asset(entry['photos'], asset_src)
						lines[i] = f"![](../photos/{photo['md5']}.{photo['type']})"
			content = '\n'.join(lines)
			# calculate date in local time zone
			from_zone = tz.gettz('UTC')
			to_zone = tz.gettz(entry['timeZone'])
			utc = datetime.strptime(entry['creationDate'], '%Y-%m-%dT%H:%M:%SZ')
			utc = utc.replace(tzinfo=from_zone)
			local_time = utc.astimezone(to_zone)

			# write contents
			markdown_dir = os.path.join(directory, './markdown/', f'{local_time.strftime("%Y%m%d %H-%M-%S")} - {diary_name}.md')
			with open(markdown_dir, 'w+', encoding='utf-8') as f:
				f.write(content)
			csuccess('Conversion Success:', markdown_dir)
		except Exception as e:
			cerr("Conversion Failed:", entry)
			cerr(repr(e))
			cerr(traceback.format_exc())
		


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def convert(directory):
	'''
	Convert dumped data to markdown files

	ARGUMENTS:

	* DIRECTORY: path of unzipped Day One data
	'''
	# create markdown dir
	markdown_dir = os.path.join(directory, './markdown')
	if not os.path.exists(markdown_dir):
		os.mkdir(markdown_dir)
	# get diary list
	file_list = os.listdir(directory)
	for file_name in file_list:
		if file_name.endswith('.json'):
			with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as f:
				content = f.read()
			convert_diary(directory, parse.unquote(file_name[:-5]), json.loads(content)['entries'])


if __name__ == '__main__':
	cli()
