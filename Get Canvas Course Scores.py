# importing the requests library
import requests
import objectpath
from notiontocanvaslib import API, Notion

# Define my Notion and Canvas API Objects
notion = Notion("ntn_b10673621302a24oPSqUziNwSslqoGrA8ADNYaCixO10Vb", "https://api.notion.com/v1")
canvas = API("1109~C3TyerEHnmcXCNwyEJnJcuv6e8JXhQAw46z8QAXcFyWRF6wzvfEmTBD2XNX22VvZ", "https://uc.instructure.com/api/v1")

# Set up the right Notion Headers
notion.headers.update({"Content-Type": "application/json", "Notion-Version": "2022-06-28",})

#-----------End Setup-------------#

# Get a list of Canvas Courses, and extract the Scores and Names as separate lists
Courses = canvas.GET("/courses", {"include": ["current_grading_period_scores", "total_scores"], "enrollment_state": "active"})
Courses_Object = objectpath.Tree(Courses.json())
Scores = list(Courses_Object.execute('$..computed_current_score'))
Names = list(Courses_Object.execute('$..name'))

# Divide Scores by 100
for i in range(len(Scores)):
  print(type(Scores[i]))
  if (type(Scores[i]) == float):
    Scores[i] = (Scores[i] / 100)
  else:
    pass

# Find the database ID for Notion

Databases = notion.SearchNotion(Title = "Canvas Database", Type = "database")
Database_ID = Databases.get('results')[0].get('id')
Database_ID = str(Database_ID)


# For all of the courses, either create a new page with the latest score, or update the existing page with the latest score
for i in range(len(Names)):
  Filters = {
    "property": "Name",
    "rich_text": {
      "contains": f"{Names[i]}"
    }
  }
  searchresultJSON = notion.SearchNotionDatabase(Database_ID, Filters)

  searchresultobject = objectpath.Tree(searchresultJSON)
  searchresult = list(searchresultobject.execute('$..results[0]'))

  Score = {"Score" : {"number" : Scores[i]}}
  
  if (searchresult == []):
    # If the page doesn't exist, create it and add the latest score
    print(notion.CreateNotionPageInDatabase(Database_ID, f"{Names[i]}", Score))
  else:
    # Say that the page already exists
    # Update the existing page with the latest score
    print(f"Page '{Names[i]}' already exists")
    pageid = searchresultobject.execute('$..id[0]')
    notion.PatchNotionPage(pageid, Score)









