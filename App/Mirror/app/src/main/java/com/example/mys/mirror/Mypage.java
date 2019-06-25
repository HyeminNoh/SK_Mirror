package com.example.mys.mirror;

import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;


public class Mypage extends AppCompatActivity {

    FirebaseAuth firebaseAuth;
    private DatabaseReference mDatabase;
    List<UserDTO> userDTOS= new ArrayList<>();
    String name;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mypage);

        setTitle("마이페이지");


        firebaseAuth = firebaseAuth.getInstance();
        final FirebaseUser user = firebaseAuth.getCurrentUser();

        //DB초기화
        mDatabase = FirebaseDatabase.getInstance().getReference("users");
        String id = user.getEmail();
        final String uid = user.getUid();

        int result = id.indexOf("@");
        name= id.substring(0,result);

        final EditText useradd = (EditText) findViewById(R.id.useradd);

        //DB객체 불러오기 및 리스트저장
        mDatabase.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                userDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    UserDTO userDTO = snapshot.getValue(UserDTO.class);

                    if(userDTO.userid.equals(uid)) {
                        userDTOS.add(userDTO);
                        useradd.setText(userDTO.address);

                    }


                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

       // uadd = userlist.get(1);
        //Toast.makeText(getApplicationContext(),uadd,Toast.LENGTH_LONG).show();


        TextView useremail = (TextView) findViewById(R.id.useremail);

        useremail.setText(id);
        ;





        //useradd.setText();





    }

    public void pwreplace(View view)
    {
        EditText userpw = (EditText) findViewById(R.id.userpw);
        userpw.setFocusableInTouchMode(true);
        userpw.setEnabled(true);
    }

    public void useraddreplace(View view)
    {
        EditText useradd = (EditText) findViewById(R.id.useradd);
        useradd.setFocusableInTouchMode(true);
        useradd.setEnabled(true);
        useradd.setFocusableInTouchMode(true);
        useradd.setFocusable(true);
    }
}
