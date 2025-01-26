import requests
import urllib.parse  as p
API_KEY="<INSERT_YOUR_API_KEY>"
SEARCH_ENGINE_ID="<INSERT_YOUR_SEARCH_ENGINE_ID_HERE>"
target_domain="bbc.com"
query="google custom search engine api python"

for page in range(1,11):
    print("[*] Going for page:",page)

    #calculating start
    start=(page-1)*10+1

    #make Api req
    url= f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
    data=requests.get(url).json() #sends a GET request to the API
    search_items=data.get("items")
    found=False

    for i,search_item in enumerate(search_items,start=1):
        #get page title
        title=search_item.get("title")
        snippet=search_item.get("snippet")
        html_snippet=search_item.get("htmlSnippet")

        #extract page url
        link=search_item.get("link")

        #extract the domain name
        domain_name=p.urlparse(link).netloc
        if domain_name.endswith(target_domain):
            rank=i+start-1
            print(f"[+]{target_domain} is found on rank #{rank} for keyword:'{query}'")
            print("[+] Title:", title)
            print("[+] Snippet:", snippet)
            print("[+] URL:", link)
            found=True
            break
        if found:
            break