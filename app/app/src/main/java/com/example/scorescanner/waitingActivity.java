package com.example.scorescanner;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class waitingActivity extends AppCompatActivity {
    String uuid;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.waiting_layout);
        uuid = getIntent().getExtras().getString("uuid");
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent intent = new Intent(getBaseContext(), MainActivity.class);
                intent.putExtra("html", uuid);
                intent.putExtra("name",getIntent().getExtras().getString("name"));
                startActivity(intent);
            }
        },10000);
    }
//    public Thread thread = new Thread(new Runnable() {
//        @Override
//        public void run() {
//            HttpURLConnection conn = null;
//            String strHTML = "";
//            try {
//                conn = (HttpURLConnection) new URL().openConnection();
//                conn.setConnectTimeout(10000);
//                conn.setReadTimeout(15000);
//                conn.setRequestMethod("GET");
//                conn.setDoInput(true);
//                conn.setDoOutput(false);
//                conn.connect();
//                InputStream in = conn.getInputStream();
//                BufferedReader br = new BufferedReader(new InputStreamReader(in));
//                String str = null;
//                while((str = br.readLine())!=null){
//                    strHTML += str;
//                }
//                JSONObject jsonObject = new JSONObject(strHTML);
//                jsonObject.getString("msg");
//            } catch (IOException | JSONException e) {
//                e.printStackTrace();
//            }
//        }
//    });
}
