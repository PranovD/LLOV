""" This module does blah blah blah """

from mailchimp3 import MailChimp
import pprint

try:
    import keys
except IOError:
    print("Keys File not Found. Online Access")

# MAILCHIMP KEYS
MC_CLIENT = MailChimp(mc_api=keys.MAILCHIMP_API_KEY)


def get_volunteer_emails():
    """
    Description
    """

    member_list = MC_CLIENT.lists.members.all('796717863d', get_all=True)
    return pprint.pprint(member_list)


def add_volunteer_email():
    """
    Old /volunteer path
    """

    """
    tag_list = [{'id': 18321, 'name': 'Volunteer'}]
    if fostering == 'on':
        tag_list = [{'id': 18321, 'name': 'Volunteer'},
                   {'id': 18325, 'name': 'Foster'}]

    email = request.form.get('email')
    print (email)
    email = 'temp_email@wokcy.com'
    MC_client.lists.members.create('796717863d', {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': first_name,
            'LNAME': last_name,
        },
    })
    """

    return None


def add_foster_volunteer_email():
    """
    Old /foster path
    """

    """
    tag_list = [{'id': 18325, 'name': 'Foster'}]
    if fostering == 'on':
        tag_list = [{'id': 18321, 'name': 'Volunteer'},
                    {'id': 18325, 'name': 'Foster'}]

    email = request.form.get('email')
    print(email)
    email = 'test_account_from_website@gmail.com'
    MC_client.lists.members.create('796717863d', {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': first_name,
            'LNAME': last_name,
        },
    })
    """

    return None
