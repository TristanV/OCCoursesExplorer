# -*- coding: utf-8 -*-
# STREAMLIT_APP 
# Copyright (c) 2022, Tristan Vanrullen - all rights reserved.
# Streamlit demo for OCCoursesExplorer
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import OCCoursesConfig as occ
# from OCCoursesConfig import display,IFrame,HTML
import OCCoursesDatasets as ocd
import OCCoursesAgenda as oca
import OCCoursesGraphs as ocg


st.set_page_config(layout="wide")

@st.cache        
def load_datasets():
    # --- Dataset first load
    ocd.load_OC_datasets()        
 
    


def main():
    load_datasets()
    
    
    
    # st.title('OCCourses Explorer Demo')
    st.sidebar.title('OCCourses Explorer Demo')
    main_view = st.sidebar.selectbox('Explore OpenClassrooms',('Data','Topics', 'Paths', 'Courses', 'Schedule','Info'),key="main_view")
    st.sidebar.image('img/OCCoursesExplorer_logo.png',use_column_width='auto')
    st.sidebar.markdown("[OCCoursesExplorer on Github](https://github.com/TristanV/OCCoursesExplorer)")
    st.sidebar.markdown('---')
    st.sidebar.write('Last database update: 2022-12-06')   
    # --------------------------------------------------- 
    if main_view == 'Data':        
        st.header('OCCoursesExplorer Data Summary')
        
        
        c = st.container()
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Topics
        with col1:
            st.subheader("Topics")
            st.image('img/topic.png',use_column_width ='auto')        
            st.metric("Topics", len(ocd.OC_Topics))

        # Paths
        with col2:
            st.subheader("Paths")
            st.image('img/path.png',use_column_width ='auto')        
            st.metric("Paths", len(ocd.OC_Paths)) 
            st.image('img/bright_star.png',use_column_width ='auto') 
            st.metric("Paths skills", len(ocd.OC_PathsSkills))
            
        # Projects
        with col3: 
            st.subheader("Projects")
            st.image('img/project.png',use_column_width ='auto')       
            st.metric("Projects", len(ocd.OC_Projects)) 
            st.image('img/bright_star.png',use_column_width ='auto')  
            st.metric("Projects skills", len(ocd.OC_ProjectsSkills))
            st.image('img/multilink.png',use_column_width ='auto')     
            st.metric("Projects-courses links", len(ocd.OC_ProjectsCoursesLinks))
        
        # Courses
        with col4: 
                st.subheader("Courses")
                st.image('img/course.png',use_column_width ='auto')      
                st.metric("Courses", len(ocd.OC_Courses))
                st.image('img/part.png',use_column_width ='auto')        
                st.metric("Courses parts", len(ocd.OC_CoursesParts))
                st.image('img/chapter.png',use_column_width ='auto')        
                st.metric("Courses chapters", len(ocd.OC_CoursesChapters))
                st.image('img/bright_star.png',use_column_width ='auto')        
                st.metric("Courses skills", len(ocd.OC_CoursesSkills))
                st.image('img/link.png',use_column_width ='auto')        
                st.metric("Courses links", len(ocd.OC_CoursesLinks))       
                
                
                
                
                
        
    # ---------------------------------------------------
    elif main_view == 'Topics':    
        
        menu , viz = st.columns([1,4])
        
        with menu:
            st.header('Topics and Paths')
            paths_height_slider = st.slider("View height",200,1200,900,10,"%d px",key="paths_height_slider") 
            df=ocd.OC_Topics[["topic_name","topic_id"]][ocd.OC_Topics["topic_id"].isin(ocd.OC_Paths.topic_id.unique())].sort_values(by=["topic_name"])
            paths_topics_options={"-":"-"}
            for i,r in df.iterrows():
                paths_topics_options[r["topic_id"]]=r["topic_name"]
            paths_topic_selector = st.selectbox("Topic", paths_topics_options.keys(), format_func=lambda x: paths_topics_options[x], index=0,key="paths_topic_selector")
            paths_language_selector = st.selectbox("Lang", ["-"] + list(ocd.OC_Paths["path_language"].unique()), index=0,key="paths_language_selector")
            paths_level_selector = st.selectbox("Level", ["-"] + list(ocd.OC_Paths["path_level"].sort_values().unique()) , index=0,key="paths_level_selector") 
            paths_duration_selector = st.selectbox("Months", ["-"] + list(ocd.OC_Paths["path_duration_months"].sort_values().unique()), index=0,key="paths_duration_selector")

        
        href= occ.VizFolder+"oc_topics_and_paths.html"
        # heading="Topics and Paths at OpenClassrooms<i> ...et voilà</i>!"
        #encoding trick for those who like accents in their titles: 
        # heading=heading.encode('utf-8').decode('latin')
        frame_height=paths_height_slider
        frame_width =1000
        filter_options={
            "height":paths_height_slider,
            "topic":paths_topic_selector,
            "language":paths_language_selector,
            "level":paths_level_selector,
            "duration":paths_duration_selector
        } 
        # OC like bg color : "#d5d0f5"
        g = ocg.build_topics_and_paths_graph(height=str(frame_height)+'px', width='99%', bgcolor="#FFFFFF", font_color="#141414",
                                            directed=False,notebook=True,layout=False,show_buttons=False,
                                            filter_options=filter_options)
                                            #heading=heading, show_titles = True,
        g.show(href)
        HtmlFile = open(href, 'r', encoding='utf-8')
        source = HtmlFile.read() 
        with viz:
            components.html(source, height = frame_height+10,width=frame_width)
    # ---------------------------------------------------
    elif main_view == 'Paths':        
        st.header('Paths and Projects')
    # ---------------------------------------------------
    elif main_view == 'Courses':        
        st.header('Courses galaxy')
    # ---------------------------------------------------
    elif main_view == 'Schedule':        
        st.header('Paths schedule')
    # ---------------------------------------------------
    elif main_view == 'Info':        
        st.header('Information about this demo')
        content = Path("README_STREAMLIT_DEMO.md").read_text()
        st.markdown(content)
        
        
    return True
# end main() function        

        
if __name__ == '__main__':
    main()