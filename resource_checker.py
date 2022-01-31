import json
import click
import os
import hashlib


def calculate_md5(file_dir):
	with open(file_dir, 'rb') as f:
		m = hashlib.md5()
		m.update(f.read())
		return m.hexdigest()


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


def asset_check(directory, type: str, format_str: str):
	# get diary list
	file_list = os.listdir(directory)
	diary_list = []
	for file_name in file_list:
		if file_name.endswith('.json'):
			diary_list.append(os.path.join(directory, file_name))
	
	# read all images md5 in diary
	image_md5s = []
	for diary_dir in diary_list:
		with open(diary_dir, 'r', encoding='utf-8') as f:
			contents = f.read()
		contents_dict = json.loads(contents)
		entries = contents_dict['entries']
		for entry in entries:
			if f'{type}s' not in entry.keys(): continue
			assets = entry[f'{type}s']
			for asset in assets:
				image_md5s.append(f"{asset['md5']}.{asset[format_str]}")
	
	# read all image md5 in asset folder
	asset_path = os.path.join(directory, f'./{type}s')
	asset_files = os.listdir(asset_path)
	
	# check whether assets exist
	click.echo(click.style(f"============ {type} Existence Check ============", bg='blue', fg='white'))
	for md5 in image_md5s:
		if md5 not in asset_files:
			print('Image file not found:', md5)

	# check whether md5 hash are correct
	click.echo(click.style(f"============ {type} MD5 Check ============", bg='blue', fg='white'))
	asset_files = [os.path.join(asset_path, asset_file) for asset_file in os.listdir(asset_path)]
	for asset_file in asset_files:
		if calculate_md5(asset_file) != os.path.basename(asset_file).split('.')[0]:
			cerr("MD5 does not match:", asset_file, "=>", calculate_md5(asset_file))
		else:
			csuccess("Match:", asset_file)


@click.group()
def cli():
	pass


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def check(directory):
	'''
	Check data integrity. Only photos, audios, and videos are supported.

	ARGUMENTS:

	* DIRECTORY: path of unzipped Day One data
	'''
	asset_check(directory, 'photo', 'type')
	asset_check(directory, 'audio', 'format')
	asset_check(directory, 'video', 'type')


if __name__ == '__main__':
	cli()
