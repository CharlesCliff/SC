package com.bella.smartclass.client;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListView;

import com.bella.smartclass.R;

import java.util.ArrayList;
import java.util.HashMap;


public class QuestionListActivity extends ActionBarActivity{
	
	private ListView questionList;
	SingleQuestionAdapter adapter;
    ArrayList<String> results;
    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState); 
        setContentView(R.layout.activity_question_list);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        findViews();
        setListeners();
        fakeData();
    }  
    
    private void findViews(){
        questionList = (ListView) findViewById(R.id.question_list);
    }
    
    private void setListeners(){

    }
    
	private void fakeData() {
		ArrayList<HashMap<String, Object>> data = new ArrayList<HashMap<String, Object>>();

		for (int i = 0; i < 10; i++) {
			HashMap<String, Object> item = new HashMap<String, Object>();
			item.put("title", "question " + i);
            item.put("optionA", "option A");
            item.put("optionB", "option B");
            item.put("optionC", "option C");
            item.put("optionD", "option D");
			data.add(item);
		}

        adapter = new SingleQuestionAdapter(QuestionListActivity.this, data, R.layout.single_question_item,
                new String[]{"title", "optionA", "optionB", "optionC", "optionD"},
                new int[]{R.id.title, R.id.option_A, R.id.option_B, R.id.option_C, R.id.option_D}, results);

	    questionList.setAdapter(adapter);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.question_list, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.put_forward) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }


}  