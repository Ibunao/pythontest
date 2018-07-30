class HtmlOutPuter(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, new_data):
        if new_data is None:
            return
        self.datas.append(new_data)

    def output_html(self):
        fout = open('output.md','w')

        print(len(self.datas)), 'records have been added!'
        for data in self.datas:
            fout.write(data['title'].encode('utf-8'))
            fout.write(data['url'])
        fout.close()
