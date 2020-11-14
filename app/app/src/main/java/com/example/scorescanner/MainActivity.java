package com.example.scorescanner;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.PagerAdapter;
import androidx.viewpager.widget.ViewPager;

import android.net.wifi.hotspot2.pps.HomeSp;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.material.tabs.TabLayout;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        View Home = getLayoutInflater().inflate(R.layout.home_layout,null);
        View Score = getLayoutInflater().inflate(R.layout.score_layout,null);

        List<View> pages = new ArrayList<View>(Arrays.asList(Home,Score));

        ((ViewPager)findViewById(R.id.viewpager)).setAdapter(new LenfViewPager(pages));
        ((TabLayout)findViewById(R.id.TabLayout)).setupWithViewPager(((ViewPager)findViewById(R.id.viewpager)));
    }
    public class LenfViewPager extends PagerAdapter{
        List<View> mlist;
        public LenfViewPager(List<View> list) {
            super();
            mlist = list;
        }

        @Nullable
        @Override
        public CharSequence getPageTitle(int position) {
            switch (position) {
                case 0:
                    return "Home";
                case 1:
                    return "Score Sheet";
                case 2:
                    return "Answer Card";
            }
            return null;
        }

        @Override
        public void destroyItem(@NonNull ViewGroup container, int position, @NonNull Object object) {
            if(mlist.get(position)!=null)
                container.removeView(mlist.get(position));
        }
        @NonNull
        @Override
        public Object instantiateItem(@NonNull ViewGroup container, int position) {
            container.addView(mlist.get(position));
            return mlist.get(position);
        }

        @Override
        public int getCount() {
            return mlist.size();
        }

        @Override
        public boolean isViewFromObject(@NonNull View view, @NonNull Object object) {
            return view == object;
        }
    }
}