package com.bella.smartclass.client;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.text.InputType;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.bella.smartclass.R;

public class RegisterActivity extends ActionBarActivity {
	
	Button registerButton;
	
	EditText username;
	EditText password;
	EditText passwordAgain;
  
    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        findViews();
        setListeners();
    } 
    
    private void findViews(){
    	registerButton = (Button)findViewById(R.id.register_user_button);
    	username = (EditText)findViewById(R.id.register_username);
    	password = (EditText)findViewById(R.id.register_password);
    	passwordAgain = (EditText)findViewById(R.id.register_password_again);
    }
    
    private void setListeners(){
    	registerButton.setOnClickListener(registerListener);
		password.setOnTouchListener(passwordListener);
		passwordAgain.setOnTouchListener(passwordListener);
    }
    
    private Button.OnClickListener registerListener = new Button.OnClickListener()
	 {
		  public void onClick(View v)
		 {
			  String name = username.getText().toString();
			  String pw = password.getText().toString();
			  String pw2 = passwordAgain.getText().toString();
			  Intent intent = new Intent();
			  intent.setClass(RegisterActivity.this, MainActivity.class);
			  startActivity(intent);
		 }
	 };
	 
	 private EditText.OnTouchListener passwordListener = new EditText.OnTouchListener()
	 {
		@Override
		public boolean onTouch(View v, MotionEvent event) {
			((EditText)v).setText("");
			((EditText)v).setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
			return false;
		}
	 }; 

}  