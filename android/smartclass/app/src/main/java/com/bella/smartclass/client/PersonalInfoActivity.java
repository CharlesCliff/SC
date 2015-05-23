package com.bella.smartclass.client;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.text.InputType;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;

import com.bella.smartclass.R;

public class PersonalInfoActivity extends ActionBarActivity {
    EditText inputName, telephone, mail;
    boolean editable = false;

    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState); 
        setContentView(R.layout.activity_personal_info);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        findViews();
        setListeners();
        fakeData();
    }

    private void findViews(){
        inputName = (EditText) findViewById(R.id.input_name);
        telephone = (EditText) findViewById(R.id.input_telephone);
        mail = (EditText) findViewById(R.id.input_mail);
    }

    private void setListeners(){

    }

    private void fakeData(){
        inputName.setText("XXX");
        telephone.setText("010-62576257");
        mail.setText("XXX@163.com");
        inputName.setInputType(InputType.TYPE_NULL);;
        telephone.setInputType(InputType.TYPE_NULL);;
        mail.setInputType(InputType.TYPE_NULL);;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.personal_info, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.edit) {
            if(!editable) {
                editable = true;
                inputName.setInputType(InputType.TYPE_CLASS_TEXT);
                telephone.setInputType(InputType.TYPE_CLASS_TEXT);
                mail.setInputType(InputType.TYPE_CLASS_TEXT);
                item.setTitle(R.string.save);
            }else{
                editable = false;
                inputName.setInputType(InputType.TYPE_NULL);
                telephone.setInputType(InputType.TYPE_NULL);
                mail.setInputType(InputType.TYPE_NULL);
                item.setTitle(R.string.edit_info);
                finish();
            }
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}