import click
import os
import json
import traceback
from urllib import parse
from datetime import datetime
from dateutil import tz


# audio map for html5
audio_map = {
	'm4a': 'audio/mp4',
	'ogg': 'audio/ogg',
	'oga': 'audio/ogg',
	'mp3': 'audio/mp3',
}

# video map for html5
video_map = {
	'mp4': 'video/mp4',
	'webm': 'video/webm',
	'mov': 'video/mp4',
}

# device map
device_map = {
	'iPad1,1': 'iPad',
	'iPad2,1': 'iPad 2',
	'iPad2,2': 'iPad 2',
	'iPad2,3': 'iPad 2',
	'iPad2,4': 'iPad 2',
	'iPad2,5': 'iPad mini',
	'iPad2,6': 'iPad mini',
	'iPad2,7': 'iPad mini',
	'iPad3,1': 'iPad (3rd generation)',
	'iPad3,2': 'iPad (3rd generation)',
	'iPad3,3': 'iPad (3rd generation)',
	'iPad3,4': 'iPad (4th generation)',
	'iPad3,5': 'iPad (4th generation)',
	'iPad3,6': 'iPad (4th generation)',
	'iPad4,1': 'iPad Air',
	'iPad4,2': 'iPad Air',
	'iPad4,3': 'iPad Air',
	'iPad4,4': 'iPad mini 2',
	'iPad4,5': 'iPad mini 2',
	'iPad4,6': 'iPad mini 2',
	'iPad4,7': 'iPad mini 3',
	'iPad4,8': 'iPad mini 3',
	'iPad4,9': 'iPad mini 3',
	'iPad5,1': 'iPad mini 4',
	'iPad5,2': 'iPad mini 4',
	'iPad5,3': 'iPad Air 2',
	'iPad5,4': 'iPad Air 2',
	'iPad6,3': 'iPad Pro (9.7-inch)',
	'iPad6,4': 'iPad Pro (9.7-inch)',
	'iPad6,7': 'iPad Pro (12.9-inch)',
	'iPad6,8': 'iPad Pro (12.9-inch)',
	'iPad6,11': 'iPad (5th generation)',
	'iPad6,12': 'iPad (5th generation)',
	'iPad7,1': 'iPad Pro (12.9-inch) (2nd generation)',
	'iPad7,2': 'iPad Pro (12.9-inch) (2nd generation)',
	'iPad7,3': 'iPad Pro (10.5-inch)',
	'iPad7,4': 'iPad Pro (10.5-inch)',
	'iPad7,5': 'iPad (6th generation)',
	'iPad7,6': 'iPad (6th generation)',
	'iPad7,11': 'iPad (7th generation)',
	'iPad7,12': 'iPad (7th generation)',
	'iPad8,1': 'iPad Pro (11-inch)',
	'iPad8,2': 'iPad Pro (11-inch)',
	'iPad8,3': 'iPad Pro (11-inch)',
	'iPad8,4': 'iPad Pro (11-inch)',
	'iPad8,5': 'iPad Pro (12.9-inch) (3rd generation)',
	'iPad8,6': 'iPad Pro (12.9-inch) (3rd generation)',
	'iPad8,7': 'iPad Pro (12.9-inch) (3rd generation)',
	'iPad8,8': 'iPad Pro (12.9-inch) (3rd generation)',
	'iPad8,9': 'iPad Pro (11-inch) (2nd generation)',
	'iPad8,10': 'iPad Pro (11-inch) (2nd generation)',
	'iPad8,11': 'iPad Pro (12.9-inch) (4th generation)',
	'iPad8,12': 'iPad Pro (12.9-inch) (4th generation)',
	'iPad11,1': 'iPad mini (5th generation)',
	'iPad11,2': 'iPad mini (5th generation)',
	'iPad11,3': 'iPad Air (3rd generation)',
	'iPad11,4': 'iPad Air (3rd generation)',
	'iPad11,6': 'iPad (8th generation)',
	'iPad11,7': 'iPad (8th generation)',
	'iPad12,1': 'iPad (9th generation)',
	'iPad12,2': 'iPad (9th generation)',
	'iPad13,1': 'iPad Air (4th generation)',
	'iPad13,2': 'iPad Air (4th generation)',
	'iPad13,4': 'iPad Pro (11-inch) (3rd generation)',
	'iPad13,5': 'iPad Pro (11-inch) (3rd generation)',
	'iPad13,6': 'iPad Pro (11-inch) (3rd generation)',
	'iPad13,7': 'iPad Pro (11-inch) (3rd generation)',
	'iPad13,8': 'iPad Pro (12.9-inch) (5th generation)',
	'iPad13,9': 'iPad Pro (12.9-inch) (5th generation)',
	'iPad13,10': 'iPad Pro (12.9-inch) (5th generation)',
	'iPad13,11': 'iPad Pro (12.9-inch) (5th generation)',
	'iPad14,1': 'iPad mini (6th generation)',
	'iPad14,2': 'iPad mini (6th generation)',
	'iPhone1,1': 'iPhone',
	'iPhone1,2': 'iPhone 3G',
	'iPhone2,1': 'iPhone 3GS',
	'iPhone3,1': 'iPhone 4',
	'iPhone3,2': 'iPhone 4',
	'iPhone3,3': 'iPhone 4',
	'iPhone4,1': 'iPhone 4S',
	'iPhone5,1': 'iPhone 5',
	'iPhone5,2': 'iPhone 5',
	'iPhone5,3': 'iPhone 5c',
	'iPhone5,4': 'iPhone 5c',
	'iPhone6,1': 'iPhone 5s',
	'iPhone6,2': 'iPhone 5s',
	'iPhone7,1': 'iPhone 6 Plus',
	'iPhone7,2': 'iPhone 6',
	'iPhone8,1': 'iPhone 6s',
	'iPhone8,2': 'iPhone 6s Plus',
	'iPhone8,4': 'iPhone SE (1st generation)',
	'iPhone9,1': 'iPhone 7',
	'iPhone9,2': 'iPhone 7 Plus',
	'iPhone9,3': 'iPhone 7',
	'iPhone9,4': 'iPhone 7 Plus',
	'iPhone10,1': 'iPhone 8',
	'iPhone10,2': 'iPhone 8 Plus',
	'iPhone10,3': 'iPhone X',
	'iPhone10,4': 'iPhone 8',
	'iPhone10,5': 'iPhone 8 Plus',
	'iPhone10,6': 'iPhone X',
	'iPhone11,2': 'iPhone XS',
	'iPhone11,4': 'iPhone XS Max',
	'iPhone11,6': 'iPhone XS Max',
	'iPhone11,8': 'iPhone XR',
	'iPhone12,1': 'iPhone 11',
	'iPhone12,3': 'iPhone 11 Pro',
	'iPhone12,5': 'iPhone 11 Pro Max',
	'iPhone12,8': 'iPhone SE (2nd generation)',
	'iPhone13,1': 'iPhone 12 mini',
	'iPhone13,2': 'iPhone 12',
	'iPhone13,3': 'iPhone 12 Pro',
	'iPhone13,4': 'iPhone 12 Pro Max',
	'iPhone14,2': 'iPhone 13 Pro',
	'iPhone14,3': 'iPhone 13 Pro Max',
	'iPhone14,4': 'iPhone 13 mini',
	'iPhone14,5': 'iPhone 13',
	'iPod1,1': 'iPod touch',
	'iPod2,1': 'iPod touch (2nd generation)',
	'iPod3,1': 'iPod touch (3rd generation)',
	'iPod4,1': 'iPod touch (4th generation)',
	'iPod5,1': 'iPod touch (5th generation)',
	'iPod7,1': 'iPod touch (6th generation)',
	'iPod9,1': 'iPod touch (7th generation)',
	'iMac21,1': 'iMac (24-inch, M1, 2021)',
	'iMac21,2': 'iMac (24-inch, M1, 2021)',
	'Macmini9,1': 'Mac mini (M1, 2020)',
	'MacBookAir10,1': 'MacBook Air (Late 2020)',
	'MacBookPro17,1': 'MacBook Pro (13-inch, M1, 2020)',
	'MacBookPro18,1': 'MacBook Pro (16-inch, 2021)',
	'MacBookPro18,2': 'MacBook Pro (16-inch, 2021)',	'MacBookPro18,3': 'MacBook Pro (14-inch, 2021)',
	'MacBookPro18,4': 'MacBook Pro (14-inch, 2021)',
}


def convert_time_to_local_time(entry, field):
	from_zone = tz.gettz('UTC')
	if 'timeZone' not in entry.keys():
		to_zone = tz.gettz('UTC')
	else:
		to_zone = tz.gettz(entry['timeZone'])
	utc = datetime.strptime(entry[field], '%Y-%m-%dT%H:%M:%SZ')
	utc = utc.replace(tzinfo=from_zone)
	local_time = utc.astimezone(to_zone)
	return local_time


def repr_device_model(entry):
	if entry['creationDeviceModel'] in device_map.keys():
		return device_map[entry['creationDeviceModel']]
	return entry['creationDeviceModel']


def repr_os(entry):
	os_name = 'Unkown OS'
	os_version = 'Unkown Version'
	if 'creationOSName' in entry.keys():
		os_name = entry['creationOSName']
	if 'creationOSVersion' in entry.keys():
		os_version = entry['creationOSVersion']
	return f'{os_name} {os_version}'


# meta rules
meta_rules = [
	{
		'type': 'key-value',
		'name': '📅 Create',
		'color': '#F03A17',
		'show': lambda entry : 'creationDate' in entry.keys(),
		'value': lambda entry : convert_time_to_local_time(entry, 'creationDate').strftime("%Y/%m/%d %H:%M:%S"),
	},
	{
		'type': 'key-value',
		'name': '📅 Modify',
		'color': '#F03A17',
		'show': lambda entry : 'modifiedDate' in entry.keys(),
		'value': lambda entry : convert_time_to_local_time(entry, 'modifiedDate').strftime("%Y/%m/%d %H:%M:%S"),
	},
	{
		'type': 'key-value',
		'name': '📱 Device Model',
		'color': '#0794BD',
		'show': lambda entry : 'creationDeviceModel' in entry.keys(),
		'value': lambda entry : repr_device_model(entry),
	},
	{
		'type': 'key-value',
		'name': '💿 OS',
		'color': '#FFC83D',
		'show': lambda entry : ('creationOSName' in entry.keys()) or ('creationOSVersion' in entry.keys()),
		'value': lambda entry : repr_os(entry),
	},
	{
		'type': 'key-value',
		'name': '🆔 Day One UUID',
		'color': '#886CE4',
		'show': lambda entry : 'uuid' in entry.keys(),
		'value': lambda entry : entry['uuid'],
	},
	{
		'type': 'key-value',
		'name': '🌐 Time Zone',
		'color': '#5BCFF0',
		'show': lambda entry : 'timeZone' in entry.keys(),
		'value': lambda entry : entry['timeZone'],
	},
	{
		'type': 'flag',
		'name': '⭐ Starred',
		'show': lambda entry : dict(entry).get('starred') == True
	},
	{
		'type': 'flag',
		'name': '⌛ All Day',
		'show': lambda entry : dict(entry).get('isAllDay') == True
	},
	{
		'type': 'flag',
		'name': '📌 Pinned',
		'show': lambda entry : dict(entry).get('isPinned') == True
	},
	{
		'type': 'key-value',
		'name': '⌨ Device',
		'color': '#F95F5A',
		'show': lambda entry : 'creationDevice' in entry.keys(),
		'value': lambda entry : entry['creationDevice'],
	},
	{
		'type': 'key-value',
		'name': '#️⃣ tag',
		'color': '#0078D7',
		'show': lambda entry : 'tags' in entry.keys(),
		'value': lambda entry : entry['tags']
	},
	{
		'type': 'key-value',
		'name': '⛳ Activity',
		'color': '#34D058',
		'show': lambda entry : 'activityName' in entry['userActivity'].keys() if 'userActivity' in entry.keys() else False,
		'value': lambda entry : entry['userActivity']['activityName']
	},
	{
		'type': 'key-value',
		'name': '🚶‍♂️ Walking',
		'color': '#BF8EF3',
		'show': lambda entry : 'stepCount' in entry['userActivity'].keys() if 'userActivity' in entry.keys() else False,
		'value': lambda entry : entry['userActivity']['stepCount']
	}
	# TODO
	# weather
	# location
]

# obtain css
root_dir = os.path.split(os.path.abspath(__file__))[0]
style_path = os.path.join(root_dir, 'style.css')
with open(style_path, 'r', encoding='utf-8') as f:
	css = f.read()
css = ''.join([line.strip() for line in css.splitlines()])

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
			# process lines
			lines = content.split('\n')
			for i in range(len(lines)):
				line = lines[i]
				# assets
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
				# fix line breaking problems with quotes
				elif str(line).strip().startswith('>'):
					lines[i] = line + '\n'
				# fix indention problems with code blocks
				elif str(line).strip() == '```':
					lines[i] = '```'
				# fix line breaking problems with titles
				elif str(line).startswith('#'):
					lines[i] = line + '\n'
			content = '\n'.join(lines)
			# add styles and meta to contents
			content += f'\n<style>{css}</style>\n'

			for rule in meta_rules:
				if not rule['show'](entry): continue
				if rule['type'] == 'key-value':
					key = rule['name']
					value = rule['value'](entry)
					if not isinstance(value, list):
						value = [value]
					for val in value:
						content += \
						f'<div class="github-badge" height="20px" style="background-color: {rule["color"]}">\n' + \
						f'  <span class="badge-subject">{key}</span><span class="badge-value">{val}</span>\n' + \
						f'</div> '
				elif rule['type'] == 'flag':
					key = rule['name']
					content += \
					f'<div class="github-badge" height="20px">\n' + \
					f'  <span class="badge-subject">{key}</span>\n' + \
					f'</div> '

			# calculate date in local time zone
			local_time = convert_time_to_local_time(entry, 'creationDate')
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
