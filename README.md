# ReproducibleQuantitativeDataScience

A course prepared by Dr Melanie Ganz and Dr Cyril Pernet, with guest lecturers: Dr Robert Oostenveld, Dr Michael Hanke, Dr Nikola Stikov, and Dr Russ Poldrack. The course structure is over 5 days plus personal work: 2 days, course work, 2 days, course work, and 1 day with presentations.

**For teachers**: We expect students to join the course several months after starting their PhD allowing them to already have data and some code. This will allow them to apply the concepts developed to their own data and code. It is also expected to have a platform to interact with students via a 'wall' with notes. 

**For students**: During the course, active participation is expected. In session 1, we'll use [padlet](https://padlet.com/dashboard) to interact with each other (anonymous posting allowed) and also do group work. In session 2, we use GitHub (that you learn in session 1) to share code and review each other code. It is recommended to share something you are working on, but if you feel uncomfortable with that, prepare something to be shared/reviewed. In session 3, you must present in front of everybody. While it may feel uncomfortable, it is expected from any PhD student to be able to do so, and not just for this course. In general, there are no rights and wrongs in trying to improve reproducibility, it is only expected that you try given the conceptual and practical tools presented.

## Part 1

### Day 1 - Data Collection and data storage

- Introduction to reproducibility: [Definitions and origins](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.01_Definitions%26Origins.pdf)  
- How do you store data on your computer? [Data structures and data naming](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.02_StoringData%26Code.pdf)  
- Data provenance: [keeping track of where data are coming from](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.03_DataProvenance.pdf)  
- [Reproducibility is hard](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.04_ReproducibilityIsHard.pdf): [case studies](http://www.practicereproducibleresearch.org/core-chapters/4-casestudies.html) 

### Day 2 - Reproducible designs, protocols and pre-registration

- [Concepts and tools for protocol documentation, and study pre-registration](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.05_Concepts%26Tools_doc%26preregistration.pdf)  
- [Data Privacy, Ethic and GDPR](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.06_Ethic%26GDPR.pdf) - lecture and practical case reviews 
- [Using markdown](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.07_Using_markdown_for_documentation.pdf) see [cheat sheet](https://www.markdownguide.org/cheat-sheet/) for documentation - practical  
- [Version control and social coding with Git](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/1.08_VersionControl_Mkd_SocialCoding.pdf) see the [quick sheet](https://github.com/CPernet/Quicksheets/blob/main/git_github/git.mkd) and GitHub  -- people who know can pair wih newbies

*Please prepare before the course*:
- install [git version control](https://git-scm.com/install/windows) on your machine
- create an account on [GitHub](https://github.com/) if you do not have one
- we recommend installing [GitHub desktop](https://desktop.github.com/download/). It usually also comes with git but we have seen some weird windows installation, so please check git bash is present on your machine
- not mandatory, but recommended (also used in the next section), is to install [VSCode](https://code.visualstudio.com/download), open it and sign in your github account.

 
### Course work

Using your PhD research data, protocol, code, etc, write a report explaining from where you start, and which measures are already in place to increase reproducibility as per concepts presented during days 1 and 2. What measures can be taken to increase reproducibility and if any, why some cannot be implemented? (page count 2 to 3)

## Part 2

### Day 3 - Better coding 

- [Programming](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/2.01_Programming.pdf)  
- [Good coding practices](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/2.02_Better_coding.pdf)   
- [An introduction to computational analysis methods](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/2.03_Computational_analysis_methods.pdf): permutation, bootstrap, cross-validation, out-of-sample generalization
- Agentic coding. The lecture is inspited from [Russ' Poldrack 2025 AI testing repo](https://zenodo.org/records/21455933)
- Time to update your code - implement some of the practices discussed today using agentic coding, let's review each other work/discuss. Tip: don't forget to version control your code, makes it easier to see what the agent changes.

*Please prepare before the course*:  
Install [VSCode](https://code.visualstudio.com/download), open it and sign into your github account.  Make sure agents are enabled in your VS Code settings. You can use Copilot for free by signing up for the [Copilot Free plan](https://github.com/settings/copilot/features) and get a monthly allowance of inline suggestions and AI credits

### Day 4 - Better analyses 

- Understanding p-values (see [notebook](https://github.com/CPernet/ReproducibleQuantitativeDataScience/tree/main/p_values))
- [P-hacking](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/2.04_Hacking_HARKing_and_SHARKING_your_research.pdf) your data  
- Feedback on coursework and discuss further issues to make your PhD reproducible  
- [Computational reproducibility] the lecture is inpired by the 2023/2024/2025 lecture from Michael Hanke see his repository [here](https://files.inm7.de/mih/pres/talks/rdm_reproducibility_copenhagen2023.html) (lecture and practical all afternoon). 

*Please prepare before the course*:
- [install docker on your own machine](https://docs.docker.com/engine/install/) so you can use a container and then build a container. For wondows users, you need 1st to have the linux subsystem insalled (in power shaell, type ```wsl-ext --install```)
- [install uv](https://docs.astral.sh/uv/getting-started/installation/) this is a package managment + virtual environment that plays well with python

### Course work 

Improve code you are using based on the concepts and tools reviewed over the 4 days: from version control and better inline documentation, to functionalization and modern computational statistics.  Make a 10 minutes presentation summarizing all of your course works and what measures you have taken to improve reproducibility in your PhD (including work from session 1). 

## Part 3

### Day 5 - Data sharing 

- The ‘data’ cycle, [sharing from raw data to figures](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/3.01_DataSharing.pdf) - lecture  
- [Reproducible publishing](https://github.com/CPernet/ReproducibleQuantitativeDataScience/blob/main/lecture_slides/3.02_OpenPublishing.pdf) - [see example here](https://preprint.neurolibre.org/10.55458/neurolibre.00014/) 
- Presentations and discussions/social event (drinks and pizza) 
