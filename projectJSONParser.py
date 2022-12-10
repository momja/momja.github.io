import json
import datetime

# custom Decoder
def decodeDateTime(project):
    if 'start_date' in project:
        project["start_date"] = datetime.datetime.strptime(project["start_date"], '%m/%y')
    if 'end_date' in project:
        project["end_date"] = datetime.datetime.strptime(project["end_date"], '%m/%y')
    start_formatted_date = project["start_date"].strftime('%b %y') 
    end_formatted_date = project["end_date"].strftime('%b %y') 
    project["display_date"] = f'{start_formatted_date} — {end_formatted_date}'
    return project


def parse(file_name):
    with open(file_name, 'r') as f:
        project_data = json.load(f, object_hook=decodeDateTime)

    return sorted(project_data, key=lambda project: project['start_date'], reverse=True)
