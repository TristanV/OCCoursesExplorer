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
        # st.subheader('OCCoursesExplorer Data Summary')
        
        
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
        more_info = st.expander("🡺📖 More information about the data used in this application", expanded=False)
        with more_info:
            content = Path("README_DATA_INFORMATION.md").read_text()
            st.markdown(content)
            #st.markdown(content,unsafe_allow_html=True)
    # ---------------------------------------------------
    elif main_view == 'Topics':    
        
        menu , viz = st.columns([1,4])
        
        with menu:
            st.subheader('Topics and Paths')
            df=ocd.OC_Topics[["topic_name","topic_id"]][ocd.OC_Topics["topic_id"].isin(ocd.OC_Paths.topic_id.unique())].sort_values(by=["topic_name"])
            paths_topics_options={"-":"-"}
            for i,r in df.iterrows():
                paths_topics_options[r["topic_id"]]=r["topic_name"]
            paths_topic_selector = st.selectbox("🏫 Topic", paths_topics_options.keys(), format_func=lambda x: paths_topics_options[x], index=0,key="paths_topic_selector")
            paths_language_selector = st.selectbox("💬Lang", ["-"] + list(ocd.OC_Paths["path_language"].unique()), index=0,key="paths_language_selector")
            paths_level_selector = st.selectbox("🎓 Level", ["-"] + list(ocd.OC_Paths["path_level"].sort_values().unique()) , index=0,key="paths_level_selector") 
            paths_duration_selector = st.selectbox("📅 Months", ["-"] + list(ocd.OC_Paths["path_duration_months"].sort_values().unique()), index=0,key="paths_duration_selector")
            other_inputs = st.expander("... other parameters", expanded=False)
            with other_inputs:
                paths_width_slider = st.slider("View width",200,1600,1000,10,"%d px",key="paths_width_slider") 
                paths_height_slider = st.slider("View height",200,1200,680,10,"%d px",key="paths_height_slider") 
            
        
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
                                                          help='The shape of the learning structure, to climb the path towards success. Select a shape to see differently how projects are connected to courses.')

            projects_max_depth_slider = st.slider("🔍 Max Depth",0,20,2,1,key="projects_max_depth_slider", 
                                                help='Do not explore links between courses too deeply : limit exploration to Max Depth !')
            
            projects_ireadmycoursesonce_check = st.checkbox("📚 Persistent learning",value=False,key="projects_ireadmycoursesonce_check",
                                                            help='I learn my courses once, so do not draw links towards courses already linked to another earlier project! (avoid too many links towards the same course)')
            
            projects_hidereferences_check = st.checkbox("🕚 Focused learning",value=False,key="projects_hidereferences_check",
                                                        help='Just focus on mandatory courses requirements, and ignore informative / optional references.')

            projects_relations_max_distance_slider =  st.slider("🙈 Max Lookout",0,20,1,1,key="projects_relations_max_distance_slider",
                                                                help='Some courses are transitively linked to other courses (A to B, B to C, C to D), but are also linked directly to the same courses (A to D for instance). Long distance relations between courses may be disturbing: Max Lookout is defined as the max distance between courses that are already transitively connected, over which the links will not be drawn in the graph)')
            
            projects_pseudonodes_check = False # This is a demo. Let's not disturb users with this experimental feature
             
            other_inputs = st.expander("... other parameters", expanded=False)
            with other_inputs:
                projects_width_slider = st.slider("View width",200,1600,1000,10,"%d px",key="projects_width_slider") 
                projects_height_slider = st.slider("View height",200,1200,680,10,"%d px",key="projects_height_slider")            
         
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
                st.header("Path structure for : "+path["path_title"])
            components.html(source, height = frame_height+10,width=frame_width)
    # ---------------------------------------------------
    elif main_view == 'Courses':         
        menu , viz = st.columns([1,4]) 
        
        with menu:
            st.subheader('Courses galaxy') 
                
            # "max_depth"                          : courses_max_depth_slider,
            # "hide_references"                    : courses_hidereferences_check,
            # "atlas_layout"                       : courses_algo_check, 
            
            courses_inputs = st.expander("📒 Course filters", expanded=False)
            with courses_inputs:
                df=ocd.OC_Topics[["topic_name","topic_id"]][ocd.OC_Topics["topic_id"].isin(ocd.OC_Paths.topic_id.unique())].sort_values(by=["topic_name"])
                courses_topics_options={0:"-"}
                for i,r in df.iterrows():
                    courses_topics_options[r["topic_id"]]=r["topic_name"]
                courses_topic_selector = st.selectbox("🏫 Course Topic", 
                                                    courses_topics_options.keys(), 
                                                    format_func=lambda x: courses_topics_options[x], 
                                                    index=0,
                                                    key="courses_topic_selector",
                                                    help="Only show courses having the given topic")
                
                courses_language_selector = st.selectbox("💬 Course Lang", 
                                                         ["-"] + list(ocd.OC_Courses["course_language"].unique()), 
                                                         index=0,
                                                         key="courses_language_selector",
                                                         help="Only show courses having the given lang")
                
            paths_inputs = st.expander("📚 Path filters", expanded=False)
            with paths_inputs:                
                df=ocd.OC_Topics[["topic_name","topic_id"]][ocd.OC_Topics["topic_id"].isin(ocd.OC_Paths.topic_id.unique())].sort_values(by=["topic_name"])
                courses_path_topics_options={0:"-"}
                for i,r in df.iterrows():
                    courses_path_topics_options[r["topic_id"]]=r["topic_name"]
                courses_path_topic_selector = st.selectbox("🏫 Path Topic", 
                                                           courses_path_topics_options.keys(), 
                                                           format_func=lambda x: courses_path_topics_options[x], 
                                                           index=0,
                                                           key="courses_path_topic_selector",
                                                           help="Only show paths having the given topic")
                courses_path_language_selector = st.selectbox("💬 Path Lang", 
                                                              ["-"] + list(ocd.OC_Paths["path_language"].unique()), 
                                                              index=0,
                                                              key="courses_path_language_selector",
                                                              help="Only show paths having the given lang")
            
                courses_paths_options={0:"-"}            
                # select topics having paths
                df = ocd.OC_Topics[["topic_name","topic_id"]][ocd.OC_Topics["topic_id"].isin(ocd.OC_Paths.topic_id.unique())]
                # merge paths with these topics
                df = ocd.OC_Paths.merge(df, on='topic_id', how='left').sort_values(by=["topic_name","path_language","path_title"])
                if courses_path_topic_selector!=0:
                    df=df[["path_title","path_language","path_id","topic_name","topic_id"]][df["topic_id"].isin([courses_path_topic_selector])].sort_values(by=["topic_name","path_language","path_title"])
                if courses_path_language_selector!='-':
                    df=df[["path_title","path_language","path_id","topic_name","topic_id"]][df["path_language"].isin([courses_path_language_selector])].sort_values(by=["topic_name","path_language","path_title"])
                for i,r in df.iterrows():
                    courses_paths_options[r["path_id"]]=r["topic_name"][:3]+"-"+r["path_language"]+" : "+r["path_title"] 
                courses_path_selector = st.selectbox("📚 Path", 
                                                    courses_paths_options.keys(), 
                                                    format_func=lambda x: courses_paths_options[x], 
                                                    index=0,
                                                    key="courses_path_selector",
                                                    help="Show all paths of this list, or select one path") 
                
                courses_max_depth_slider = st.slider("🔍 Max Depth",0,20,0,1,key="courses_max_depth_slider", 
                                                help='Do not explore links between courses too deeply : limit exploration to Max Depth !')
            
                courses_hidereferences_check = projects_hidereferences_check = st.checkbox("🕚 Focused learning",value=False,key="courses_hidereferences_check",
                                                        help='Just focus on mandatory courses requirements, and ignore informative / optional references.')

                courses_connexpaths_check = st.checkbox('🔗 Show only courses linked to the visible paths',False,key='courses_connexpaths_check',
                                                        help='Show only courses related to the selected paths (courses belonging to paths connex graph). Hide courses and links not related to the selected paths.')
                
             
            other_inputs = st.expander("... other parameters", expanded=False)
            with other_inputs:
                courses_palette_selector = st.selectbox("🎨 Graph color palette",["Topic","Dependency","Hybrid"],index=0,key="courses_palette_selector",
                                                        help="Choose a color palette to setup how courses, paths and dependencies are drawn.")
                
                courses_algo_check = st.checkbox("🌐 Force Atlas layout",False, key="courses_algo_check",
                                                 help="Choose whether the graph is layout freely or is constrained into a spherical shape.")
                courses_width_slider = st.slider("View width",200,1600,1000,10,"%d px",key="courses_width_slider") 
                courses_height_slider = st.slider("View height",200,1200,680,10,"%d px",key="courses_height_slider")               
         
        href= occ.VizFolder+"custom_oc_courses.html" 
        
        frame_height=courses_height_slider
        frame_width =courses_width_slider  
        
        filter_options={
            "height"                             : courses_height_slider,
            "topic"                              : courses_topic_selector,
            "language"                           : courses_language_selector,
            "path_topic"                         : courses_path_topic_selector,
            "path_language"                      : courses_path_language_selector,
            "path"                               : courses_path_selector, 
            "max_depth"                          : courses_max_depth_slider,
            "hide_references"                    : courses_hidereferences_check,
            "atlas_layout"                       : courses_algo_check,
            "show_my_way"                        : False, 
            "palette"                            : courses_palette_selector,
            "connex_paths"                       : courses_connexpaths_check
        }
    
         
        
        # OC like bg color : "#d5d0f5" 
        g = ocg.build_courses_graph(topic_id=courses_topic_selector,
                                language=courses_language_selector,
                                path_topic_id=courses_path_topic_selector,
                                path_language=courses_path_language_selector,
                                path_id=courses_path_selector,
                                max_depth=courses_max_depth_slider,
                                atlas_layout=courses_algo_check,
                                show_my_way=False,
                                show_only_requirement_relations=courses_hidereferences_check,
                                height=str(courses_height_slider)+'px', width='99%',
                                palette=courses_palette_selector,
                                bgcolor="#FFFFFF", font_color="#141414",
                                directed=True,notebook=True,layout=False,show_titles=True,
                                show_buttons=False,filter_options=filter_options)    
        
        if (type(g)!=type(None)):
            g.show(href)
            HtmlFile = open(href, 'r', encoding='utf-8')
            source = HtmlFile.read() 
            with viz:
                components.html(source, height = frame_height+10,width=frame_width)
                # debug purpose
                # options = g.options.to_json()
                # import json
                # opt=json.loads(options)
                # st.write(opt)
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