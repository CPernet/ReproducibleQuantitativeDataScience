# Git workshop exercises

All workshop participants are split into multiple groups. Please identify your group members...

# Instruction to get started with Git and GitHub

1 - Get a decent editor [Visual Studio](https://code.visualstudio.com/) is recommended, [Notepad++](https://notepad-plus-plus.org/downloads/) if you want to go really light)  
2 - Go to GitHub and open an account (which you may have if you read this online)  
3 - Windows and Mac users, download and install [GitHub desktop](https://desktop.github.com/)  (GUI to manage repositories, it really is easier)  
  
Note: a little knowledge of [bash](https://github.com/CPernet/Quicksheets/blob/main/bash/bash.mkd) goes a long way when using the Git command line.  

Warning: (1) make sure you log in from your editor to Github allowing easy push/pull/clone to/from the web; (2) make sure any folder you work one is not protected or ensure the software is allowed to write (e.g. exclude a folder in F-secure, allow VS code, etc).

## Link things together

Open a terminal (from VS code via the terminal menu, get [Git Bash](https://gitforwindows.org/) on Windows, any terminal otherwise)  
 
```
git config --global user.nane "GitHubUserName"   
git config --global user.email "YourEmail"
```

# Exercise 1

clone this repository! 

# Exercise 2

We have a separate directory for each group.

Please write a markdown file with short **introduction** about yourself. For example, what food do you like.

Save it with your name or your pseudonym like `yourname.md`, and add it to the directory that corresponds to your group.

Pull, Commit, Push and Pull to add your introduction - and also to get the introductions of the others.

#  Exercise 3

In each group directory there is a `README.md` file in which we want to collect **recommendations of movies and/or TV shows**.

Pull the latest changes to your local repository, edit the README and add your recommendation.

Commit and push...

As you are all doing this at (more or less) the same time, it is very likely that there will be merge conflicts and that chaos will ensue... breathe in and breathe out, and let's try to work these out together. Collaborating and social coding is not only about jointly contributing to a repository, but also on making agreements on the workflow. Who does what, in what order, and who takes responsibility.

#  Exercise 4

Create an [issue](https://github.com/Donders-Institute/git-workshop/issues) for one of your group members, for example ask them to add or modify a file. Assign a label to the issue and assign it to the group member that should resolve it.

**Working together** while not sitting next to each other (and possibly in different time zones) requires good communication. You can discuss the issue online: every comment that is added to the issue will result in an email. Other repository (aka team) members can also read along.
