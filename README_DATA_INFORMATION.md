# INSIGHTS ON THE ONLINE UNIVERSITY PEDAGOGIC STRUCTURE AND MATERIAL

The data available on OpenClassrooms is not only free to use and transform (thanks to an open licence), but **structured as a huge pedagogic web-university**. 

The OCCoursesExplorer application tries to answer several questions asked by students like me during our online training, or throw some light on several subjects regarding this educational experience. Read the minidoc to understand the deep motivations for all this work.

Here are some of these questions about OpenClassrooms paths, projects and courses:

- What are the different diplomas or degrees available and compatible with my professional aspirations?
- What are the differences and commonalities between several paths or degrees?
- What are the online courses related to a path projects? 
- Taking into account the many links (mandatory prerequisites or optional references) between courses, in which order should the online courses be taken? 
- What is the cognitive or mental load that accompanies each project on a given path? How can we measure this load with metrics that are independent of course content and difficulty?
- Can we reduce this mental load by scheduling courses methodically? 
- What do I miss if I skip a given course?
- Are there some goldnuts hidden in the depths of the courses structure?

These questions arise either because of the **large amount of information to be taken into account** in order to keep a relevant overview, or because of the **sometimes very dense network structure of the knowledge** to be manipulated.

Educational websites are naturally using hyper-text browsing (links between pages) to render complex relations between pieces of information. The consequence of this is that the underlying data structures are sometimes disappearing and become implicit knowledge. 

Tables of content can easily render tree-structures (such as course-part-chapter-section), but they are irrelevant to render requirement-networks between pedagogic resources (for instance the course A requires mandatorily to have followed the course B, itself requiring the courses C and optionally the course D, and so on). When following a path and a given course, the students often meet situations when they cannot keep track of the relevant things to do to satisfy the course prerequisites. 

With OCCoursesExplorer, we first take things as they are (i.e. we consider the full OpenClassrooms pedagogic material as a graph) and collect it into an **internal graph-structure representation**. Then we observe this graph structure and apply graph-theory algorithms to **visualize things with a bird-eye view**, and break the courses network hyper-connex complexity into a **student-friendly simplified schedule**.

# From online university to an internal graph-structure representation

To turn a full website such as OpenClassrooms into a graph representation, we simply do (with computer science toolbox) what students do with their eyes and patience: we **read every page, and extract the underlying structure into a knowledge graph**. This kind of reverse-knowledge extraction makes use of **scraping techniques** (here made legally possible thanks to an open-licence).

The following image shows how this scraping process turns the OpenClassrooms website knwoledge into our graph knowledge base.


**The Paths are grouped by Topic**

![Scraping OpenClassrooms Topics and Paths](https://raw.githubusercontent.com/TristanV/OCCoursesExplorer/main/doc/scraping_OC_Topics_Paths_800.png) 


**The Paths are a list of Projects. Each Project is related to several Courses.**

![Scraping OpenClassrooms Projects](https://raw.githubusercontent.com/TristanV/OCCoursesExplorer/main/doc/scraping_OC_Projects_800.png)


**The Courses are grouped by Topic.**

![Scraping OpenClassrooms Courses](https://raw.githubusercontent.com/TristanV/OCCoursesExplorer/main/doc/scraping_OC_Courses_800.png)


**Each Course is structured into Parts and each Part into Chapters.**

**Courses are linked to other courses.**

**The links between courses can be 'prerequisites' (mandatory), or 'references' (optional).**

![Scraping OpenClassrooms Courses details](https://raw.githubusercontent.com/TristanV/OCCoursesExplorer/main/doc/scraping_OC_Courses_details_800.png)

# Content is evolving constantly!

An important aspect of the pedagogic material is that the courses, projects, paths and topics are continuously evolving. 

- Students provide feedback to teachers, who update their courses
- New technologies and techniques appear in the world, become 'nice to have' and replace old techniques. Hence Paths and projects evolve too!
- New diplomas are integrated in the online University program, so new Paths and new contents are often created.

For these reasons, the pedagogic **database needs to be scraped periodically**. This action is done with the OCCoursesExplorer main application, that can be launched with "Voilà!" or with a Jupyter Notebook (see the minidoc).

# From the internal graph-structure to an optimized schedule

Now considering the full graph representing a Path, its Projects and the Courses recommended for each Project, we can understand which parts of the graph will be a source of concern for the students. In many paths, the cognitive charge is increasing around the middle of the path, when many courses are followed simultaneously and many of these courses are linked together with strong prerequisites relations.

In the following image, one can see an overview of the graph for the *Web Developer* french path. 

The graph is showing the main **path project backbone** (here shaped as a mountain from project 1 at the bottom left, to project 8 at the top right). 

Each project is also linked to some courses with a green arrow (these courses are understood as **prerequisites courses** to successfully achieve the projects). Each course is also linked to other courses (**prerequisites** or simple **references**).

We want here to highlight the complexity issues when a student wants to follow 3 levels of references or requirements between courses (a standard learner will usually only need to follow 1 level of requirement or references). We can see a growing and overwhelming complex network as the path progresses from project 1 to project 6. 

![Web Developer Path (depth 2)](https://raw.githubusercontent.com/TristanV/OCCoursesExplorer/main/doc/OCCE_webdev_projects_depth2_800px.png)

The **persistent learning** optimization uses the fact that a course already followed for project N will not have to be followed again for project N+1 (I remember what I learned). So the **persistent learning** operation hides the links towards courses already visited in earlier projects. The following picture shows how the hyper-connexity issue is transformed into a simple tree structure.

![Web Developer Path (depth 2) with Persistent Learning optimization](https://raw.githubusercontent.com/TristanV/OCCoursesExplorer/main/doc/OCCE_webdev_projects_depth2_persistent_learning_800px.PNG)

Other optimizations have been made with the OCCExplorer application (**Focused Learning**, **Degree sort**), so that we could provide the best schedule for a given Path. These features will be documented later, but now you can start using the demo. Visit all the demo views, and feel free to send me some feedback via Github or LinkedIn!

# References

Source and documentation of this project are on Github : https://github.com/TristanV/OCCoursesExplorer/

A pdf of the minidoc is also accessible here : https://github.com/TristanV/OCCoursesExplorer/blob/main/doc/OpenClassrooms%20Courses%20Explorer%20minidoc.pdf

A live demo of main functionalities is on Streamlit : https://occourses.streamlit.app/
