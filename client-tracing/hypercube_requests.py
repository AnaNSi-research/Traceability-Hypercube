import requests

INSERT = '/insert'
REMOVE = '/remove'
PIN_SEARCH = '/pin_search'
SUPERSET_SEARCH = '/superset_search'

class HypercubeRequests:
    def __init__(self, hypercube_addr) -> None:
        self.hypercube_addr = hypercube_addr

    def add_obj(self, obj, keyword):
        url = self.hypercube_addr + INSERT
        
        return requests.get(url=url, params={'obj': obj, 'keyword': str(keyword)})
    
    def remove_obj(self, obj, keyword):
        url = self.hypercube_addr + REMOVE
        
        return requests.get(url=url, params={'obj': obj, 'keyword': str(keyword)})
    
    def pin_search(self, keyword, threshold=-1):
        url = self.hypercube_addr + PIN_SEARCH
        
        return requests.get(url=url, params={'keyword': str(keyword), 'threshold': threshold})
    
    def superset_search(self, keyword, threshold=10):
        url = self.hypercube_addr + SUPERSET_SEARCH

        return requests.get(url=url, params={'keyword': str(keyword), 'threshold': threshold, 'sender': 'user'})