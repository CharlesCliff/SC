package com.bella.smartclass.client;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;

import com.bella.smartclass.R;

public class AskQuestionActivity extends ActionBarActivity {
    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState); 
        setContentView(R.layout.activity_ask_question);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
    }  
}  