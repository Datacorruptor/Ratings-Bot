

from github import Github

# First create a Github instance:

# using an access token
g = Github("")
repo = g.get_user().get_repo("Rating-Bot-Data")

all_files = []
contents = repo.get_contents("")
while contents:
   file_content = contents.pop(0)
   if file_content.type == "dir":
      contents.extend(repo.get_contents(file_content.path))
   else :
      file = file_content
      all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

with open('txt.txt', 'r') as file:
   content = file.read()


git_prefix = 'perenos/'
git_file = git_prefix + 'db.json'

if git_file in all_files:
   contents = repo.get_contents(git_file)
   repo.update_file(contents.path, "committing files", content, contents.sha, branch = "main")
   print(git_file + ' UPDATED')
else :
   repo.create_file(git_file, "committing files", content, branch = "main")
   print(git_file + ' CREATED')