import urllib

def resource_path(year, month, day):
    return f"prices/{year}/{str(month).zfill(2)}/{year}-{str(month).zfill(2)}-{str(day).zfill(2)}-prices.csv"


def download_link(year, month, day):
    return f"https://dev.azure.com/tankerkoenig/362e70d1-bafa-4cf7-a346-1f3613304973/_apis/git/repositories/0d6e7286-91e4-402c-af56-fa75be1f223d/items?path=/{resource_path(year, month, day)}&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=master&resolveLfs=true&%24format=octetStream&api-version=5.0&download=true"

# download file with target path
def download_file(year, month, day, target_path):
    link = download_link(year, month, day)
    print(f"Downloading {link} to {target_path}")
    try:
        urllib.request.urlretrieve(link, target_path)
    except urllib.error.HTTPError as e:
        print(f"Error: {e}")