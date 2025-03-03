from notiontocanvaslib import API, Notion
import notiontocanvaslib as ntc
import objectpath


# Read the API Keys and Database ID from the aptly named "API Keys & Database ID.txt" file
APIKeyFileDict = {}
with open("API Keys & Database ID.txt", "r") as APIKeyFile:
    APIKeyAndDatabaseIDFileDict = dict(line.strip().split(':', 1) for line in APIKeyFile)

NotionAPIKey = APIKeyAndDatabaseIDFileDict.get("Notion").strip()
CanvasAPIKey = APIKeyAndDatabaseIDFileDict.get("Canvas").strip()
DatabaseId = APIKeyAndDatabaseIDFileDict.get("Database_Id").strip()

# Define my Notion and Canvas API Objects
notion = Notion(NotionAPIKey, "https://api.notion.com/v1")
canvas = API(CanvasAPIKey, "https://uc.instructure.com/api/v1")

# Set up the right Notion Headers
notion.headers.update({"Content-Type": "application/json", "Notion-Version": "2022-06-28",})

#-----------End Setup-------------#

# Get a list of currently enrolled Canvas Courses
CourseJSON = canvas.GETALL("/courses", {"enrollment_state": "active"})
Courseids = ntc.GetAttributesFromJSON("id", CourseJSON)
print(Courseids)

# Get my Course Names
CourseNames = ntc.GetAttributesFromJSON("name", CourseJSON)


for j in range(len(Courseids)):
        
    # Get the list of assignments in one course
    AssignmentsJSON = canvas.GETALL(f"/courses/{Courseids[j]}/assignments", {})

    for i in range (len(AssignmentsJSON)):
        
        # Get a bunch of attributes from the assignment
        AssignmentName = AssignmentsJSON[i]["name"]
        AssignmentDescription = AssignmentsJSON[i]["description"]
        AssignmentDueDate = AssignmentsJSON[i]["due_at"]
        AssignmentURL = AssignmentsJSON[i]["html_url"]
        AssignmentId = AssignmentsJSON[i]["id"]
        AssignmentQuizState = AssignmentsJSON[i]["is_quiz_assignment"]
        AssignmentLockTime = AssignmentsJSON[i]["lock_at"]
        AssignmentPossiblePoints = AssignmentsJSON[i]["points_possible"]
        AssignmentCreatedTime = AssignmentsJSON[i]["created_at"]
        AssignmentCourseid = AssignmentsJSON[i]["course_id"]
        AssignmentGroupid = AssignmentsJSON[i]["assignment_group_id"]
        AssignmentCourseName = CourseNames[j]
        AssignmentOmitFromGrade = AssignmentsJSON[i]["omit_from_final_grade"]


        # Get the most recent grade for the assignment
        AssignmentSubmissionJSON = canvas.GET(f"/courses/{AssignmentCourseid}/assignments/{AssignmentId}/submissions/self", {}).json()

        # Get the Assignment Submission State
        if (AssignmentSubmissionJSON.get("submitted_at", ) == None):
            AssignmentSubmissionState = False
        else:
            AssignmentSubmissionState = True
        
        # Helpful tip: using .get() allows me to avoid a KeyError issue if the score doesn't exist yet
        AssignmentScore = AssignmentSubmissionJSON.get("score", )
        SubmissionId = AssignmentSubmissionJSON.get("id", )

        # Get the Assignment Group for the assignment from Canvas
        AssignmentGroupJSON = canvas.GET(f"/courses/{AssignmentCourseid}/assignment_groups", {}).json()
        AssignmentGroupJSON_Object = objectpath.Tree(AssignmentGroupJSON)
        AssignmentGroupName = list(AssignmentGroupJSON_Object.execute(f'$..*[@.id is {AssignmentGroupid}].name'))[0]
        AssignmentGroupWeight = list(AssignmentGroupJSON_Object.execute(f'$..*[@.id is {AssignmentGroupid}].group_weight'))[0] / 100
        
        # Get the data for the assignment groups from Canvas What-if Grades
        # This is a workaround for the fact that Canvas doesn't give me the total points for an assignment group anywhere except for the What-if grades endpoint

        # It would be really easy to just use this feature to calculate how an assignment is impacting my grade, but I don't want to have to wait 20 minutes for
        # all of those to update
        TotalGradesJSON = canvas.PUT(f"/submissions/{SubmissionId}/what_if_grades", {"student_entered_score": None}).json()

        # Get total points for assignment groups, current scores for assignment groups, and ids for assignment groups
        TotalGradesJSONObject = objectpath.Tree(TotalGradesJSON)
        GroupPointTotals = list(TotalGradesJSONObject.execute('$.grades.current_groups..possible'))
        GroupScores = list(TotalGradesJSONObject.execute('$.grades.current_groups..grade'))
        GroupIds = list(TotalGradesJSONObject.execute('$.grades.current_groups..id'))
        CourseCurrentScore = list(TotalGradesJSONObject.execute('$.grades.current.grade'))
        
        # Check to make sure the course current score exists before turning it into a percentage
        if CourseCurrentScore[0]:
            CourseCurrentScore = CourseCurrentScore[0] / 100
        else:
            pass
        
        # Create two reference dictionaries, one for total points in assignment groups, and one for current scores of assignment groups
        GroupPointsDict = dict(zip(GroupIds, GroupPointTotals))
        GroupScoresDict = dict(zip(GroupIds, GroupScores))

        # From each of those reference dictionaries, get the assignment group's total points and 
        # the assignment group's current score that correspond to the current assignment
        AssignmentGroupPoints = GroupPointsDict.get(AssignmentGroupid, 0)
        AssignmentGroupCurrentScore = GroupScoresDict.get(AssignmentGroupid, 0)

        # Check to make sure the assignment group current score exists before turning it into a percentage
        if AssignmentGroupCurrentScore:
            AssignmentGroupCurrentScore = AssignmentGroupCurrentScore / 100
        else:
            pass

        # Almost done! Create a dictionary in Notion's API format, and assign the values we collected to the corresponding Notion properties
        NotionAssignmentJSON = {
            "parent": {
                "database_id": DatabaseId
            },
            "properties": {
                "Name": {
                "title": [
                    {
                    "text": {
                        "content": f"{AssignmentName}"
                    }
                    }
                ]
                },
                "Submitted?": {
                "checkbox": AssignmentSubmissionState
                },
                "URL": {
                "url": f"{AssignmentURL}"
                },
                "Score": {
                "number": AssignmentScore
                },
                "Quiz?": {
                "checkbox": AssignmentQuizState
                },
                "Possible Points": {
                "number": AssignmentPossiblePoints
                },
                "Created Time": {
                "date": {
                    "start": f"{AssignmentCreatedTime}"
                }
                },
                "Assignment Id": {
                "number": AssignmentId
                },
                "Course Id": {
                "number": AssignmentCourseid
                },
                "Course": {
                    "select": {
                        "name": f"{AssignmentCourseName}"
                    }
                },
                "Import": {
                    "select": {
                        "name": "Canvas Import"
                    }
                }
            }
        }

        # Incorporate these attributes, which aren't always included
        if AssignmentLockTime:
            NotionAssignmentJSON["properties"]["Lock Time"] = {
                "date": {
                    "start": f"{AssignmentLockTime}"
                }
            }
        if AssignmentDueDate:
            NotionAssignmentJSON["properties"]["Due Date"] = {
                "date": {
                    "start": f"{AssignmentDueDate}"
                }
            }
        if AssignmentGroupid:
            NotionAssignmentJSON["properties"]["Group Id"] = {
                "number": AssignmentGroupid
            }

        if AssignmentGroupName:
            NotionAssignmentJSON["properties"]["Assignment Group"] = {
                "select": {
                    "name": f"{AssignmentGroupName}"
                }
            }
        if AssignmentGroupWeight:
            NotionAssignmentJSON["properties"]["Group Weight"] = {
                "number": AssignmentGroupWeight
            }
        if AssignmentGroupPoints:
            NotionAssignmentJSON["properties"]["Group Total Points"] = {
                "number": AssignmentGroupPoints
            }
        if AssignmentOmitFromGrade:
            NotionAssignmentJSON["properties"]["Omit From Grade?"] = {
                "checkbox": AssignmentOmitFromGrade
            }
        if AssignmentGroupCurrentScore:
            NotionAssignmentJSON["properties"]["Assignment Group Current Score"] = {
                "number": AssignmentGroupCurrentScore
            }
        if CourseCurrentScore:
            NotionAssignmentJSON["properties"]["Course Current Score"] = {
                "number": CourseCurrentScore
            }

        Filters = {
        "property": "Assignment Id",
        "number": {
            "equals": AssignmentId
        }
        }
        searchresultJSON = notion.SearchNotionDatabase(DatabaseId, Filters)
        searchresultobject = ntc.objectpath.Tree(searchresultJSON)
        searchresult = list(searchresultobject.execute('$..results[0]'))

        if (searchresult == []):
            notion.POST("/pages", NotionAssignmentJSON).json()
            print(f"Assignment {AssignmentName} Created!")
        else:
            notion.PATCH(f"/pages/{searchresultobject.execute('$..id[0]')}", NotionAssignmentJSON)
            print(f"Assignment {AssignmentName} Updated!")