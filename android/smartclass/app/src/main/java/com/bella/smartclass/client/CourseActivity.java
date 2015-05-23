package com.bella.smartclass.client;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.bella.smartclass.R;

public class CourseActivity extends ActionBarActivity{
	ActionBar actionBar;
	LinearLayout mainLayout;
    LinearLayout askQuestion, projectList, testList;
    TextView courseName, courseIntro;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_course);
        actionBar = getSupportActionBar();
        actionBar.setDisplayHomeAsUpEnabled(true);
		findViews();
		setListeners();
        fakeData();
	}
	
	private void findViews(){
        mainLayout = (LinearLayout) findViewById(R.id.main_content);
        askQuestion = (LinearLayout) findViewById(R.id.ask_question);
        projectList = (LinearLayout) findViewById(R.id.project_list);
        testList = (LinearLayout) findViewById(R.id.test_list);
        courseName = (TextView) findViewById(R.id.course_name);
        courseIntro = (TextView) findViewById(R.id.course_introduction);
	}
	
	private void setListeners(){
        askQuestion.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {
                startActivity(new Intent(CourseActivity.this, AskQuestionActivity.class));
            }
        });
        projectList.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {
                startActivity(new Intent(CourseActivity.this, ProjectListActivity.class));
            }
        });
        testList.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {
                startActivity(new Intent(CourseActivity.this, TestListActivity.class));
            }
        });
    }

    private void fakeData() {
        courseName.setText("Computer Networking");
        courseIntro.setText("This is test test test test test test test test test test test test test test.");
    }
}