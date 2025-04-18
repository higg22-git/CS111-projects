from urllib import parse
import requests

class RequestGuard():
    def __init__(self, url):
        self.url = url
        self.domain = get_domain(url)
        self.full_domain = get_full_domain(url)
        self.forbidden = self.parse_robots()


    def can_follow_link(self, url):
        if self.domain == get_domain(url):
            parsed_url = parse.urlparse(url)
            path = parsed_url.path
            for f_path in self.forbidden:
                if path.startswith(f_path):
                    return False
            return True
        else: 
            return False


    def make_get_request(self, url, use_stream = False):
        if self.can_follow_link(url):
            return requests.get(url, stream = use_stream)
        else:
            return None


    def parse_robots(self):
        robots_file = requests.get('https://' + self.domain + '/robots.txt')
        disallowed_paths = []
        i = 0
        for item in robots_file.text.split():
            if item == "Disallow:":
                if robots_file.text.split()[i+1].startswith('/'):
                    disallowed_paths.append(robots_file.text.split()[i+1])
            i += 1
        return disallowed_paths
    
    

def get_domain(url):
    parsed_url = parse.urlparse(url)
    scheme = parsed_url.scheme
    address = parsed_url.netloc

    if scheme == 'http' or scheme == 'https':
        return f"{address}"
    else:
        return ''
    
def get_full_domain(url):
    parsed_url = parse.urlparse(url)
    scheme = parsed_url.scheme
    address = parsed_url.netloc

    if scheme == 'http' or scheme == 'https':
        return f"{scheme}://{address}"
    else:
        return ''


if __name__ == "__main__":
    url = 'https://www.example.com'
    request_guard = RequestGuard(url)
    print(f"URL: {request_guard.url}")
    print(f"Domain: {request_guard.domain}")
    print(f"Forbidden: {request_guard.forbidden}")
    print(f"Can follow link: {request_guard.can_follow_link('https://www.example.com/some/path')}")
    print(f"GET request: {request_guard.make_get_request('https://www.example.com')}")