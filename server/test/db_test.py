# import unittest
# from models import Link

# class TestCalculator(unittest.TestCase):
#     def set_data(self):
#         Link

""" datetime.datetime.now().time().isoformat()
    datetime.date.today().isoformat()"""
import redis
import json
import threading
import time
import datetime
import tldextract
from collections.abc import Set, Hashable
from typing import NamedTuple
import functools

r = redis.StrictRedis(
                host='localhost',
                port=6379,
                db=0,
                password=None,
                socket_timeout=None,
                charset="utf-8",
                decode_responses=True
        )

hats_1 = { "2020-05-14": {
    "09:17:31.173473": "https://stackoverflow.com",
    "10:57:10.140373": "https://git.some_one.agency/",
    "12:37:01.186473": "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
    "14:00:51.156374": "https://dashboard.heroku.com/apps",
    "20:47:41.124473": "https://www.digitalocean.com/",
    }
    
}

hats_2 = {"2020-05-15": {
    "07:10:01.186473": "https://ya.ru",
    "09:37:05.186573": "https://ya.ru?q=123",
    "16:30:01.186473": "funbox.ru",
    "19:30:00.186473": "https://stackoverflow.com/questions/11828270",
    }
}

hats_3 = {"2020-05-16": {
    "11:27:02.186473": "https://ya.ru/some_one",
    "15:17:03.123412": "https://ya.ru?q=123",
    "18:07:08.141253": "https://vk.com",
    }
}


def save():
    with r.pipeline() as pipe:
        for day in (hats_1, hats_2, hats_3):
            for d_date, item in day.items():
                for d_time, url in item.items():
                    t_stamp = str(int(time.mktime(datetime.datetime.strptime(f'{d_date} {d_time}', "%Y-%m-%d %H:%M:%S.%f").timetuple())))
                    print(f'date:{d_date} :{d_time} , stamp:{t_stamp}, url:{url}')  
                    data = [t_stamp, '{"url":"'+f'{url}"'+'}']
                    pipe.execute_command('ZADD', "links", *data)
        pipe.execute()
    r.bgsave()

def timestamp():
    return int(datetime.datetime.now().timestamp())

def connection_db():
    return redis.StrictRedis(
                host='localhost',
                port=6379,
                db=0,
                password=None,
                socket_timeout=None,
                charset="utf-8",
                decode_responses=True
            )


class SortedSet:
    
    ZADD = "ZADD"
    SCORE = "WITHSCORES"
    ZINCRBY = "ZINCRBY"
    ZRANGE = "ZRANGE"
    ZREVRANGE = "ZREVRANGE"
    ZRANGEBYSCORE = "ZREVRANGEBYSCORE"
    ZREVRANGEBYSCORE = "ZREVRANGEBYSCORE"

    def __init__(self, model, score='', *args, **kwargs):
        self.model = model
        self.score = score
        self.min = None
        self.max = None
        self.timestamp = None
        self.query_type = None
        self.args = args
        self.kwargs = kwargs
    
    def zget(self, revers=False):
        method = self.ZREVRANGEBYSCORE if bool(revers) else self.ZRANGEBYSCORE
        out = [method, self.model, self.min, self.max]
        out.append(self.SCORE if bool(self.score) else '')
        return out
    
    def zset(self, *args, **kwargs):
        return [self.ZADD, self.model, self.timestamp, '"{}"'.format(str(kwargs))]
    
    def zupdate(self, *args, **kwargs):
        return [self.ZINCRBY, self.model, self.timestamp, '"{}"'.format(str(kwargs))]
    
    def zall(self, *args, **kwargs):
        method = self.ZREVRANGE if bool(revers) else self.ZRANGE
        out = [method, self.model, self.min, self.max]
        out.append(self.SCORE if bool(self.score) else '')
        return out
    
    VALUES = {
        "get": zget,
        "set": zset,
        "update": zupdate,
        "all": zall
    }

    def query_construct(self, *args, **kwargs):
        return self.VALUES[self.query_type](self, *args, **kwargs)

class QuerySet(Set, Hashable):
    """ Кверисэт запроса """
    
    ___hash__ = Set._hash

    wrapped_methods = ('difference',
                       'intersection',
                       'symetric_difference',
                       'union',
                       'copy')

    def __repr__(self):
        return "QuerySet({0})".format(self._set)

    def __new__(cls, iterable):
        selfobj = super(QuerySet, cls).__new__(QuerySet)
        selfobj._set = iterable
        for method_name in cls.wrapped_methods:
            setattr(selfobj, method_name, cls._wrap_method(method_name, selfobj))
        return selfobj

    @classmethod
    def _wrap_method(cls, method_name, obj):
        def method(*args, **kwargs):
            result = getattr(obj._set, method_name)(*args, **kwargs)
            return QuerySet(result)
        return method

    def __getattr__(self, attr):
        return getattr(Link, attr)
            
    def __contains__(self, item):
        return item in self._set

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter(self._set)

class BaseModel:
    
    mapping = {}
    
    def __init__(self, *args, **kwargs):
        self.model = None
        self.conn = connection_db()
        self.args = args
        self.kwargs = kwargs
    
    def serializer(self, fields_data):
        try:
            json.loads(*fields_data)
        except TypeError:
            if bool(self.score):
                data = json.loads(fields_data[0])
                data['score'] = fields_data[1] 
                return data
            raise TypeError
    
    def exec(self, query):
        with self.conn.pipeline() as pipe:
            print(query)
            pipe.execute_command(*query)
            return pipe.execute()
    
    def set_items(self, instance, data):
        for k, v in data.items():
            self.mapping[k] = v
            setattr(instance, k, v) 
    
    def __repr__(self):
        return "{}Object({})".format(type(self).__name__, self.mapping)

class ModelManager(BaseModel):

    def __init__(self, model,
        score=False,
        timestamp=datetime.datetime.now().timestamp,
        filed_type=None,
        *args,
        **kwargs
        ):
        super(ModelManager, self).__init__(*args, **kwargs)
        self.model = model
        self.score = score
        self.timestamp = timestamp
        self.type = filed_type(model=model, score=score,)
        self.args = args
        self.kwargs = kwargs
    
    def get(self, timestamp, *args, **kwargs):
        self.type.query_type, self.type.min, self.type.max = 'get', timestamp, timestamp
        return Model(
                self.serializer(*self.exec(
                    self.type.query_construct(*args, **kwargs))
                    )
                )
    
    def filter(self, time_min=False, time_max=False, *args, **kwargs):
        self.type.query_type = 'get'
        self.type.min = time_min 
        self.type.max = time_max if bool(time_max) else time_min
        return QuerySet(Model(
                self.serializer(*self.exec(
                    self.type.query_construct(*args, **kwargs))
                    )
                )
            )
    
    def set(self, *args, **kwargs):
        self.type.query_type = 'set'
        self.type.timestamp = int(self.timestamp())      
        self.exec(
            self.type.query_construct(*args, **kwargs)
            )
        self.conn.bgsave()
        return Model(kwargs), True

        
    def update(self, timestamp=False, *args, **kwargs):
        self.type.query_type = 'update'
        self.type.timestamp = imestamp if bool(timestamp) else self.timestamp()    
        self.exec(
            self.type.query_construct(*args, **kwargs)
            )
        self.conn.bgsave()
        return Model(kwargs), True

    def delete(self, key):
        pass

class Model(BaseModel):
    """ Абстрактная модель данных
    используем sorted set redis.
    """
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def __new__(cls, data=False, *args, **kwargs):
        instance = super(Model, cls).__new__(cls, *args, **kwargs)
        if bool(data):
            cls.set_items(cls, instance, data)
        return instance

class Link(Model):

    objects = ModelManager(
            model='links',
            score=True,
            timestamp=datetime.datetime.now().timestamp,
            filed_type=SortedSet,
        )


link = Link.objects.get(1589437051)
# links = Link.objects.filter(1589437051)
print(link)
# link.objects.update(url=)
# print(link)

# links_1 = Link.objects.set(url='https://some_one_url?/account/12312412/album/17')
# print(links_1)

