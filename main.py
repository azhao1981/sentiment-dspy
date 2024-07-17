import requests

def main():
  response = requests.get('https://ifconfig.me')
  print(response.text)

if __name__ == "__main__":
  main()