import faker
from django.test import TestCase
from faker import Faker

from falmer.studentgroups.models import MSLStudentGroup

fake = Faker()
fake.add_provider(faker.providers.company)
fake.add_provider(faker.providers.internet)

def msl_api_factory(slug = None):
    return {
        'id': fake.pyint(),
        'name': fake.company(),
        'link': f'/organisation/{slug or fake.slug()}/',
        'description': fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None),
        'category': 'Uncategorised',
        'logo_url': 'https://sussexstudent.com/asset/groupinglogoimage/default/67fc461a61a4482cae44fb89fd670903.jpg?thumbnail_width=440&thumbnail_height=360&resize_type=ResizeFitAll'
    }


class SyncCase(TestCase):
    def test_create_new(self):
        a = MSLStudentGroup.create_from_msl(msl_api_factory(slug='comedy-society'))
        self.assertTrue(isinstance(a, MSLStudentGroup))
        self.assertEqual(a.group.slug, 'comedy-society')

    def test_update_new(self):
        data = msl_api_factory()
        msl_g = MSLStudentGroup.create_from_msl(data)
        g = msl_g.group
        self.assertEqual(g.name, data['name'])

        new_data = msl_api_factory()
        new_data['id'] = data['id']
        msl_g.update_from_msl(new_data)
        self.assertEqual(g.name, new_data['name'])
