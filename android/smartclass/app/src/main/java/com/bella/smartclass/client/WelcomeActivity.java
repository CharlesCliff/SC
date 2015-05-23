package com.bella.smartclass.client;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.Window;

import com.bella.smartclass.R;

public class WelcomeActivity extends Activity {  
  
    private final int WELCOME_DISPLAY_LENGHT = 3000;
  
    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState);  
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_welcome);
  
        new Handler().postDelayed(new Runnable() {  
            public void run() {  
                Intent mainIntent = new Intent(WelcomeActivity.this,  
                        GuideActivity.class);
                WelcomeActivity.this.startActivity(mainIntent);  
                WelcomeActivity.this.finish();  
            }  
  
        }, WELCOME_DISPLAY_LENGHT);  
  
    }  
}  