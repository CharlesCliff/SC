package com.bella.smartclass.util;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.util.Log;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Bella on 2015/4/22.
 */
public class NetworkLinker {
    boolean upload = false;        //上传还是下载
    URL url = null;
    List<NameValuePair> postParameters = null;
    HttpClient client = null;
    HttpPost request = null;
    HttpResponse response = null;
    String strResult = null;

    public NetworkLinker(boolean mUpload){
        upload = mUpload;
        init();
    }

    public void init(){
        try {
            url = new URL(Constants.BaseUrl);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        client = new DefaultHttpClient();
        request = new HttpPost(Constants.BaseUrl);
        postParameters = new ArrayList<NameValuePair>();
    }

    public void addParams(String name, String param){
        postParameters.add(new BasicNameValuePair(name, param));
    }

    public String execute(){
        UrlEncodedFormEntity formEntity = null;
        try {
            formEntity = new UrlEncodedFormEntity(postParameters);
            request.setEntity(formEntity);
            response = client.execute(request);
            if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK){
                strResult = EntityUtils.toString(response.getEntity());
                return strResult;
            }else{
                return null;
            }
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }  catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static boolean ifNetworkLinked(Context context){
        try {
            ConnectivityManager connectivity = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
            if (connectivity != null) {
                // 获取网络连接管理的对象
                NetworkInfo info = connectivity.getActiveNetworkInfo();
                if (info != null&& info.isConnected()) {
                    // 判断当前网络是否已经连接
                    if (info.getState() == NetworkInfo.State.CONNECTED) {
                        return true;
                    }
                }
            }
        } catch (Exception e) {
            Log.v("error", e.toString());
        }
        return false;
    }
}
