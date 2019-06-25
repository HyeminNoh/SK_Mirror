package com.example.mys.mirror;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Chronometer;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;


import java.util.ArrayList;
import java.util.List;

public class Hairmatch extends AppCompatActivity {

    ArrayList<String> ImageList;

    private DatabaseReference mDatabase;
    FirebaseAuth firebaseAuth;
    String name;
    GridView listView;
    EditText imgsearch_name;

    List<UserImageDTO> userImageDTOS= new ArrayList<>();

    Chronometer chronometer;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_hairmatch);
        setTitle("헤어매칭");

        //getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));

        firebaseAuth = firebaseAuth.getInstance();

        listView = (GridView) findViewById(R.id.hairmatch);
        imgsearch_name = (EditText) findViewById(R.id.imgsearch_name);

        ImageList = new ArrayList<String>();

        //DB초기화
        mDatabase = FirebaseDatabase.getInstance().getReference("baseimage");
        name = "memoAdapter";

        //DB객체 불러오기 및 리스트저장
        mDatabase.child("test").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                ImageList.clear();
                userImageDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    UserImageDTO userImageDTO = snapshot.getValue(UserImageDTO.class);
                    userImageDTOS.add(userImageDTO);
                    ImageList.add(userImageDTO.img_file);

                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

                Intent intent = new Intent(getApplicationContext(), Show_image.class);
                intent.putExtra("filename", ImageList.get(position));
                intent.putExtra("name",userImageDTOS.get(position).img_name);

                startActivity(intent);
            }
        });

            ImageAdapter test = new ImageAdapter(getApplicationContext(), R.layout.image_list, ImageList);

            listView.setAdapter(test);
    }



    class ImageAdapter extends BaseAdapter {
        Context context;
        int layout;
        ArrayList<String> img ;
        LayoutInflater inf;
        public ImageAdapter(Context context, int layout, ArrayList<String> tttt) {
            img = new ArrayList<String>();
            this.context = context;
            this.layout = layout;
            this.img = tttt;
            inf = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);

        }

        @Override
        public int getCount() {
            return img.size();
        }

        @Override
        public Object getItem(int position) {
            return img.get(position);
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if (convertView==null)
                convertView = inf.inflate(layout,null);

            ImageView iv = (ImageView)convertView.findViewById(R.id.imageView1);
            //iv.setImageResource(R.drawable.back1);
            Glide.with(context).load(img.get(position)).dontAnimate().into(iv);
            return convertView;
        }

    }

    public void imageview(View v)
    {

        //DB객체 불러오기 및 리스트저장
        mDatabase.child("test").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                ImageList.clear();
                userImageDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    UserImageDTO userImageDTO = snapshot.getValue(UserImageDTO.class);
                    userImageDTOS.add(userImageDTO);
                    ImageList.add(userImageDTO.img_file);

                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        ImageAdapter test = new ImageAdapter(getApplicationContext(),R.layout.image_list, ImageList);

        listView.setAdapter(test);
    }

    public  void  imgsearch(View view)
    {

        //DB객체 불러오기 및 리스트저장
        mDatabase.child("test").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                ImageList.clear();
                userImageDTOS.clear();
                String search = imgsearch_name.getText().toString();

                int i=0;
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    UserImageDTO userImageDTO = snapshot.getValue(UserImageDTO.class);

                    if(search.getBytes().length<=0) {
                        Toast.makeText(getApplicationContext(),"검색할 헤어이름을 입력하세요",Toast.LENGTH_LONG).show();
                    }

                    else if(userImageDTO.img_name.contains(search)) {
                        userImageDTOS.add(userImageDTO);
                        ImageList.add(userImageDTO.img_file);
                    }
                    i++;

                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        ImageAdapter test = new ImageAdapter(getApplicationContext(),R.layout.image_list, ImageList);

        listView.setAdapter(test);
    }

}
