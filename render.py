# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import os, imp
from glob import glob

DOMAIN = 'xkcd.omniavinco.kr'
BASE_URL = 'http://%s' % DOMAIN
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
  dict = imp.load_source('', filename).__dict__
  dict['id'] = os.path.basename(dict['__file__']).rsplit('.', 1)[0].split('.', 1)[0]
  
  if 'metas' not in dict:
    dict['metas'] = {}

  dict['metas']['twitter:domain'] = DOMAIN
  dict['metas']['twitter:title'] = dict['title']
  dict['metas']['twitter:creator'] = dict['creator']

  if dict['type'] == "image":
    dict['metas']['twitter:card'] = 'photo'
    dict['metas']['twitter:image:src'] = url_for('res', filename=dict['source'])

  return dict

def make_redirect_page(source, target):
  pass

def render_content(template, data):
  out_filename = os.path.basename(data['__file__']).rsplit('.', 1)[0] + '.html'
  out_path = os.path.join(OUT_PATH, out_filename)
  template.stream(data).dump(out_path, encoding='utf-8')
  
def render_random(file_list):
  out_pat = os.path.join(OUT_PATH, 'random.js')

def url_for(namespace, **kwargs):
  url_set = {
    'res': '%s/res/{filename}' % BASE_URL,
    'content': '%s/{target}.html' % BASE_URL
    }
  return url_set[namespace].format(**kwargs)

env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
env.globals['url_for'] = url_for
file_list = get_file_list()
prev_file = None
file_name = file_list[0]

def get_target_name(file_name):
  if file_name:
    return os.path.basename(file_name).rsplit('.', 1)[0]
  return file_name

for file_index in range(len(file_list)):
  next_file = file_list[file_index + 1] if len(file_list) > file_index + 1 else None
  info = parse_info_file(file_name)
  info['prev'] = get_target_name(prev_file)
  info['next'] = get_target_name(next_file)
  render_content(env.get_template('view.html'), info)
  prev_file = file_name
  file_name = next_file
