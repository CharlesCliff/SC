package com.bella.smartclass.client;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.view.View;
import android.view.Window;
import android.widget.Button;

import com.bella.smartclass.R;

public class GuideActivity extends FragmentActivity {

	SectionsPagerAdapter sectionsPagerAdapter;
	private static final int COUNT = 3;
	private boolean autoPlay = true;
	private Message message = new Message();
	private AutoPlayHandler autoPlayHandler = new AutoPlayHandler();

	ViewPager viewPager;
	Button registerButton;
	Button loginButton;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		this.requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.activity_guide);
		findViews();
		setListeners();
		//autoPlay();
	}

	private void findViews() {
		sectionsPagerAdapter = new SectionsPagerAdapter(
				getSupportFragmentManager());

		// Set up the ViewPager with the sections adapter.
		viewPager = (ViewPager) findViewById(R.id.viewpager);
		viewPager.setAdapter(sectionsPagerAdapter);
		registerButton = (Button) findViewById(R.id.guide_register_button);
		loginButton = (Button) findViewById(R.id.guide_login_button);
	}

	private void setListeners() {
		registerButton.setOnClickListener(registerListener);
		loginButton.setOnClickListener(loginListener);
	}

	private Button.OnClickListener registerListener = new Button.OnClickListener() {
		public void onClick(View v) {
			// Close this Activity
			Intent intent = new Intent();
			intent.setClass(GuideActivity.this, RegisterActivity.class);
			startActivity(intent);
			//finish();
		}
	};

	private Button.OnClickListener loginListener = new Button.OnClickListener() {
		public void onClick(View v) {
			Intent intent = new Intent();
			intent.setClass(GuideActivity.this, LoginActivity.class);
			startActivity(intent);
			//finish();
		}
	};

	// 自动播放
	private void autoPlay() {
		if (autoPlay == true){
			autoPlayHandler.sendMessageDelayed(message, 2000);// 延迟两秒发送消息
		}
	}

	class AutoPlayHandler extends Handler {
		@Override
		public void handleMessage(Message msg) {
			if (autoPlay == true) {
				viewPager.setCurrentItem((viewPager.getCurrentItem() + 1) % COUNT);
				//viewPager.setCurrentItem((viewPager.getCurrentItem() + 1));
				message = autoPlayHandler.obtainMessage(0);// 重新给message赋值，因为前一个message“还在使用中”
				sendMessageDelayed(message, 2000);
			}
		}
	}

	public class SectionsPagerAdapter extends FragmentPagerAdapter {
		Fragment fragmentOne, fragmentTwo, fragmentThree;
		Bundle argsOne, argsTwo, argsThree;
		int count;

		public SectionsPagerAdapter(FragmentManager fm) {
			super(fm);
			count = COUNT;
			fragmentOne = new GuideFragment();
			argsOne = new Bundle();
			argsOne.putInt("KEY_TYPE", 0);
			fragmentOne.setArguments(argsOne);
			fragmentTwo = new GuideFragment();
			argsTwo = new Bundle();
			argsTwo.putInt("KEY_TYPE", 1);
			fragmentTwo.setArguments(argsTwo);
			fragmentThree = new GuideFragment();
			argsThree = new Bundle();
			argsThree.putInt("KEY_TYPE", 2);
			fragmentThree.setArguments(argsThree);
		}

		@Override
		public Fragment getItem(int position) {
			int pos = position % COUNT;
			switch (pos) {
			case 0:
				return fragmentOne;
			case 1:
				return fragmentTwo;
			case 2:
				return fragmentThree;
			default:
				return fragmentOne;
			}
		}

		@Override
		public int getCount() {
			// Show 3 total pages but for loops.
			return 3;
		}
	}
}
