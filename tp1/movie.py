import json


class Time():
    def __init__(self, t, room, subtitled):
        self.time = t
        self.room = room
        self.subtitled = subtitled


class Movie():
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.genre = ''
        self.language = ''
        self.duration = 0
        self.director = ''
        self.cast = []
        self.synopsis = ''
        self.times = []

    def add_time(self, time, room, subtitled):
        self.times.append(Time(time, room, subtitled))

    def to_dict(obj):
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
