package com.bella.smartclass.client;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.bella.smartclass.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class ProjectMakeTeamActivity extends ActionBarActivity {

    private Spinner projectElector, projectElector2, projectElector3;
    private ArrayAdapter<String> spinnerAdapter = null;
    private Button confirmTeam;
    private boolean newTeamExtended = false, invitationsExtended = true;
    private LinearLayout newTeamLayout, newTeamExtendedButton, invitationsExtendedButton;
    private ListView invitations;
    private OnClickAdapter invitationAdapter;
    private TextView newTeamExtendedHint, invitationsExtendedHint;

    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState); 
        setContentView(R.layout.activity_project_make_team);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        findViews();
        setListeners();
        fakeData();
    }

    private void findViews(){
        projectElector = (Spinner) findViewById(R.id.project_elector);
        projectElector2 = (Spinner) findViewById(R.id.project_elector2);
        projectElector3 = (Spinner) findViewById(R.id.project_elector3);
        confirmTeam = (Button) findViewById(R.id.confirm_team);
        newTeamLayout = (LinearLayout) findViewById(R.id.make_team_content);
        invitations = (ListView) findViewById(R.id.invitations);
        newTeamExtendedButton = (LinearLayout) findViewById(R.id.make_team_extended_button);
        invitationsExtendedButton = (LinearLayout) findViewById(R.id.look_invitation);
        newTeamExtendedHint = (TextView) findViewById(R.id.new_team_extended_hint);
        invitationsExtendedHint = (TextView) findViewById(R.id.invitations_extended_hint);
    }

    private void setListeners(){
        projectElector.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1,
                                       int arg2, long arg3) {
                Toast.makeText(ProjectMakeTeamActivity.this, "你的第一选择是" + ((TextView)arg1).getText(),
                        Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {

            }
        });
        projectElector2.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1,
                                       int arg2, long arg3) {
                Toast.makeText(ProjectMakeTeamActivity.this, "你的第二选择是" + ((TextView)arg1).getText(),
                        Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {

            }
        });
        projectElector3.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1,
                                       int arg2, long arg3) {
                Toast.makeText(ProjectMakeTeamActivity.this, "你的第三选择是" + ((TextView)arg1).getText(),
                        Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {

            }
        });
        confirmTeam.setOnClickListener((new Button.OnClickListener(){
            @Override
            public void onClick(View v) {
                Toast.makeText(ProjectMakeTeamActivity.this, R.string.have_confirmed_team,
                        Toast.LENGTH_SHORT).show();
                startActivity(new Intent().setClass(ProjectMakeTeamActivity.this, ProjectShowActivity.class));
            }
        }));
        newTeamExtendedButton.setOnClickListener(new LinearLayout.OnClickListener() {
            @Override
            public void onClick(View v) {
                changeNewTeamExtended();
                changeInvitationsExtended();
            }
        });
        invitationsExtendedButton.setOnClickListener(new LinearLayout.OnClickListener(){
            @Override
            public void onClick(View v) {
                changeNewTeamExtended();
                changeInvitationsExtended();
            }
        });
    }

    private void fakeData(){
        String[] projects = {"project1", "project2", "project3", "project4", "project5"};
        spinnerAdapter = new ArrayAdapter<String>(this,android.R.layout.simple_spinner_item, projects);
        projectElector.setAdapter(spinnerAdapter);
        projectElector2.setAdapter(spinnerAdapter);
        projectElector3.setAdapter(spinnerAdapter);


        List<HashMap<String, Object>> data = new ArrayList<HashMap<String, Object>>();
        for(int i = 0; i < 3; i++){
            HashMap<String, Object> item = new HashMap<String, Object>();
            item.put("content", "XX邀请你加入队伍。队伍成员还有XX，XXX和XXX");
            data.add(item);
        }
        invitationAdapter = new OnClickAdapter(this, data, R.layout.invitation_item, new String[]{"content"}, new int[]{R.id.invitation_content});
        invitations.setAdapter(invitationAdapter);
    }

    private void changeNewTeamExtended(){
        if(newTeamExtended){
            newTeamExtended = false;
            newTeamLayout.setVisibility(View.GONE);
            newTeamExtendedHint.setText(R.string.start_team);
        }else{
            newTeamExtended = true;
            newTeamLayout.setVisibility(View.VISIBLE);
            newTeamExtendedHint.setText(R.string.fold_start_team);
        }
    }

    private void changeInvitationsExtended(){
        if(invitationsExtended){
            invitationsExtended = false;
            invitations.setVisibility(View.GONE);
            invitationsExtendedHint.setText(R.string.look_make_team_invitation);
        }else{
            invitationsExtended = true;
            invitations.setVisibility(View.VISIBLE);
            invitationsExtendedHint.setText(R.string.fold_invitation);
        }
    }

    class OnClickAdapter extends SimpleAdapter {
        public OnClickAdapter(Context context, List<HashMap<String, Object>> items, int resource, String[] from, int[] to) {
            super(context, items, resource, from, to);
        }


        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            convertView = null;
            convertView = super.getView(position, convertView, parent);

            Button agree = (Button) convertView.findViewById(R.id.confirm);
            agree.setOnClickListener(new Button.OnClickListener(){

                @Override
                public void onClick(View v) {
                }
            });
            return convertView;
        }
    };
}
