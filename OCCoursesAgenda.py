# -*- coding: utf-8 -*-
# OPENCLASSROOMS-COURSES-EXPLORER 
# Copyright (c) 2021, Tristan Vanrullen - all rights reserved.
# Note there is a licence for the code and another for the contents generated by the application
# see licence.txt for more details 

import OCCoursesConfig as occ
from OCCoursesConfig import pd, np, display, math, OCGraphsIconsURL
import OCCoursesDatasets as ocd
import OCCoursesGraphs as ocg
import OCCoursesPlots as ocp
import matplotlib
 

def get_agenda_html_page(body):
    page= '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=latin"/>    
<style type="text/css">
    table {
        width: 98%;
        border-collapse: collapse;
    }  
    tbody tr:nth-child(even) {
        background-color: #f6f7f6;
    }
    tbody tr:nth-child(odd) {
        background-color: #ffffff;
    }

    tbody tr:last-of-type {
        border-bottom: 3px solid #141414;
    }
    thead tr{
        background-color: #f1f1f1;
    }
    
    
    
    
    thead th {
        color: #141414;
        border-top: 1px solid #141414;
        border-bottom: 1px solid #141414;
        padding: 12px 15px;
    }  
    thead td.border {
        color: #242424;
        border-top: 1px solid #141414;
        border-bottom: 1px solid #141414;
        padding: 12px 15px;
        background-color: #fff;
        text-align:center;
    }
    thead td.noborder { 
        border: 0px;
        background-color: #fff;
    }
    tbody td {
        color: #242424;
        padding: 12px 15px;
        vertical-align:top;
    }
    tbody td.criticalpath{ 
        border-left : 3px solid #4de2c9 
    }
    .leftrefbox{ 
        border: 1px solid #eae3e6;
        border-right: 50px solid #eae3e6;
        padding: 12px 15px;
        text-align:left;
    }
    .rightrefbox{ 
        border: 1px solid #e3eae6;
        border-left: 50px solid #e3eae6;
        padding: 12px 15px;
        text-align:right;
    }
    div.OpenClassroomsCoursesExplorer {
        position: fixed;
        z-index:123;
        bottom: 20px;
        right: 20px;
        width: 400px;
        height:20px;
        text-align:center;
        font-size=10px;
        color:#343434;
        border: 1px solid #d5d0f5;
    }
    div.OpenClassroomsCoursesExplorer a{
        color:#141414; 
        font-size=11px;
    }
    </style>   
    </head>
    <body>'''
    page+=body
    page+=''' 
    <div class="OpenClassroomsCoursesExplorer">
        Schedule generated with <a href="https://github.com/TristanV/OpenClassroomsCoursesExplorer" target="_blank">OpenClassrooms Courses Explorer</a>
    </div>
    </body>
    '''
    return page
#end function

def get_course_layer(course_id,courses_layers):
    counter=0
    for layer in courses_layers:
        if course_id in layer:
            return counter
        counter+=1
    return -1
#end function


def get_course_rank(course_id,courses_ranks):
    counter=0
    for nodes in courses_ranks:
        if course_id in nodes:
            return counter
        counter+=1
    return -1
#end function

def get_degree_in(course_id,dfcc,dfc):
    return len(dfcc[dfcc["tgt_course_id"].isin([course_id]) & ~dfcc["src_course_id"].isin([course_id]) & dfcc["src_course_id"].isin(dfc.course_id.values)])
#end function

def get_degree_out(course_id,dfcc,dfc):
    return len(dfcc[dfcc["src_course_id"].isin([course_id]) & ~dfcc["tgt_course_id"].isin([course_id]) & dfcc["tgt_course_id"].isin(dfc.course_id.values)])
#end function

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
def get_project_dependencies(path_id,project_number,required_max_depth,references_max_depth,courses_exclusion_set):
    
    dfoccourses=ocd.OC_Courses
    dfoccourses=dfoccourses.merge(ocd.OC_MyProgressCourses,on="course_id",how="left")
    dfoccourses["status"]=dfoccourses["progression"].apply(ocg.progression_to_status)
    dfoccourses=dfoccourses.merge(ocd.OC_Topics[["topic_id","topic_color"]],on="topic_id",how="left")  
    dfoccourses["course_difficulty_grade"]=dfoccourses['course_difficulty'].map(ocd.course_grades)
    
    all_courses = set(dfoccourses.course_id.unique())
    
    # ------------ get the COURSES IMMEDIATELY REQUIRED FOR THE PROJECTs and relevant for the filter
    dfpc= ocd.OC_ProjectsCoursesLinks[ocd.OC_ProjectsCoursesLinks["path_id"].isin([path_id]) &\
                                      ocd.OC_ProjectsCoursesLinks["project_number"].isin([project_number])] # courses referenced/required by the project

    # ------------ get ALL the COURSES LINKED TO PROJECT COURSES TRANSITIVELY        
    #use sets to have unique courses IDs and avoid counting the same courses twice or more
    path_courses = set(dfpc.course_id.unique())
    path_critical_courses = set(dfpc.course_id.unique()) #courses only related to the project via requirement links
    courses_layers=[path_courses]
    courses_critical_layers=[path_critical_courses]
    depth=0 
    linked_courses_found=True
    while linked_courses_found and depth<max(required_max_depth,references_max_depth):
        linked_courses_found = False
        depth+=1
        df=ocd.OC_CoursesLinks[(ocd.OC_CoursesLinks["src_course_id"].isin(path_courses)) &\
                               ~(ocd.OC_CoursesLinks["tgt_course_id"].isin([0]))]
        tgt_courses=set()
        tgt_critical_courses=set()
        if(depth<=required_max_depth):
            dff=df[df["relation"].isin(["requires"])]
            tgt_courses=tgt_courses | set(dff.tgt_course_id.values)
            tgt_critical_courses=tgt_critical_courses | set(dff.tgt_course_id.values)
        
        if(depth<=references_max_depth):
            dff=df[~(df["relation"].isin(["requires"]))]
            tgt_courses=tgt_courses | set(dff.tgt_course_id.values)
            
        tgt_courses=tgt_courses - path_courses
        tgt_critical_courses=tgt_critical_courses - path_critical_courses
        #now iterate
        if (len(tgt_courses)>0):
            linked_courses_found = True
            courses_layers.append(tgt_courses)
            path_courses=path_courses | tgt_courses
        if (len(tgt_critical_courses)>0): 
            courses_critical_layers.append(tgt_critical_courses)
            path_critical_courses=path_critical_courses | tgt_critical_courses
    # end while  
    
    path_courses = path_courses - courses_exclusion_set #unused
    
    if (len(path_courses) == 0):
        return None,None,set()
        
    dfc=dfoccourses[dfoccourses["course_id"].isin(path_courses)]  
    dfc=dfc.sort_values(by=["course_duration_hours","course_difficulty_grade"]) 
    dfc["layer"]=dfc.apply(lambda x: get_course_layer(x['course_id'], courses_layers), axis=1)
    dfc["is_critical"]=dfc.apply(lambda x: x['course_id'] in path_critical_courses, axis=1)
    
    # ------------ get ALL the COURSES LINKED TO COURSES 
    dfcc=ocd.OC_CoursesLinks[(ocd.OC_CoursesLinks["src_course_id"].isin(path_courses)) & \
                         (ocd.OC_CoursesLinks["tgt_course_id"].isin(path_courses))].drop_duplicates(subset=["src_course_id","tgt_course_id","relation"])
    dfcc=dfcc.merge(dfoccourses, left_on='src_course_id', right_on='course_id', how='left')
    dfcc=dfcc[['src_course_id','relation', 'tgt_course_id','course_title','course_difficulty','course_duration_hours','status']].copy ()
    dfcc.columns=['src_course_id','relation', 'tgt_course_id','src_course_title','src_course_difficulty','src_course_duration_hours','src_status']
    dfcc=dfcc.merge(dfoccourses, left_on='tgt_course_id', right_on='course_id', how='left')
    dfcc=dfcc[['src_course_id','relation', 'tgt_course_id',\
               'src_course_title','src_course_difficulty','src_course_duration_hours','src_status',\
               'course_title','course_difficulty','course_duration_hours','status']].copy ()
    dfcc.columns=['src_course_id','relation', 'tgt_course_id',\
                  'src_course_title','src_course_difficulty','src_course_duration_hours','src_status',\
                  'tgt_course_title','tgt_course_difficulty','tgt_course_duration_hours','tgt_status']  
    dfcc["src_course_difficulty_grade"]=dfcc['src_course_difficulty'].map(ocd.course_grades)
    dfcc["tgt_course_difficulty_grade"]=dfcc['tgt_course_difficulty'].map(ocd.course_grades)
    dfcc=dfcc.sort_values(by=["tgt_course_duration_hours","tgt_course_difficulty_grade","src_course_duration_hours","src_course_difficulty_grade"]).drop_duplicates(subset=["src_course_id","tgt_course_id","relation"]) 
    
    # ------------- compute degrees, ranks and orders
    # well this is the core algorithm to order nodes in a network according to their dependency towards other nodes
    # we have "requirement" and "reference" links, the first being critical and the second being non mandatory
    # two rankings are hence calculated for these two subnetworks
    rank_req_dfcc=dfcc[dfcc["relation"].isin(["requires"])][["src_course_id","tgt_course_id"]].drop_duplicates().copy()
    rank_ref_dfcc=dfcc[~dfcc["relation"].isin(["requires"])][["src_course_id","tgt_course_id"]].drop_duplicates().copy()
    dfc["degree_req_in"]=dfc.apply(lambda x: get_degree_in(x['course_id'], rank_req_dfcc,dfc), axis=1) #unused
    dfc["degree_req_out"]=dfc.apply(lambda x: get_degree_out(x['course_id'], rank_req_dfcc,dfc), axis=1)
    dfc["degree_ref_in"]=dfc.apply(lambda x: get_degree_in(x['course_id'], rank_ref_dfcc,dfc), axis=1) #unused
    dfc["degree_ref_out"]=dfc.apply(lambda x: get_degree_out(x['course_id'], rank_ref_dfcc,dfc), axis=1)
    
    rank_req_dfc=dfc[["course_id","degree_req_in","degree_ref_in","degree_req_out","degree_ref_out"]].copy()
    courses_req_ranks=[]
    rank=0  
    while len(rank_req_dfc)>0:
        min_degree=rank_req_dfc["degree_req_out"].min()
        rank_req_nodes=set(rank_req_dfc[rank_req_dfc["degree_req_out"]==min_degree].course_id.values)
        courses_req_ranks.append(rank_req_nodes)
        rank_req_dfc=rank_req_dfc[~rank_req_dfc["course_id"].isin(rank_req_nodes)]
        rank_req_dfcc=rank_req_dfcc[~rank_req_dfcc["tgt_course_id"].isin(rank_req_nodes)]
        if len(rank_req_dfc)>0:
            rank_req_dfc["degree_req_out"]=rank_req_dfc.apply(lambda x: get_degree_out(x['course_id'], rank_req_dfcc,rank_req_dfc), axis=1)
        rank+=1
    # end while  
    rank_ref_dfc=dfc[["course_id","degree_req_in","degree_ref_in","degree_req_out","degree_ref_out"]].copy()    
    courses_ref_ranks=[]
    rank=0  
    while len(rank_ref_dfc)>0:
        min_degree=rank_ref_dfc["degree_ref_out"].min()
        rank_ref_nodes=set(rank_ref_dfc[rank_ref_dfc["degree_ref_out"]==min_degree].course_id.values)
        courses_ref_ranks.append(rank_ref_nodes)
        rank_ref_dfc=rank_ref_dfc[~rank_ref_dfc["course_id"].isin(rank_ref_nodes)]
        rank_ref_dfcc=rank_ref_dfcc[~rank_ref_dfcc["tgt_course_id"].isin(rank_ref_nodes)]
        if len(rank_ref_dfc)>0:
            rank_ref_dfc["degree_ref_out"]=rank_ref_dfc.apply(lambda x: get_degree_out(x['course_id'], rank_ref_dfcc,rank_ref_dfc), axis=1)
        rank+=1
    # end while  
    
#     display(courses_ranks)
    dfc["rank_req"]=dfc.apply(lambda x: get_course_rank(x['course_id'], courses_req_ranks), axis=1)
    dfc["rank_ref"]=dfc.apply(lambda x: get_course_rank(x['course_id'], courses_ref_ranks), axis=1)
    
    return dfc.sort_values(by=["rank_req","rank_ref","course_difficulty_grade","course_duration_hours","degree_req_out","degree_ref_out"]) ,\
            dfcc,\
            path_critical_courses
# end function

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
def build_path_agenda_html(path_id,required_max_depth=1,references_max_depth=0,options=None):
    ht="Please select a path"
    
#     options={
#         "path"                               : schedule_path_selector.value,   
#         "requires_max_depth"                          : schedule_requires_max_depth_slider.value,
#         "references_max_depth"                    : schedule_references_max_depth_slider.value
#     }
    if type(options)!=type(None): 
        path_id = options["path"] 
        required_max_depth=options["required_max_depth"]
        references_max_depth=options["references_max_depth"] 
    
    # ------------ get the PATH
    dfpa= ocd.OC_Paths[ocd.OC_Paths["path_id"].isin([path_id])]
    if len(dfpa)==0:
        return ht
    else: 
        ht="No Courses to schedule with these options!"
        
    dfpa=dfpa.merge(ocd.OC_Topics[["topic_id","topic_color"]],on="topic_id",how="left")    
    
    # ------------ get the PROJECTS of the PATH
    dfpr= ocd.OC_Projects[ocd.OC_Projects["path_id"].isin(dfpa.path_id.unique())].sort_values(by="project_number") # projects nodes
    dfpr=dfpr.merge(ocd.OC_Paths[["path_id","topic_id"]],on="path_id",how="left")
    dfpr=dfpr.merge(ocd.OC_Topics[["topic_id","topic_color"]],on="topic_id",how="left")
    dfpr=dfpr.merge(ocd.OC_MyProgressProjects,on=["path_id","project_number"],how="left")
    dfpr=dfpr.fillna(value={"status":"none"})
    dfpr=dfpr[["path_id","project_number","project_title","project_description","project_duration_hours","status"]].sort_values(by="project_number") 
    
    if len(dfpr) == 0:
        return ht
    else:
        path= next(ocd.OC_Paths[ocd.OC_Paths["path_id"].isin([path_id])].iterrows())[1]
        path_title=path["path_title"]#.encode('utf-8').decode('latin')
        ht=""
        img=""
        if (path["path_illustration"]!="" and path["path_illustration"]!=np.nan):
            img='<img width="180"/ valign="middle" src="'+path["path_illustration"]+'">' 
        ht+='<h1>'+img+'&nbsp;Schedule for the path '+path_title+'</h1>'
        ht+="<p>Language : "+path["path_language"]+" / Duration : "+str(path["path_duration_months"])+"m</p>" 
        ht+="<p>Hereunder is the schedule for required courses (depth="+str(required_max_depth)+")</p>"
        if (references_max_depth>0):
            ht+="<p>Recommended references are also explored (depth="+str(references_max_depth)+")</p>" 
    
    # ------------- SCHEDULE EACH PROJECT
    oc_colors=["#7451eb","#9471fb","#B491FE"]
    path_color="#7451eb"
    project_color="#5451db"
    course_color="#B491FE"
    link_colors={
        "primary_requires"    : "#2D2", # the requirement links between a project and courses
        "primary_references"  : "#22D", # the "other" links between a project and courses (the list is empty but we have a color for that :) )
        "secundary_requires"  : "#8C2", # the requirement links between courses of depth D to depth D+1
        "secundary_references": "#82C", # the other links between courses of depth D to depth D+1
        "tertiary_requires"   : "#DB2", #the requirement links between courses of depth D to any depth other than D+1
        "tertiary_references" : "#D2B", # the other links between courses of depth D to any depth other than D+1
        "long_link"           : "#BB8", # the other long distance links
    }
    
    # ---------- PROJECTS 
    courses_exclusion_set=set()
    total_allocated_duration=0
    total_scheduled_duration=0
    total_courses_critical_count=0
    total_scheduled_critical_duration=0
    total_courses_count=0
    total_scheduled_unbooked_duration=0
    total_courses_unbooked=0
    total_scheduled_booked_duration=0
    total_courses_booked=0
    total_scheduled_in_progress_duration=0
    total_courses_in_progress=0
    total_scheduled_done_duration=0
    total_courses_done=0
    for ii,nn in dfpr[dfpr["path_id"].isin([path_id])].iterrows():
        ht+="<h2>"+str(nn["project_number"])+"-"+nn["project_title"]+"</h2>" 
        
        project_allocated_duration = nn["project_duration_hours"]
        project_scheduled_duration=0
        project_courses_critical_count=0
        project_scheduled_critical_duration=0
        project_courses_count=0 
        project_scheduled_unbooked_duration=0
        project_courses_unbooked=0
        project_scheduled_booked_duration=0
        project_courses_booked=0
        project_scheduled_in_progress_duration=0
        project_courses_in_progress=0
        project_scheduled_done_duration=0
        project_courses_done=0
        # ----------- now grab the subset of courses required for this project
        dfc, dfcc, path_critical_courses = get_project_dependencies(path_id,nn["project_number"],required_max_depth,references_max_depth,set())
        # if there is no course for this project, let's jump to next project
        if (type(dfc)!=type(None)) and len(dfc)>0: 
            ht+="<table>"
            ht+="<thead><tr>"
            ht+="<th width='90px'>rank</th><th>status</th><th colspan=2>course</th><th>duration</th><th>needs</th><th>needed by</th>"
            ht+="</tr></thead><tbody>"
            # ---------- COURSES
            for i,r in dfc.iterrows():
                
                dur=0
                status="unbooked"
                ignore_this_course = False
                if r["course_id"] in courses_exclusion_set:
                    ignore_this_course=True
                else:
                    if r["course_duration_hours"]!=np.nan:
                        dur=r["course_duration_hours"]
                    project_scheduled_duration+=dur
                    project_courses_count+=1 
                    if (r["status"]=="none"):
                        status="Unbooked"
                        project_scheduled_unbooked_duration+=dur
                        project_courses_unbooked+=1
                    elif (r["status"]=="todo"):
                        status="To Do"
                        project_scheduled_booked_duration+=dur
                        project_courses_booked+=1
                    elif (r["status"]=="in_progress"):
                        status="In progress"
                        project_scheduled_in_progress_duration+=dur
                        project_courses_in_progress+=1
                    elif (r["status"]=="done"):
                        status="Achieved"
                        project_scheduled_done_duration+=dur
                        project_courses_done+=1  
                    if r["is_critical"] == True:
                        project_courses_critical_count+=1
                        project_scheduled_critical_duration+=dur
                classname=""
                if r["is_critical"] == True:
                    classname="criticalpath" 
                ht+="<tr>"
                if (ignore_this_course):
                    # ---------------
                    ht+="<td colspan=2 class='"+classname+"'>Planned in a previous project" 
                    ht+="<br/>Rank req: "+str(r['rank_req'])
                    ht+="<br/>Rank ref: "+str(r['rank_ref'])
#                     ht+="<br/>Order : "+str(r['order'])
                    ht+="<br/>°req out : "+str(r['degree_req_out'])
                    ht+="<br/>°ref out : "+str(r['degree_ref_out'])
                    ht+="<br/>°req in : "+str(r['degree_req_in'])
                    ht+="<br/>°ref in : "+str(r['degree_ref_in'])
                    ht+="<br/>Layer : "+str(r['layer'])
                    if r["is_critical"] == True:
                        ht+='<br/><b>On the critical path</b>'
                    ht+="</td>" 
                    # ---------------
                    ht+="<td colspan=2>"
                    ht+= str(r["course_id"])+"-<a href=\""+r["course_url"]+"\" target=\"_blank\">"+r["course_title"]+"</a>"
                    ht+="<br/>Course difficulty : "+str(r["course_difficulty_grade"])
                    ht+="</td>"
                    # ---------------
                    ht+="<td>-</td>"
                else:
                    # ---------------
                    ht+="<td class='"+classname+"'>"
                    ht+="Rank req: "+str(r['rank_req'])
                    ht+="<br/>Rank ref: "+str(r['rank_ref'])
#                     ht+="<br/>Order : "+str(r['order'])
                    ht+="<br/>°req out : "+str(r['degree_req_out'])
                    ht+="<br/>°ref out : "+str(r['degree_ref_out'])
                    ht+="<br/>°req in : "+str(r['degree_req_in'])
                    ht+="<br/>°ref in : "+str(r['degree_ref_in'])
                    ht+="<br/>Layer : "+str(r['layer'])
                    ht+="</td>"
                    # ---------------
                    imgurl=OCGraphsIconsURL["course"]
                    if r["status"]!=np.nan and r["status"]!="none":
                        imgurl=OCGraphsIconsURL["course_"+r["status"]]
                    ht+="<td>"
                    ht+='<img src="'+imgurl+'" height="40" align="middle"/>' 
                    ht+='<br/>'+status
                    if r["is_critical"] == True:
                        ht+='<br/><b>On the critical path</b>'
                    ht+="</td>"
                    # ---------------
                    img=""
                    if r["course_illustration"]!=np.nan and r["course_illustration"]!="":
                        img='<img src="'+r["course_illustration"]+'" height="80" align="middle"/>&nbsp;'
                    ht+="<td>"
                    ht+=img
                    ht+="</td>"
                    # ---------------
                    ht+="<td>"
                    ht+= str(r["course_id"])+"-<a href=\""+r["course_url"]+"\" target=\"_blank\">"+r["course_title"]+"</a>"
                    ht+="<br/>Course difficulty : "+str(r["course_difficulty_grade"])
                    ht+="</td>"
                    # ---------------
                    ht+="<td>" 
                    ht+=str(dur)+" h"
                    ht+="</td>"
                # --------------- 
                ht+="<td colspan='2'>" 
                
                required_courses=dfcc[dfcc["src_course_id"].isin([r["course_id"]]) & dfcc["relation"].isin(["requires"]) & ~dfcc["tgt_course_id"].isin([r["course_id"]]) ].merge(dfc,left_on="tgt_course_id",right_on="course_id",how="left").dropna(subset=["course_id"])
                if(len(required_courses)>0):
                    ht+="<div class='leftrefbox'><b>Requires</b>"
                    for ii,rr in required_courses.iterrows(): 
                        ht+="<br/>"+str(rr["course_id"])+"-<a href=\""+rr["course_url"]+"\" target=\"_blank\">"+rr["course_title"]+"</a>"
                    ht+="</div>"
                        
                references_courses=dfcc[dfcc["src_course_id"].isin([r["course_id"]]) & ~dfcc["relation"].isin(["requires"]) & ~dfcc["tgt_course_id"].isin([r["course_id"]]) & ~dfcc["tgt_course_id"].isin(required_courses.tgt_course_id.values)].merge(dfc,left_on="tgt_course_id",right_on="course_id",how="left").dropna(subset=["course_id"])
                if(len(references_courses)>0):
                    ht+="<div class='leftrefbox'><b>References</b>"
                    for ii,rr in references_courses.iterrows(): 
                        ht+="<br/>"+str(rr["course_id"])+"-<a href=\""+rr["course_url"]+"\" target=\"_blank\">"+rr["course_title"]+"</a>"
                    ht+="</div>"

                required_courses=dfcc[dfcc["tgt_course_id"].isin([r["course_id"]]) & dfcc["relation"].isin(["requires"]) & ~dfcc["src_course_id"].isin([r["course_id"]]) ].merge(dfc,left_on="src_course_id",right_on="course_id",how="left").dropna(subset=["course_id"])
                if(len(required_courses)>0 or r["layer"]==0):
                    ht+="<div class='rightrefbox'><b>Required by</b>"
                    if r["layer"]==0:
                        ht+="<br/> Project "+str(nn["project_number"])
                    for ii,rr in required_courses.iterrows(): 
                        ht+="<br/>"+str(rr["course_id"])+"-<a href=\""+rr["course_url"]+"\" target=\"_blank\">"+rr["course_title"]+"</a>"
                    ht+="</div>"                
                        
                references_courses=dfcc[dfcc["tgt_course_id"].isin([r["course_id"]]) & ~dfcc["relation"].isin(["requires"]) & ~dfcc["src_course_id"].isin([r["course_id"]]) & ~dfcc["src_course_id"].isin(required_courses.src_course_id.values)].merge(dfc,left_on="src_course_id",right_on="course_id",how="left").dropna(subset=["course_id"])
                if(len(references_courses)>0):
                    ht+="<div class='rightrefbox'><b>Referenced by</b>"
                    for ii,rr in references_courses.iterrows(): 
                        ht+="<br/>"+str(rr["course_id"])+"-<a href=\""+rr["course_url"]+"\" target=\"_blank\">"+rr["course_title"]+"</a>"
                    ht+="</div>"   
                ht+="</td>"
                # ---------------
                ht+="</tr>"
            #end course loop
            ht+="</tbody>"
            courses_exclusion_set = courses_exclusion_set | set(dfc.course_id.values)
        #end if there are courses to schedule 
        else: 
            ht+="<table>"
        #end if there are no courses
        # --------------- Totals
        ht+="<thead><tr>"
        ht+="<th colspan=3>Project #"+str(nn["project_number"])+"</th><th>courses</th><th>courses duration</th><th>project duration</th><th>percent</th>"
        ht+="</tr>"
        if (project_courses_unbooked>0):
            ht+="<tr>"
            ht+="<td colspan='3' class='noborder'></td><td  class='border'>"+str(project_courses_unbooked)+" unbooked</td><td class='border'>"+str(project_scheduled_unbooked_duration)+" h</td><td colspan=2 class='noborder'></td>"
            ht+="</tr>"
        if (project_courses_booked>0):
            ht+="<tr>"
            ht+="<td colspan='3' class='noborder'></td><td class='border'>"+str(project_courses_booked)+" booked</td><td class='border'>"+str(project_scheduled_booked_duration)+" h</td><td colspan=2 class='noborder'></td>"
            ht+="</tr>"
        if (project_courses_in_progress>0):
            ht+="<tr>"
            ht+="<td colspan='3' class='noborder'></td><td class='border'>"+str(project_courses_in_progress)+" in progress</td><td class='border'>"+str(project_scheduled_in_progress_duration)+" h</td><td colspan=2 class='noborder'></td>"
            ht+="</tr>"
        if (project_courses_done>0):
            ht+="<tr>"
            ht+="<td colspan='3' class='noborder'></td><td class='border'>"+str(project_courses_done)+" achieved</td><td class='border'>"+str(project_scheduled_done_duration)+" h</td><td colspan=2 class='noborder'></td>"
            ht+="</tr>" 
        ht+="<tr>"
        ht+="<td colspan=3 class='noborder'></td>"
        ht+="<th>"+str(project_courses_count)+" courses<br/>incl "+str(project_courses_critical_count)+" critical courses</th>"
        ht+="<th>"+str(project_scheduled_duration)+" h<br/>"+str(project_scheduled_critical_duration)+" h</th>"
        ht+="<th>"+str(project_allocated_duration)+" h</th>"
        ht+="<th>"+str(int(100*project_scheduled_duration/project_allocated_duration))+"%<br/>"+str(int(100*project_scheduled_critical_duration/project_allocated_duration))+" %</th>"
        ht+="</tr></thead>"
        ht+="</table>"
        total_allocated_duration += project_allocated_duration
        total_scheduled_duration += project_scheduled_duration
        total_courses_critical_count+=project_courses_critical_count
        total_scheduled_critical_duration+=project_scheduled_critical_duration
        total_courses_count+=project_courses_count
        total_scheduled_unbooked_duration+=project_scheduled_unbooked_duration
        total_courses_unbooked+=project_courses_unbooked
        total_scheduled_booked_duration+=project_scheduled_booked_duration
        total_courses_booked+=project_courses_booked
        total_scheduled_in_progress_duration+=project_scheduled_in_progress_duration
        total_courses_in_progress+=project_courses_in_progress
        total_scheduled_done_duration+=project_scheduled_done_duration
        total_courses_done+=project_courses_done
    # end loop on projects    
    
    ht+="<br/>"
    ht+="<br/>"
    ht+="<h2>Summary for "+str(len(dfpr))+" projects</h2>"
    ht+="<table><thead>"
    ht+="<tr>"
    ht+="<th>courses</th><th>scheduled courses duration</th><th>allocated projects duration</th><th>percent</th>"
    ht+="</tr>"
    if (total_courses_unbooked>0):
        ht+="<tr>"
        ht+="<td class='border'>"+str(total_courses_unbooked)+" unbooked</td><td class='border'>"+str(total_scheduled_unbooked_duration)+" h</td><td colspan=2 class='noborder'></td>"
        ht+="</tr>"
    if (total_courses_booked>0):
        ht+="<tr>"
        ht+="<td class='border'>"+str(total_courses_booked)+" booked</td><td class='border'>"+str(total_scheduled_booked_duration)+" h</td><td colspan=2 class='noborder'></td>"
        ht+="</tr>"
    if (total_courses_in_progress>0):
        ht+="<tr>"
        ht+="<td class='border'>"+str(total_courses_in_progress)+" in progress</td><td class='border'>"+str(total_scheduled_in_progress_duration)+" h</td><td colspan=2 class='noborder'></td>"
        ht+="</tr>"
    if (total_courses_done>0):
        ht+="<tr>"
        ht+="<td class='border'>"+str(total_courses_done)+" achieved</td><td class='border'>"+str(total_scheduled_done_duration)+" h</td><td colspan=2 class='noborder'></td>"
        ht+="</tr>"   
    ht+="<tr>"
    ht+="<th>"+str(total_courses_count)+" courses<br/>incl "+str(total_courses_critical_count)+" critical courses</th>"
    ht+="<th>"+str(total_scheduled_duration)+" h<br/>"+str(total_scheduled_critical_duration)+" h</th>"
    ht+="<th>"+str(total_allocated_duration)+" h</th>"
    ht+="<th>"+str(int(100*total_scheduled_duration/total_allocated_duration))+"%<br/>"+str(int(100*total_scheduled_critical_duration/total_allocated_duration))+" %</th>"
    ht+="</tr></thead>"
    ht+="</table>"
    ht+="<br/>"
    ht+="<br/>"
    # ------------- Finish
    return get_agenda_html_page(ht)
# end function