import requests
import objectpath

def GetAttributesFromJSON(attribute_tag, JSON):
    Attributes = []
    JSONobj = objectpath.Tree(JSON)
    Attributes = list(JSONobj.execute(f'$..{attribute_tag}'))
    return Attributes

class API:
    def __init__(self, AuthKey, URL):
        self.AuthKey = AuthKey
        self.URL = URL
        self.headers = {"Authorization": "Bearer {0}".format(AuthKey)}

    def GET(self, URL_Suffix, params):
        r = requests.get(self.URL + URL_Suffix, headers=self.headers, params=params)
        return r

    def GETALL(self, URL_Suffix, inputParams):
        headers = self.headers
        results = []
        url = self.URL + URL_Suffix
        params = inputParams
        params.update({'per_page': 10, 'page': 1})
        while True: 
            # send request 
            response = requests.get(url, params=params, headers=headers) 
            # check status code 
            if response.status_code != 200: 
              raise ValueError('Request failed with status code ' + str(response.status_code)) 
            # parse response data 
            data = response.json()
            # add results to list 
            results.extend(data) 
            params = {}
            # check if there are more pages 
            if 'next' in response.links.keys(): 
              url = response.links['next']['url'] 
            else: 
              break 
        return results

    def POST(self, URL_Suffix, Data):
        r = requests.post(self.URL + URL_Suffix, headers=self.headers, json=Data)
        return r
    
    def PATCH(self, URL_Suffix, Data):
        r = requests.patch(self.URL + URL_Suffix, headers=self.headers, json=Data)
        return r

    def PUT(self, URL_Suffix, Data):
        r = requests.put(self.URL + URL_Suffix, headers=self.headers, json=Data)
        return r
   
class Notion(API):
    def CreateNotionPage(self, JSON):
        self.POST("/pages", JSON).json()

    def CreateNotionPageInDatabase(self, Database_ID, Title, Properties):
        JSON = {
            "parent": {
                "database_id": Database_ID
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": f"{Title}"
                            }
                        }
                    ]
                }
            }
        }
        JSON["properties"].update(Properties)

        return self.POST("/pages", JSON).json()

    def SearchNotion(self, Title = "", Type = ""):
        JSON = {
            "filter": {
                "property": "object"
            },
            "sort": {
                "direction": "ascending",
                "timestamp": "last_edited_time"
            }
        }

        # This operation can only filter by these two properties - super annoying!
        if Title:
            JSON["query"] = f"{Title}"
        if Type:
            JSON["filter"]["value"] = f"{Type}"
        return self.POST("/search", JSON).json()
    
    def SearchNotionDatabase(self, Database_ID, Filters):
        JSON = {
            "filter": {

            }
            
        }

        JSON["filter"] |= (Filters)

        return self.POST(f"/databases/{Database_ID}/query", JSON).json()
    
    def PatchNotionPage(self, Page_ID, Properties):
        JSON = {
            "properties": {

            }
        }
        
        JSON["properties"].update(Properties)
        return (self.PATCH(f"/pages/{Page_ID}", JSON)).json()