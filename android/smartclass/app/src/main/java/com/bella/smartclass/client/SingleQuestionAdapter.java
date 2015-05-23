package com.bella.smartclass.client;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.SimpleAdapter;
import android.widget.TextView;

import com.bella.smartclass.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;



public class SingleQuestionAdapter extends SimpleAdapter {
    ArrayList<String> results;
    boolean[] extended;
    String[] checkedOption;
    public SingleQuestionAdapter(Context context, List<HashMap<String, Object>> items, int resource, String[] from, int[] to, ArrayList<String> results) {
        super(context, items, resource, from, to);
        this.results = results;
        extended = new boolean[items.size()];
        checkedOption = new String[items.size()];
    }


    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        convertView = null;
        convertView = super.getView(position, convertView, parent);

        final TextView title = (TextView) convertView.findViewById(R.id.title);
        final RadioGroup options = (RadioGroup) convertView.findViewById(R.id.options);
        final RadioButton option_A = (RadioButton) convertView.findViewById(R.id.option_A);
        final RadioButton option_B = (RadioButton) convertView.findViewById(R.id.option_B);
        final RadioButton option_C = (RadioButton) convertView.findViewById(R.id.option_C);
        final RadioButton option_D = (RadioButton) convertView.findViewById(R.id.option_D);

        title.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(extended[position]) {
                    extended[position] = false;
                    option_A.setVisibility(View.GONE);
                    option_B.setVisibility(View.GONE);
                    option_C.setVisibility(View.GONE);
                    option_D.setVisibility(View.GONE);
                }else{
                    extended[position] = true;
                    option_A.setVisibility(View.VISIBLE);
                    option_B.setVisibility(View.VISIBLE);
                    option_C.setVisibility(View.VISIBLE);
                    option_D.setVisibility(View.VISIBLE);
                }
            }
        });

        options.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener(){
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                if(checkedId ==  option_A.getId())
                    checkedOption[position] = "A";
                else if(checkedId ==  option_B.getId())
                    checkedOption[position] = "B";
                else if(checkedId ==  option_C.getId())
                    checkedOption[position] = "C";
                else if(checkedId ==  option_D.getId())
                    checkedOption[position] = "D";
            }
        });

        convertView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });
        return convertView;
    }
};