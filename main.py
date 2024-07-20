import requests

def main():
  response = requests.get('https://ifconfig.me')
  print(response.text)

def get_ip():
  return get_url('https://ifconfig.me')

def get_url(url):
    try:
        response = requests.get(url, timeout=3)  # 设置3秒超时
        return response.text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""
    
if __name__ == "__main__":
  print(get_ip())