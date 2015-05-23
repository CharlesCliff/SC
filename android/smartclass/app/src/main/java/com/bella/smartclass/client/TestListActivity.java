package com.bella.smartclass.client;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import com.bella.smartclass.R;
import com.bella.smartclass.client.component.RateTextCircularProgressBar;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class TestListActivity extends ActionBarActivity implements  SwipeRefreshLayout.OnRefreshListener{

    private ListView testList;
    SwipeRefreshLayout testListContainer;
    SimpleAdapter sa;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test_list);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        findViews();
        setListeners();
        fakeData();
    }

    private void findViews() {
        testList = (ListView) findViewById(R.id.test_list);
        testListContainer = (SwipeRefreshLayout) findViewById(R.id.test_list_container);
        testListContainer.setColorScheme(android.R.color.holo_blue_light,
                R.color.red,
                android.R.color.holo_orange_light, R.color.red);
    }

    private void setListeners() {
        testListContainer.setOnRefreshListener(this);
    }

    private void fakeData() {
        List<HashMap<String, Object>> data = new ArrayList<HashMap<String, Object>>();

        for (int i = 0; i < 5; i++) {
            HashMap<String, Object> item = new HashMap<String, Object>();
            item.put("name", "test " + i);
            item.put("finish_time", "2015/6/19");
            data.add(item);
        }

        sa = new OnClickAdapter(this, data, R.layout.test_item, new String[]{"name", "finish_time"}, new int[]{R.id.test_name, R.id.finish_time});
        testList.setAdapter(sa);
    }

    @Override
    public void onRefresh() {
        if (testListContainer.isRefreshing()) {
            new Handler().postDelayed(new Runnable() {
                public void run() {
                    testListContainer.setRefreshing(false);
                    //Toast.makeText(ProjectListActivity.this, "refresh", Toast.LENGTH_SHORT);
                    sa.notifyDataSetChanged();
                }
            }, 1000);

        }
    }

    private class OnClickAdapter extends SimpleAdapter {
        public OnClickAdapter(Context context, List<HashMap<String, Object>> items, int resource, String[] from, int[] to) {
            super(context, items, resource, from, to);
        }


        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            convertView = null;
            convertView = super.getView(position, convertView, parent);

            RateTextCircularProgressBar progressBar;
            progressBar = (RateTextCircularProgressBar) convertView.findViewById(R.id.progress_bar);
            progressBar.setTextColor(getResources().getColor(R.color.red));
            progressBar.getCircularProgressBar().setPrimaryColor(getResources().getColor(R.color.red));
            progressBar.setTextSize(15);
            progressBar.setMax(100);
            progressBar.setProgress(70);

            convertView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(TestListActivity.this, QuestionListActivity.class);
                    startActivity(intent);
                }
            });
            return convertView;
        }
    };
}


