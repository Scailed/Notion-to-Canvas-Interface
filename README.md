# Import Your Canvas Assignments into Notion!

Do you hate Canvas's interface? Do all of your teachers organize their assignments in a different way? Do you use Notion? Do you like snakes? Well then you should use this script written entirely in Python to import your assignments from Canvas into Notion!

## Introduction
This is a python script I wrote to import all of my assignments from Canvas into Notion. There are much cleaner, faster, and probably more reliable ways to do this, but the primary objective for this project was to make it work, and to be able to write it quickly. However, I am interested in improving this project as much as possible, so I'm not just abandoning it on Github, this project is under continuous development, so check back every so often for updates. Bug reports and feedback are welcome! 

Last side note: when I was first starting out, I would read some readmes that made it seem like the project creator made an entire game engine from scratch in 8 hours or something ridiculous like that, and that made me feel like I was taking waaay too long. I now know that those numbers didn't include all of the research time and learning time that the programmer did before working on their project. So I want to make it clear that this project took me TWO WEEKS to write - learning a new aspect of a programming language takes a LONG TIME. If you're a newbie, don't worry if you can't finish an idea in an afternoon, you're a slow programmer right now because you aren't familiar with what you're working with. You'll get faster, but it'll take a month or so to notice the difference.

Alright, encouragement over, let's check out the features of this project.

## Features
- Connects to Canvas via Canvas API
- Connects to Notion via Notion API
- Imports these properties from Canvas:
  - Assignment name
  - Submission state
  - URL
  - Current assignment score
  - Whether the assignment is a quiz
  - Possible points for the assignment
  - Created time (Normally not visible in Canvas!)
  - The assignment's ID
  - The course ID for the assignment
  - Lock time
  - Due date
  - Grade group ID
  - Grade group name
  - Grade group weight
  - Grade group total points
  - Whether the assignment is omitted from your final grade
  - Current score for the assignment's grade group
  - Current score for the assignment's course
- Features in Notion Database
  - All typical sorting and filtering that Notion can do (sort by due date, filter by submission state, etc.)
  - Assignment grade impact when submitted (Note: this isn't accurate at the moment, more on that later)
  - It's Notion! You just have all of the properties from Canvas imported into one big database!

## Setup Instructions
Since this is basically a Python script I wrote to connect my Notion workspace to my Canvas assignments, it's going to be a lot harder to setup than just installing an app on your computer and running it, but it should run on any computer.

### Step 1: Clone the Github repository to your computer
If you aren't familiar with github, this just means that you're downloading a copy of my code onto your computer. 

**Make sure to save it somewhere easily accessible, you'll be running this script a lot. More on this later.**

### Step 2: Setup your API key for Canvas
In your Canvas dashboard, click on Account > Settings, and scroll down to the bottom of the settings page, you should see something like this, although you may have a different set of integrations. Luckily, the existing integrations don't affect our program at all.

![Canvas API window image](<Canvas API window screenshot.png>)

You'll want to click "New Access Token," this is how we'll allow our script to access our canvas assignment data. When you do, you'll see something like this window.

![alt text](<New Access Token Image.png>)

You don't have to say that the purpose is "Notion to Canvas Integration" for the script to work, so you can name it whatever you want. However, I would recommend naming it something descriptive in case you forget what it's for. I'd also recommend leaving the "Expiration Date" and "Expiration Time" blank so that you don't have to worry about your integration randomly cutting out on you. If you have some reason to set the expiration date and time, it won't affect the functionality of the program. At least until the expiration date passes, after that it won't work at all.

Once you've filled out the "Purpose" field, and either edited the "Expiration Date" and "Expiration Time," or left them blank, click "Generate Token." That'll pull up a window like this one:

![alt text](<Access Token Details.png>)

Canvas's advice is sound here, DO NOT close this window until you have the Token saved into a text file. I've actually included a place for you to put it in the repository files anyway, so you don't have to create your own! Open the folder that you cloned the github repository into. (Don't worry, the access token details window won't close unless you click the "X" in the top right, so it's safe to click off of your browser). From there, open the file named "API Keys & Database ID.txt". It'll look like this.

![alt text](<API Key txt file.png>)

 We're going to copy the API token from Canvas into this file. If you aren't sure what your token is, it's the long string of random characters titled "Token". In this example case, my token is "1109~kTzn8fE3MVX8KcfDHVJUYDcArnGmQRULBJ3YmyX8TcNr3aBftU7rDYK76CZE37LZ". Copy your token to your clipboard (Cmd/Ctrl + C), delete the text after "Canvas:" and paste the token in its place. If you're worried about the amount of space between "Canvas:" and your token, you don't have to worry. The script deletes any spaces before and after the token, so it won't break the program if you add an extra space or delete the existing space. Just make sure the token is on the same line as "Canvas:"

 ![alt text](<API Key txt file with Canvas token paste.png>)

 Sweet! Save the "API Keys & Database ID.txt" file, and now it's safe to close the "Access Token Details" page in your browser. Phew!

 ### Step 3: Setup your API key for Notion

 This'll be a very similar process to what we just did, except that we're going to do it in Notion now.

 Click on [this link](https://www.notion.so/my-integrations) to go to your Notion "Integrations" page. You may get prompted to sign in if you aren't signed in already. It should look like this

 ![alt text](<Notion Integrations Page.png>)

Click on "New integration," and you'll be brought to the "New integration" page.

![alt text](<New Notion Integration Page.png>)

Go ahead and name this integration (I recommend "Canvas Integration," Notion won't let you have the word "notion" in your integration name :/ ), and set "Associated workspace" to the workspace that you'll use to track your Canvas Assignments. We'll be creating a database for the script to import into in a few minutes. Make sure "Type" is set to internal, and then click "Save." You should see a pop-up like this

![alt text](<Tutorial Images/Integration Successfully Created Popup.png>)

Go ahead and click on "Configure integration settings." Or, just click the "x" for some reason, both options will do the same thing.

![alt text](<Tutorial Images/Notion API Configuration Page.png>)

We want to double check that the integration has the right permissions, so make sure that "Read content", "Update content", and "Insert Content" are all checked. This script doesn't read any user info, but if you want to be extra super safe, you can set "User Capabilities" to "No user information" without hurting my feelings. You are downloading a script written by a stranger on GitHub after all.

![alt text](<Tutorial Images/User Capabilities set to No user information.png>)

Now we can copy the API Token for use with Notion! Click "Show" on the Internal Integration Secret bar, that'll show your API token.

![alt text](<Tutorial Images/Integration Secret Screenshot.png>)

Click "Copy", pull up the "API Keys & Database ID.txt" file, delete the text that says, "Paste Notion API Key Here (No Quotation Marks!)", and then paste the API token we just copied in place of the text we deleted.

![alt text](<Tutorial Images/API Key txt file Notion token paste.png>)

Sweet! That's everything we needed to do for our API Keys

### Step 4: Setup your Notion Database

We're almost there, now we just need to setup your Notion Database.

Head to [this site](https://mountain-driver-4a5.notion.site/20f03f9ea75281a79c31f3dac0f51576?v=20f03f9ea752814f8ea8000c8789296d) and click the duplicate icon in the upper right corner; It should look something like this:

![alt text](<Tutorial Images/Notion Duplicate Icon.png>)

That'll bring you to your own Notion workspace, where you can choose where you'd like the frontend page to be saved. Don't worry, the frontend page contains the database.

Once you've placed the frontend page somewhere in your workspace, go ahead and open it up. Click on "Canvas Assignments" at the bottom. This next part is a little odd, but bear with me, this is the easiest way I could find to get the database ID.

If you're using the Notion app, click "share" in the top right, then click "copy link" and paste that link into your browser.

If you're just using Notion on the web, then you can skip the previous step

Click on the URL of the database - you'll see a huge mess of random characters after "https://www.notion.so/" we're interested in a very specific set of those characters. Between "https://www.notion.so/" and "?v=" there should be a string of 32 characters; That's your database ID

![alt text](<Tutorial Images/Notion Database ID.png>)

Copy the ID, pull up the "API Keys & Database ID.txt" file, and replace "Paste Notion Database ID Here (No Quotation Marks!)" with the database ID you copied. Save the file, and now you're all set to use this integration!

## Usage Instructions

Open up "Assignments Info.py" and run it. In the console, when you first run the script, you should see messages saying that each of your assignments have been created. If you open your database in Notion, you should see your assignments appear one by one as the script creates them.

In order to update your assignment list in Notion, you'll just have to run "Assignments Info.py" again. It usually takes about 5 minutes to completely run through each assignment, and I'd recommend running it at least once a day. I know that's a tedious process, so if you have any ideas on how to make it better, feel free submit a pull request if you've written a better solution. Otherwise, have fun using Notion with Canvas!