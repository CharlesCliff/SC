package com.bella.smartclass.client;

import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import com.bella.smartclass.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class MainActivity extends ActionBarActivity {

    private DrawerLayout mDrawerLayout;
    private ActionBarDrawerToggle mDrawerToggle;
    LinearLayout leftDrawer;
    ListView myCourseList;
    ActionBar actionBar;
    OnClickAdapter sa;
    LinearLayout aboutUs, notifyCenter, logOut, personalInfo, addCourse;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        actionBar = getSupportActionBar();
        actionBar.setDisplayHomeAsUpEnabled(true);
        findViews();
        setListeners();
        fakeData();
    }

    private void findViews(){
        myCourseList = (ListView) findViewById(R.id.course_list);
        mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
        mDrawerLayout.setDrawerShadow(R.drawable.drawer_shadow, GravityCompat.START);
        leftDrawer = (LinearLayout) findViewById(R.id.left_drawer);

        mDrawerToggle = new ActionBarDrawerToggle(
                this,                  /* host Activity */
                mDrawerLayout,         /* DrawerLayout object */
                R.drawable.ic_drawer,  /* nav drawer image to replace 'Up' caret */
                R.string.personal_setting,  /* "open drawer" description for accessibility */
                R.string.my_course  /* "close drawer" description for accessibility */
        ) {
            public void onDrawerClosed(View view) {
                actionBar.setTitle(R.string.my_course);
                invalidateOptionsMenu(); // creates call to onPrepareOptionsMenu()
            }

            public void onDrawerOpened(View drawerView) {
                actionBar.setTitle(R.string.personal_setting);
                invalidateOptionsMenu(); // creates call to onPrepareOptionsMenu()
            }
        };
        mDrawerLayout.setDrawerListener(mDrawerToggle);

        aboutUs = (LinearLayout) findViewById(R.id.about_us);
        notifyCenter = (LinearLayout) findViewById(R.id.notify_center);
        logOut = (LinearLayout) findViewById(R.id.log_out);
        personalInfo = (LinearLayout) findViewById(R.id.personal_info);
        addCourse = (LinearLayout) findViewById(R.id.add_course);
    }



    private void setListeners(){
        aboutUs.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, AboutUsActivity.class);
                startActivity(intent);
            }
        });
        notifyCenter.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {

            }
        });
        logOut.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {

            }
        });
        personalInfo.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, PersonalInfoActivity.class));
            }
        });
        addCourse.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {

            }
        });
    }

    private void fakeData() {
        List<HashMap<String, Object>> data = new ArrayList<HashMap<String, Object>>();

        for (int i = 0; i < 5; i++) {
            HashMap<String, Object> item = new HashMap<String, Object>();
            item.put("name", "Course " + i);
            item.put("intro", "This course aims to tell you how can you write an android app.");
            data.add(item);
        }

        sa = new OnClickAdapter(this, data, R.layout.course_item, new String[]{"name", "intro"}, new int[]{R.id.course_name, R.id.course_introduction});
        myCourseList.setAdapter(sa);
    }

    public void onClick(View v, int position){
        mDrawerLayout.closeDrawer(leftDrawer);
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState) {
        super.onPostCreate(savedInstanceState);
        // Sync the toggle state after onRestoreInstanceState has occurred.
        mDrawerToggle.syncState();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        // Pass any configuration change to the drawer toggls
        mDrawerToggle.onConfigurationChanged(newConfig);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (mDrawerToggle.onOptionsItemSelected(item)) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private class OnClickAdapter extends SimpleAdapter {
        public OnClickAdapter(Context context, List<HashMap<String, Object>> items, int resource, String[] from, int[] to) {
            super(context, items, resource, from, to);
        }


        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            convertView = null;
            convertView = super.getView(position, convertView, parent);

            convertView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(MainActivity.this, CourseActivity.class);
                    startActivity(intent);
                }
            });
            return convertView;
        }
    };
}