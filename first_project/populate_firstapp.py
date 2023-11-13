import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')

import django
django.setup()

import random
from firstapp.models import AccessRecord,Webpage,Topic,User
from faker import Faker

fakegen = Faker()
topics = ['Search','Social','Marketplace','News','Games']
def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t
def populate(N=5):
    for entry in range(N):
        top = add_topic()
        fake_url=fakegen.url()
        fake_date=fakegen.date()
        fake_name=fakegen.company()
        webpg = Webpage.objects.get_or_create(topic=top, url = fake_url, name = fake_name)[0]
        acc_rec = AccessRecord.objects.get_or_create(name=webpg,date=fake_date)[0]
def populate_user(N=5):
    for user in range(N):
        fake_first=fakegen.unique.first_name()
        fake_last = fakegen.unique.last_name()
        fake_email = fakegen.unique.email()
        users = User.objects.get_or_create(first_name = fake_first, last_name = fake_last, email = fake_email)

if __name__ == "__main__" : 
    print("populate")
    populate_user(N=20)
    print("complete")