import json

def fulltitle(title):
    return 'Title', title

def duration(seconds):
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return 'Length', '{:02}:{:02}:{:02}'.format(h,m,s)

def view_count(count):
    views = int(count)
    return 'Views', "{:,}".format(views)

def thumbnail(url):
    return 'Thumbnail', url

def description(desc):
    return 'Description', desc

def upload_date(datestr):
    return 'Upload date', datestr[0:4]+'-'+datestr[4:6]+'-'+datestr[6:]

def uploader_id(uid):
    return 'Uploader', uid

def json_to_comment(filepath):
    with open(filepath) as f:
        infos = json.load(f)
        
    keys = ['fulltitle', 'duration', 'view_count', 'thumbnail',
                'upload_date', 'uploader_id']
    funcs = map(eval, keys)

    lines = ['Attribute|Info', ':---|:---']

    for func, key in zip(funcs, keys):
        if key in infos:
            line = u'**{}**|{}'.format( *(func(infos[key])) )
            lines.append(line)
    
    return '\n'.join(lines)

if __name__ == '__main__':
    print json_to_comment("sample.info.json")
