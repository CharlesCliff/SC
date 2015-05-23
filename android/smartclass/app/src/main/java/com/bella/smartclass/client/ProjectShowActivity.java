package com.bella.smartclass.client;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.widget.TextView;

import com.bella.smartclass.R;

public class ProjectShowActivity extends ActionBarActivity {
    TextView projectTitle, teamMate, position, finishTime;
    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState); 
        setContentView(R.layout.activity_project_show);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        findViews();
        setListeners();
        fakeData();
    }

    private void findViews(){
        projectTitle = (TextView) findViewById(R.id.project_title);
        teamMate = (TextView) findViewById(R.id.teammate);
        position = (TextView) findViewById(R.id.position);
        finishTime = (TextView) findViewById(R.id.finish_time);
    }

    private void setListeners(){

    }

    private void fakeData(){
        projectTitle.setText(getResources().getString(R.string.your_project_title) + "project1");
        teamMate.setText(getResources().getString(R.string.your_teammate) + "XX， XXX和XXX");
        position.setText(getResources().getString(R.string.your_position) + "队长");
        finishTime.setText(getResources().getString(R.string.your_finish_time) + "2015-6-19");
    }
}  