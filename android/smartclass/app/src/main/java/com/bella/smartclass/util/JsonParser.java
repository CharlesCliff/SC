package com.bella.smartclass.util;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONTokener;

/**
 * Created by Bella on 2015/4/22.
 */
public class JsonParser {
    Constants.RequestType type;
    String inputString;
    JSONObject js;

    public JsonParser(Constants.RequestType mType, String mInputString){
        type = mType;
        inputString = mInputString;
        parse();
    }

    public void parse(){
        try {
            JSONTokener jsonParser = new JSONTokener(inputString);
            js = (JSONObject) jsonParser.nextValue();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public String getStringValue(String name){
        try {
            return js.getString(name);
        } catch (JSONException e) {
            return null;
        }
    }
}
