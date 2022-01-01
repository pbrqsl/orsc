import json

class LinkFile:
    @classmethod
    def save_links(cls, title: str, content: list, file):
        json_dict = {'links': [],
                     'title': title}
        for item in content:
            json_dict['links'].append(item)
        with open(file, 'w') as json_file:
            json_file.write(json.dumps(json_dict))

    @classmethod
    def read_links(cls, file):
        with open(file, 'r') as json_file:
            content = json.loads(json_file.read())
            return content




