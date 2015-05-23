package com.bella.smartclass.util.ResultObjects;

/**
 * Created by a on 2015/4/23.
 */
public class AllProjectObject extends ResultObject{
    private String[] projectList;
    private String[] studentList;

    public String[] getProjectList() {
        return projectList;
    }

    public void setProjectList(String[] projectList) {
        this.projectList = projectList;
    }

    public String[] getStudentList() {
        return studentList;
    }

    public void setStudentList(String[] studentList) {
        this.studentList = studentList;
    }
}
