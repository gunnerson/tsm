from datetime import date


def level():
    choices = [
        ('N', 'None'),
        ('R', 'Read'),
        ('W', 'Write'),
        ('A', 'Admin'),
    ]
    return choices

def year_choices():
    choices = []
    for r in range(1980, date.today().year + 2):
        c = (r, r)
        choices.append(c)
    return choices


def mechanic_choices():
    choices = [
        ('VP', 'Vadim'),
    ]
    return choices


def truck_make_choices():
    choices = [
        ('FL', 'Freighliner'),
        ('IN', 'International'),
        ('KW', 'Kenworth'),
        ('PB', 'Peterbilt'),
        ('VL', 'Volvo'),
        ('WS', 'Western Star'),
    ]
    return choices


def trailer_make_choices():
    choices = [
        ('HY', 'Hyundai'),
        ('UT', 'Utility'),
        ('WB', 'Wabash'),
    ]
    return choices


def company_group_choices():
    choices = [
        ('OU', 'Ours'),
        ('LO', 'Logistics'),
        ('IN', 'Insurance'),
        ('VE', 'Vendors'),
        ('GN', 'General'),
    ]
    return choices


def engine_choices():
    choices = [
        ('CT', 'Caterpillar'),
        ('CM', 'Cummins'),
        ('DT', 'Detroit'),
        ('IN', 'International'),
        ('PC', 'Paccar'),
        ('VL', 'Volvo'),
    ]
    return choices


def status_choices():
    choices = [
        ('D', 'Delivery'),
        ('I', 'Idle'),
        ('S', 'Shop'),
        ('T', 'Term'),
    ]
    return choices


def driver_status_choices():
    choices = [
        ('A', 'Active'),
        ('T', 'Term'),
    ]
    return choices


def size_choices():
    choices = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    return choices


def us_states_choices():
    choices = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AS', 'American Samoa'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('GU', 'Guam'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('MP', 'Northern Mariana Islands'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('PR', 'Puerto Rico'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VI', 'Virgin Islands'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    ]
    return choices

