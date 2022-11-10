from urllib import request, error


def resource_path_prices(year, month, day):
    return f"prices/{year}/{str(month).zfill(2)}/{year}-{str(month).zfill(2)}-{str(day).zfill(2)}-prices.csv"

def resource_path_stations(year, month, day):
    return f"stations/{year}/{str(month).zfill(2)}/{year}-{str(month).zfill(2)}-{str(day).zfill(2)}-stations.csv"

def download_link_prices(year, month, day):
    return f"https://dev.azure.com/tankerkoenig/362e70d1-bafa-4cf7-a346-1f3613304973/_apis/git/repositories/0d6e7286-91e4-402c-af56-fa75be1f223d/items?path=/{resource_path_prices(year, month, day)}&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=master&resolveLfs=true&%24format=octetStream&api-version=5.0&download=true"

def download_link_stations(year, month, day):
    return f"https://dev.azure.com/tankerkoenig/362e70d1-bafa-4cf7-a346-1f3613304973/_apis/git/repositories/0d6e7286-91e4-402c-af56-fa75be1f223d/items?path=/{resource_path_prices(year, month, day)}&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=master&resolveLfs=true&%24format=octetStream&api-version=5.0&download=true"

# download file with target path
def download_file(year, month, day, link: str, target_path):
    link = download_link_prices(year, month, day)
    print(f"Downloading {link} to {target_path}")
    try:
        request.urlretrieve(link, target_path)
    except error.HTTPError as e:
        print(f"Error: {e}")

def download_prices(year, month, day, target_path):
    download_file(year, month, day, download_link_prices(year, month, day), target_path)

def download_stations(year, month, day, target_path):
    download_file(year, month, day, download_link_stations(year, month, day), target_path)