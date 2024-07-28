class Diary:
    last_id = 0

    def __init__(self, memo, tags=' '):
        self.memo = memo
        self.tags = tags
        Diary.last_id += 1
        self.id = Diary.last_id

    def match(self, filter_text):
        return filter_text in self.memo or filter_text in self.tags

    def to_dict(self):
        return {
            'id': self.id,
            'memo': self.memo,
            'tags': self.tags
        }

class DiaryBook:
    def __init__(self):
        self.diaries = []

    def new_diary(self, memo, tags=' '):
        diary = Diary(memo, tags)
        self.diaries.append(diary)
        return diary

    def search_diary(self, filter_text):
        return [diary for diary in self.diaries if diary.match(filter_text)]
