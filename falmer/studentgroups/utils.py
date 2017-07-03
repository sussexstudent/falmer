import requests
from bs4 import BeautifulSoup
from .models import MSLStudentGroup

def get_msl_groups_page():
    req = requests.get('https://www.sussexstudent.com/sportsoc-next')

    if req.status_code == 200:
        return req.text

    return None


def parse_group(el):
    anchor = el.find('a')
    description = el.find(class_='msl-gl-description')

    data = {
        'id': int(el.attrs['data-msl-grouping-id']),
        'name': anchor.text,
        'link': anchor.attrs['href'],
        'description': description.text.strip() if description is not None else '',
        'category': 'Uncategorised',
    }

    previous = el.find_previous_sibling('li')
    if previous is not None and 'class' in previous.attrs and 'msl-gl-logo' in previous.attrs['class']:
        img = el.find_previous_sibling('li').find('img')
        data['logo_url'] = 'https://sussexstudent.com{}'.format(img.attrs['src'].replace('..', '').split('?')[0])

    return data


def get_msl_groups():
    html = get_msl_groups_page()

    if html is None:
        return []

    doc = BeautifulSoup(html)

    widget = doc.find(class_='msl_organisation_list')

    return [parse_group(el) for el in widget.find_all('li') if 'class' not in el.attrs or 'msl-gl-logo' not in el.attrs['class']]


def sync_groups_from_msl():
    msl_groups = get_msl_groups()
    msl_groups_map = {item['id']:item for item in msl_groups}
    msl_groups_ids = set(msl_groups_map)
    group_matches = {group.msl_group_id: group for group in MSLStudentGroup.objects.filter(msl_group_id__in=msl_groups_ids)}

    for msl_group_id in msl_groups_ids:
        if msl_group_id in group_matches:
            group_matches[msl_group_id].update_from_msl(msl_groups_map[msl_group_id])
        else:
            MSLStudentGroup.create_from_msl(msl_groups_map[msl_group_id])
