package com.example.mys.mirror;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.bumptech.glide.Glide;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;
import java.util.List;

public class Show_image extends AppCompatActivity {

    FirebaseAuth firebaseAuth;
    String uid;
    List<UserImageDTO> userImageDTOS= new ArrayList<>();
    String filename;
    String name;
    private DatabaseReference mDatabase;
    Button stopmirror;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_image);


       // getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));

        //stopmirror = (Button)findViewById(R.id.stopmirror);

        firebaseAuth = firebaseAuth.getInstance();
        uid = firebaseAuth.getUid();

        ImageView show = (ImageView) findViewById(R.id.show);

        Intent intent = getIntent();
        name = intent.getExtras().getString("name");
        filename = intent.getExtras().getString("filename");
        setTitle(name);
        setTitleColor(Color.parseColor("#000000"));

        final ProgressDialog progressDialog = new ProgressDialog(this);
        progressDialog.setTitle("이미지 받아오는중");
        progressDialog.show();

        Glide.with(getApplicationContext()).load(filename).dontAnimate().into(show);
        progressDialog.dismiss();




    }

    /*public void startmirror(View v)
    {

        UserImageDTO userImageDTO = new UserImageDTO();
        userImageDTO.img_file = filename;
        //DB 입력
        mDatabase = FirebaseDatabase.getInstance().getReference("onhairmatching");
        mDatabase.child(uid).setValue(userImageDTO);
    }

    public void stopmirror(View v)
    {
        mDatabase.child(uid).removeValue();
    }*/

    @Override
    protected void onDestroy() {
        super.onDestroy();
       // stopmirror.performClick();

    }
}
