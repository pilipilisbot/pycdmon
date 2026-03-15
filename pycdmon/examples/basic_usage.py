from pycdmon import CdmonDomainsClient

API_KEY = "YOUR_API_KEY"

with CdmonDomainsClient(api_key=API_KEY) as client:
    print(client.check("example.com"))
    print(client.get_price("com", "create"))
