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


st.set_page_config(page_title="OCCoursesExplorer Demo App",page_icon="img/telescope-icon_90.png",layout="wide",initial_sidebar_state="expanded")

@st.cache        
def load_datasets():
    # --- Dataset first load
    ocd.load_OC_datasets()        
 
    
def display_metric(metric_icon,metric_title,metric_value,metric_icon_width=36):
    # see https://discuss.streamlit.io/t/style-column-metrics-like-the-documentation/20464/13
    wch_colour_box = (0,204,102)
    wch_colour_font = (0,0,0)
    fontsize = 36 
    title_fontsize = 24 

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                {wch_colour_box[1]}, 
                                                {wch_colour_box[2]}, 0.15); 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 0.95); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 8px; 
                            padding-bottom: 8px;
                            line-height:38px;'>
                            <img src='{metric_icon}' width={metric_icon_width} style='vertical-align:top;'/>&nbsp;{metric_value}
                            <br/><span style='font-size: {title_fontsize}px; 
                                            margin-top: 0px;
                                            color: rgb({wch_colour_font[0]}, 
                                                    {wch_colour_font[1]}, 
                                                    {wch_colour_font[2]}, 1.0);'>
                                    {metric_title}
                                </span>
                    </p>""" 
    st.markdown(htmlstr, unsafe_allow_html=True)     
    # st.image(metric_icon,width=metric_icon_width) 
    # st.metric(metric_title, metric_value)

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
        st.subheader('OCCoursesExplorer Data Summary')
        
        
        #c = st.container()
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Topics
        with col1:
            st.subheader("Topics")
            display_metric(occ.OCGraphsIconsURL['topic'],'Topics',len(ocd.OC_Topics))
            #st.image('img/topic.png',width=48)        # ,use_column_width ='auto'
            #st.metric("Topics", len(ocd.OC_Topics))

        # Paths
        with col2:
            st.subheader("Paths")
            display_metric(occ.OCGraphsIconsURL['path'],'Paths',len(ocd.OC_Paths)) 
            display_metric(occ.OCGraphsIconsURL['skill'],'Paths skills',len(ocd.OC_PathsSkills))  
            
        # Projects
        with col3: 
            st.subheader("Projects")
            display_metric(occ.OCGraphsIconsURL['project'],'Projects',len(ocd.OC_Projects)) 
            display_metric(occ.OCGraphsIconsURL['skill'],'Projects skills',len(ocd.OC_ProjectsSkills))   
            display_metric(occ.OCGraphsIconsURL['project_link'],'Projects-courses links',len(ocd.OC_ProjectsCoursesLinks))    
        
        # Courses
        with col4: 
            st.subheader("Courses")
            display_metric(occ.OCGraphsIconsURL['course'],'Courses',len(ocd.OC_Courses))  
            display_metric(occ.OCGraphsIconsURL['part'],'Courses parts',len(ocd.OC_CoursesParts))  
            display_metric(occ.OCGraphsIconsURL['chapter'],'Courses chapters',len(ocd.OC_CoursesChapters)) 
            display_metric(occ.OCGraphsIconsURL['skill'],'Courses skills',len(ocd.OC_CoursesSkills))     
            display_metric(occ.OCGraphsIconsURL['course_link'],'Courses links',len(ocd.OC_CoursesLinks))     
        
    # ---------------------------------------------------
    elif main_view == 'Topics':    
        
        menu , viz = st.columns([1,4])
        
        with menu:
            st.subheader('Topics and Paths')
            paths_width_slider = st.slider("View width",200,1600,1000,10,"%d px",key="paths_width_slider") 
            paths_height_slider = st.slider("View height",200,1200,680,10,"%d px",key="paths_height_slider") 
            df=ocd.OC_Topics[["topic_name","topic_id"]][ocd.OC_Topics["topic_id"].isin(ocd.OC_Paths.topic_id.unique())].sort_values(by=["topic_name"])
            paths_topics_options={"-":"-"}
            for i,r in df.iterrows():
                paths_topics_options[r["topic_id"]]=r["topic_name"]
            paths_topic_selector = st.selectbox("🏫 Topic", paths_topics_options.keys(), format_func=lambda x: paths_topics_options[x], index=0,key="paths_topic_selector")
            paths_language_selector = st.selectbox("💬Lang", ["-"] + list(ocd.OC_Paths["path_language"].unique()), index=0,key="paths_language_selector")
            paths_level_selector = st.selectbox("🎓 Level", ["-"] + list(ocd.OC_Paths["path_level"].sort_values().unique()) , index=0,key="paths_level_selector") 
            paths_duration_selector = st.selectbox("📅 Months", ["-"] + list(ocd.OC_Paths["path_duration_months"].sort_values().unique()), index=0,key="paths_duration_selector")

        
        href= occ.VizFolder+"oc_topics_and_paths.html"
        # heading="Topics and Paths at OpenClassrooms<i> ...et voilà</i>!"
        #encoding trick for those who like accents in their titles: 
        # heading=heading.encode('utf-8').decode('latin')
        frame_height=paths_height_slider
        frame_width =paths_width_slider
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
        menu , viz = st.columns([1,4]) 
        
        with menu:
            st.subheader('Paths and Projects')
            
            projects_width_slider = st.slider("View width",200,1600,1000,10,"%d px",key="projects_width_slider") 
            projects_height_slider = st.slider("View height",200,1200,680,10,"%d px",key="projects_height_slider") 
            
            df=ocd.OC_Topics[["topic_name","topic_id"]][ocd.OC_Topics["topic_id"].isin(ocd.OC_Paths.topic_id.unique())].sort_values(by=["topic_name"])
            projects_topics_options={0:"-"}
            for i,r in df.iterrows():
                projects_topics_options[r["topic_id"]]=r["topic_name"]
            projects_topic_selector = st.selectbox("🏫 Topic", projects_topics_options.keys(), format_func=lambda x: projects_topics_options[x], index=0,key="projects_topic_selector")
            
            
            projects_paths_options={0:"-"}            
            if projects_topic_selector!=0:
                df=ocd.OC_Paths[["path_title","path_language","path_id"]][ocd.OC_Paths["topic_id"].isin([projects_topic_selector])].sort_values(by=["path_language","path_title"])
                for i,r in df.iterrows():
                    projects_paths_options[r["path_id"]]=r["path_language"]+" : "+r["path_title"] 
            projects_path_selector = st.selectbox("📚 Path", projects_paths_options.keys(), format_func=lambda x: projects_paths_options[x], index=0,key="projects_path_selector")
            
            
            projects_mountainshape_options={0:"Mountain",1:"OC Wheel",2:"StaiZway to OC",3:"Shad'OC Ladder"}
            projects_mountainshape_selector= st.selectbox("↝ Shape", projects_mountainshape_options.keys(), format_func=lambda x: projects_mountainshape_options[x], index=0,key="projects_mountainshape_selector",
                                                          help='The shape of the learning structure, to climb the path towards success')

            projects_max_depth_slider = st.slider("🔍 Max Depth",0,20,2,1,key="projects_max_depth_slider", 
                                                help='Do not explore links between courses too deeply : limit exploration to Max Depth !')
            
            projects_ireadmycoursesonce_check = st.checkbox("📚 Persistent learning",value=False,key="projects_ireadmycoursesonce_check",
                                                            help='I learn my courses once, so do not draw links towards courses already linked to another earlier project! (avoid too many links towards the same course)')
            
            projects_hidereferences_check = st.checkbox("🕚 Focused learning",value=False,key="projects_hidereferences_check",
                                                        help='Just focus on mandatory courses requirements, and ignore informative / optional references.')

            projects_relations_max_distance_slider =  st.slider("🙈 Max Lookout",0,20,2,1,key="projects_relations_max_distance_slider",
                                                                help='Long distance relations between courses may be disturbing: Max Lookout defines the max lookout distance. (links between courses over this max lookout distance will not be drawn in the graph)')
            
            projects_pseudonodes_check = False # This is a demo. Let's not disturb users with this experimental feature
             
                       
         
        href= occ.VizFolder+"oc_path_"+str(projects_path_selector)+"_projects_courses.html" 
        
        frame_height=projects_height_slider
        frame_width =projects_width_slider 
        filter_options={
            "height"                             : projects_height_slider,
            "topic"                              : projects_topic_selector,
            "path"                               : projects_path_selector,
            "max_depth"                          : projects_max_depth_slider,
            "i_read_my_courses_once"             : projects_ireadmycoursesonce_check,
            "hide_references"                    : projects_hidereferences_check,
            "relations_max_distance"             : projects_relations_max_distance_slider,
            "pseudo_nodes"                       : projects_pseudonodes_check,
            "mountain_shape"                     : projects_mountainshape_selector,
            "show_my_way"                        : False
        }
         
        
        # OC like bg color : "#d5d0f5"
        path_id = projects_path_selector
        if (path_id==0):
            g = ocg.mini_graph("Select a Topic and a Path!",height=str(projects_height_slider)+'px', width='99%', 
                            bgcolor=occ.OCGraphsBackgroundColor, font_color=occ.OCGraphsTextColor,
                            directed=True,notebook=True,layout=False)
        else :   
            g = ocg.build_path_projects_courses_graph(path_id=path_id,
                            height=str(projects_height_slider)+'px', width='99%',
                            bgcolor="#FFFFFF", font_color="#141414",
                            directed=True,notebook=True,layout=False,show_titles=True,
                            show_buttons=False,filter_options=filter_options)  

        g.show(href)
        HtmlFile = open(href, 'r', encoding='utf-8')
        source = HtmlFile.read() 
        with viz:
            if path_id != 0:
                path= next(ocd.OC_Paths[ocd.OC_Paths["path_id"].isin([path_id])].iterrows())[1]
                st.title("Path structure for : "+path["path_title"])
            components.html(source, height = frame_height+10,width=frame_width)
    # ---------------------------------------------------
    elif main_view == 'Courses':        
        st.subheader('Courses galaxy')
    # ---------------------------------------------------
    elif main_view == 'Schedule':        
        st.subheader('Paths schedule')
    # ---------------------------------------------------
    elif main_view == 'Info':        
        st.subheader('Information about this demo')
        content = Path("README_STREAMLIT_DEMO.md").read_text()
        st.markdown(content)
        
        
    return True
# end main() function        

        
if __name__ == '__main__':
    main()