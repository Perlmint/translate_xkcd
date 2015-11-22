# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import os, imp
from glob import glob
from copy import deepcopy

DOMAIN = 'xkcd.omniavinco.kr'
BASE_URL = 'http://%s' % DOMAIN
SITE_OWNER = "@omniavinco"
WORK_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(WORK_ROOT, 'templates')
RES_PATH = os.path.join(WORK_ROOT, 'res')
SRC_PATH = os.path.join(WORK_ROOT, 'src')
OUT_PATH = os.path.join(WORK_ROOT, 'out')

try:
  os.mkdir(OUT_PATH)
except OSError as e:
  pass

def get_file_list():
  file_list = glob(os.path.join(SRC_PATH, '*.*.py'))
  def get_id(filename):
    return int(os.path.basename(filename).split('.', 1)[0])
  file_list.sort(key=get_id)
  return file_list

def parse_info_file(filename):
  info_dict = {k: v for k, v in imp.load_source('', filename).__dict__.items() if not k.startswith('__') or k == '__file__'}
  info_dict['id'] = os.path.basename(info_dict['__file__']).rsplit('.', 1)[0].split('.', 1)[0]

  if 'metas' not in info_dict:
    info_dict['metas'] = {}

  info_dict['metas']['twitter:domain'] = DOMAIN
  info_dict['metas']['twitter:title'] = info_dict['title']
  info_dict['metas']['twitter:creator'] = info_dict['creator']
  info_dict['metas']['twitter:site'] = SITE_OWNER

  if info_dict['type'] == "image":
    info_dict['metas']['twitter:card'] = 'photo'
    info_dict['metas']['twitter:image:src'] = url_for('res', filename=info_dict['source'])

  return info_dict

def url_for(namespace, **kwargs):
  url_set = {
    'res': '%s/res/{filename}' % BASE_URL,
    'content': '%s/{target}.html' % BASE_URL,
    'source': 'https://github.com/perlmint/translate_xkcd'
    }
  return url_set[namespace].format(**kwargs)

def make_redirect_page(source, target):
  out_dir = os.path.join(OUT_PATH, source)
  out_path = os.path.join(out_dir, 'index.html')
  if not os.path.isdir(out_dir):
    os.makedirs(out_dir)
  env.get_template('redirect.html').stream({ 'url': url_for('content', target=target) }).dump(out_path, encoding='utf-8')

def render_content(template, data):
  out_filename = os.path.basename(data['__file__']).rsplit('.', 1)[0] + '.html'
  out_path = os.path.join(OUT_PATH, out_filename)
  template.stream(data).dump(out_path, encoding='utf-8')

def render_random(file_list):
  out_path = os.path.join(OUT_PATH, 'random.js')
  with open(out_path, 'w') as o:
    o.write('var list = [')
    o.write(','.join([ '"%s"' % info['id'] for info in file_list ]))
    o.write('];')

    o.write('var getRandomID = function() {')
    o.write('return list[Math.floor(Math.random() * list.length)];')
    o.write('};')

    o.write('var gotoRandomPage = function() {')
    o.write('location.href = "./" + getRandomID() + "/index.html";')
    o.write('};')

def render_index(file_list):
  out_path = os.path.join(OUT_PATH, 'index.html')
  env.get_template('index.html').stream({ 'list': file_list }).dump(out_path, encoding='utf-8')

env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
env.globals['url_for'] = url_for
file_list = get_file_list()
prev_file = None
file_name = file_list[0]

def get_target_name(file_name):
  if file_name:
    return os.path.basename(file_name).rsplit('.', 1)[0]
  return file_name

file_infos = []
for file_index in range(len(file_list)):
  next_file = file_list[file_index + 1] if len(file_list) > file_index + 1 else None
  info = parse_info_file(file_name)
  info['prev'] = get_target_name(prev_file)
  info['cur'] = get_target_name(file_name)
  info['next'] = get_target_name(next_file)
  file_infos.append(deepcopy(info))
  prev_file = file_name
  file_name = next_file

for info in file_infos:
  render_content(env.get_template('view.html'), info)
  make_redirect_page(info['id'], info['cur'])

render_index(file_infos)
render_random(file_infos)
