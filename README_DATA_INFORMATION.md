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

Tables of content can easily render tree-structures (such as course-part-chapter-section), but they are irrelevant to render requirement-networks between pedagogic resources (for instance the course A requires mandatorily to have followed the course B, itself requiring the courses B and optionally the course C, and so on). So I came to the idea that 

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

For these reasons, the pedagogic **database needs to be scraped periodically**.


# References

Source and documentation of this project are on Github : https://github.com/TristanV/OCCoursesExplorer/

A pdf of the minidoc is also accessible here : https://github.com/TristanV/OCCoursesExplorer/blob/main/doc/OpenClassrooms%20Courses%20Explorer%20minidoc.pdf

A live demo of main functionalities is on Streamlit : https://occourses.streamlit.app/
