package com.example.scorescanner;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.FileProvider;

import android.Manifest;
import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.provider.MediaStore;
import android.util.ArrayMap;
import android.util.ArraySet;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.Buffer;
import java.sql.Time;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;
import java.util.zip.Inflater;

public class MainActivity extends AppCompatActivity {
    Set<String> uuidList = new ArraySet<>();
    ArrayList<ArrayList<String>> HistoryList = new ArrayList<>();
    String projectName = "";
    String currentPhotoPath;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        SharedPreferences preferences = getSharedPreferences("uuidList", MODE_PRIVATE);
        uuidList = preferences.getStringSet("uuids",new ArraySet<>());

        ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.CAMERA },0);
        ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.INTERNET },0);


        Intent intent = getIntent();
        if(intent != null){
            Bundle b = intent.getExtras();
            if(b != null){
                String uuid = b.getString("html");
                String name = b.getString("name");
                String html = "http://10.0.13.214:5000/api/get/scoreTable/" + uuid;
                uuidList.add(uuid);
                Date date = new Date();
                SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
                preferences.edit()
                        .putStringSet("uuids", uuidList)
                        .putString(uuid+"Name", name)
                        .putString(uuid+"Time", formatter.format(date))
                        .apply();
                new AlertDialog.Builder(this)
                        .setTitle(html)
                        .setPositiveButton("Copy", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                                ClipData clip = ClipData.newPlainText("Score",html);
                                clipboard.setPrimaryClip(clip);
                            }
                        })
                        .setNegativeButton("Open", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(html));
                                startActivity(browserIntent);
                            }
                        })
                        .setNeutralButton("Leave", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {

                            }
                        }).create().show();
                int z = 0;
                z = 1;
            }
        }
        findViewById(R.id.NewProject).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LayoutInflater inflater = (LayoutInflater)getSystemService(LAYOUT_INFLATER_SERVICE);
                View view = inflater.inflate(R.layout.input_dialog, null);
                AlertDialog alertDialog = new AlertDialog.Builder(v.getContext())
                        .setView(view)
                        .setPositiveButton("Create", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                projectName = ((EditText)view.findViewById(R.id.ProjectName)).getText().toString();
                                Intent intent1 = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                                Uri photoURI = null;
                                try {
                                    photoURI = FileProvider.getUriForFile(MainActivity.this ,
                                            "com.example.scorescanner.fileprovider",
                                            createImageFile());
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                                intent1.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                                startActivityForResult(intent1,0);
                            }
                        })
                        .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {

                            }
                        })
                        .create();
                alertDialog.show();
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        SharedPreferences preferences = getSharedPreferences("uuidList", MODE_PRIVATE);
        HistoryList.clear();
        String[] sr = new String[]{"國文第二課大卷","數學排列組合小考","電子學二極體複習","英文第三課單字"};
        int i = 0;
        for (String uuid : uuidList) {
            ArrayList arrayList = new ArrayList();
            arrayList.add(uuid);
            arrayList.add(sr[i]);
//            arrayList.add(preferences.getString(uuid + "Name", ""));
            arrayList.add(preferences.getString(uuid + "Time", ""));
            HistoryList.add(arrayList);
            i++;
        }
        HistoryList = HistoryList.stream().sorted(Comparator.comparing(x->x.get(2))).collect(Collectors.toCollection(ArrayList::new));
        ((ListView) findViewById(R.id.HistoryList)).setAdapter(new LenfAdapter(getBaseContext(), HistoryList));
        ((ListView)findViewById(R.id.HistoryList)).setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String html = "http://10.0.13.214:5000/api/get/scoreTable/" + HistoryList.get(position).get(0);
                new AlertDialog.Builder(view.getContext())
                        .setTitle(html)
                        .setPositiveButton("Copy", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                                ClipData clip = ClipData.newPlainText("Score",html);
                                clipboard.setPrimaryClip(clip);
                            }
                        })
                        .setNegativeButton("Open", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(html));
                                startActivity(browserIntent);
                            }
                        })
                        .setNeutralButton("Leave", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {

                            }
                        }).create().show();
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(resultCode == -1 && requestCode == 0){
            try {
                FileInputStream fileInputStream = new FileInputStream(new File(currentPhotoPath));
                BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                int len = 0;
                byte[] buffer = new byte[1024];
                while ((len = bufferedInputStream.read(buffer))!=-1){
                    out.write(buffer,0,len);
                }

                JSONObject result = new JSONObject(new PostTask(out.toByteArray()).execute().get());
                Intent intent = new Intent(getBaseContext(),waitingActivity.class);
                intent.putExtra("uuid",result.getString("uuid"));
                intent.putExtra("name",projectName);
                startActivity(intent);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(imageFileName,".jpg", storageDir);
        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

    public static class PostTask extends AsyncTask<String,Void,String> {
        byte[] json;
        public PostTask(byte[] _json) {
            json = _json;
        }
        @Override
        protected String doInBackground(String... strings) {
            HttpURLConnection conn = null;
            String result = "";
            try {

                String lineEnd = "\r\n";
                String twoHyphens = "--";
                String boundary = "*****";
                conn = (HttpURLConnection) new URL("http://10.0.13.214:5000/api/upload/scoreTable").openConnection();
                conn.setConnectTimeout(10000);
                conn.setReadTimeout(15000);
                conn.setRequestMethod("POST");
                conn.setDoInput(true);
                conn.setDoOutput(true);
                conn.setUseCaches(false);
                conn.setInstanceFollowRedirects(true);
                conn.setRequestProperty("Content-Length", String.valueOf((json.length + 117)));
                conn.setRequestProperty("Accept-Encoding","gzip, deflate, br");
                conn.setRequestProperty("Connection", "Keep-Alive");
                conn.setRequestProperty("Content-Type","multipart/form-data; boundary=" + boundary);
                conn.connect();

                DataOutputStream dos = new DataOutputStream(conn.getOutputStream());
                dos.writeBytes(twoHyphens + boundary + lineEnd);
                dos.writeBytes("Content-Disposition: form-data; name=\"img\";filename=\"" + "imageAddress" +"\"" + lineEnd);
                dos.writeBytes("Content-Type: image/png" + lineEnd);
                dos.writeBytes(lineEnd);
                dos.write(json);
                dos.writeBytes(lineEnd);
                dos.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);
                dos.flush();
                dos.close();

                int code = conn.getResponseCode();

                if(code==HttpURLConnection.HTTP_OK){
                    InputStream in = conn.getInputStream();
                    BufferedReader br = new BufferedReader(new InputStreamReader(in));
                    String str = null;
                    while((str = br.readLine())!=null){
                        result += str;
                    }
                    in.close();
                    br.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
                Log.d("ice",e.toString());
            } finally {
                conn.disconnect();
            }
            return result;
        }
    }

    class LenfAdapter extends BaseAdapter{
        LayoutInflater layoutInflater;
        ArrayList<ArrayList<String>> arrayList;
        public LenfAdapter(Context context, ArrayList<ArrayList<String>> _arrayList) {
            super();
            layoutInflater = (LayoutInflater)context.getSystemService(LAYOUT_INFLATER_SERVICE);
            arrayList = _arrayList;
        }

        @Override
        public int getCount() {
            return arrayList.size();
        }

        @Override
        public Object getItem(int position) {
            return arrayList.get(position);
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View v = layoutInflater.inflate(R.layout.history_list_layout, parent, false);
            ((TextView)v.findViewById(R.id.uuidText)).setText(arrayList.get(position).get(0));
            ((TextView)v.findViewById(R.id.NameText)).setText(arrayList.get(position).get(1));
            ((TextView)v.findViewById(R.id.TimeText)).setText(arrayList.get(position).get(2));
            return v;
        }
    }
}