package com.bella.smartclass.client;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.bella.smartclass.R;
import com.bella.smartclass.util.ResultObjects.AllCourseObject;

public class LoginActivity extends ActionBarActivity {
	
	Button registerButton;
	Button loginButton;
	Button forgetPasswordButton;
	
	EditText username;
	EditText password;
	
  
    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        findViews();
        setListeners();
    } 
    
    private void findViews(){
    	registerButton = (Button)findViewById(R.id.register_user_button);
    	loginButton = (Button)findViewById(R.id.login_user_button);
    	username = (EditText)findViewById(R.id.login_username);
    	password = (EditText)findViewById(R.id.login_password);
    }
    
    private void setListeners(){
		loginButton.setOnClickListener(loginListener);
		//forgetPasswordButton.setOnClickListener(forgetPasswordListener);
    }
	 
	 private Button.OnClickListener loginListener = new Button.OnClickListener()
	 {
		  public void onClick(View v)
		 {
			  String name = username.getText().toString();
			  String pw = password.getText().toString();
			  Intent intent = new Intent();
			  intent.setClass(LoginActivity.this, MainActivity.class);
			  startActivity(intent);
             AllCourseObject object = new AllCourseObject();
             object.getMessage();
		 }
	 };
	 
	 private Button.OnClickListener forgetPasswordListener = new Button.OnClickListener()
	 {
		  public void onClick(View v)
		 {

		 }
	 };
}  