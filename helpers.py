import requests

def get_rand_cat_quote():
    try:
        random_cat_quote = requests.get('https://catfact.ninja/fact').json()['fact']
    except Exception as e:
        print(e)
    return random_cat_quote

if __name__ == '__main__':
    print(get_rand_cat_quote())
