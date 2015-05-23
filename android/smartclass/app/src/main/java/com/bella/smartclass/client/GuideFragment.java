package com.bella.smartclass.client;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.bella.smartclass.R;

public class GuideFragment extends Fragment {
	private int type;
	View rootView;
	
	
	public GuideFragment() {		
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		rootView = inflater.inflate(R.layout.fragment_guide,
				container, false);
		
		findViews(rootView);
		showResults();
		setListensers();
		return rootView;
	}
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    type = getArguments().getInt("KEY_TYPE");
	}
	
	private void findViews(View rootView)
	{		
	}
	private void showResults() 
	{
		switch(type)
		{
		case 1:
			rootView.setBackgroundResource(R.color.gray);
			break;
		case 2:
			rootView.setBackgroundResource(R.color.yellow);
			break;
		case 0:
		default:
			rootView.setBackgroundResource(R.color.purple);
		}
	}	
	
	 private void setListensers() {
	 }
}
