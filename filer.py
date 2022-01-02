import json

class LinkFile:
    @classmethod
    def save_links(cls, id: str, title: str, content: list, file):
        current_list = cls.read_links(file)
        current_list[id] = [title, []]
        for item in content:
            current_list[id][1].append(item)

        with open(file, 'w') as json_file:
            json_file.write(json.dumps(current_list))


    @classmethod
    def read_links(cls, file):
        with open(file, 'r') as json_file:
            content = json.loads(json_file.read())
            return content




