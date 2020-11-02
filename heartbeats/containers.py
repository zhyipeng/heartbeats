import abc
from typing import List


class SortedSetInterface(metaclass=abc.ABCMeta):

    def __init__(self, name: str) -> None:
        self.name = name
    
    @abc.abstractmethod
    def set(self, key: str, score: float) -> None:
        pass

    @abc.abstractmethod
    def get(self, key: str) -> float:
        pass

    @abc.abstractmethod
    def range_by_score(self, 
                       start: float, 
                       end: float, 
                       reversed: bool = False) -> List[str]:
        pass

    @abc.abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abc.abstractmethod
    def delete_by_score_range(self, start: float, end: float) -> None:
        pass


class SortedSet(SortedSetInterface):

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.__container = {}
    
    def __repr__(self) -> str:
        return str(self.__container)

    def set(self, key: str, score: float) -> None:
        self.__container[key] = score
    
    def get(self, key: str) -> float:
        return self.__container.get(key)
    
    def delete(self, key: str) -> None:
        self.__container.pop(key, None)
    
    def range_by_score(self, start: float, end: float, reversed: bool = False) -> List[str]:
        print(start, end, self.__container)
        ret = {}
        for k, score in self.__container.items():
            if start <= score <= end:
                ret[k] = score
        
        return [i[0] for i in 
                sorted(ret.items(), key=lambda x: x[1], reverse=reversed)]
    
    def delete_by_score_range(self, start: float, end: float) -> None:
        delete_keys = []
        for k, v in self.__container.items():
            if start <= v <= end:
                delete_keys.append(k)
        
        for k in delete_keys:
            del self.__container[k]


class RedisSortedSet(SortedSetInterface):

    def __init__(self, 
                 name: str,
                 host: str = 'localhost', 
                 port: int = 6379, 
                 db: int = 0, 
                 password: str = None) -> None:
        import redis

        super().__init__(name)

        self.__redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
        )

    def set(self, key: str, score: float) -> None:
        self.__redis_client.zadd(self.name, {key: score})

    def get(self, key: str) -> float:
        return self.__redis_client.zscore(self.name, key)
    
    def range_by_score(self, start: float, end: float, reversed: bool = False) -> List[str]:
        method = self.__redis_client.zrangebyscore
        if reversed:
            method = self.__redis_client.zrevrangebyscore

        return method(self.name, start, end)

    def delete(self, key: str) -> None:
        self.__redis_client.zrem(self.name, key)

    def delete_by_score_range(self, start: float, end: float) -> None:
        self.__redis_client.zremrangebyscore(self.name, start, end)
