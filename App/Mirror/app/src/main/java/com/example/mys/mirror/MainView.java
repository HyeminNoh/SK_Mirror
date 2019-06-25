package com.example.mys.mirror;

import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
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


public class MainView extends AppCompatActivity {

    Button designer;
    boolean admin=false;
    String name;
    FirebaseAuth firebaseAuth;

    DatabaseReference mDatabase;
    List<UserDTO> userDTOS = new ArrayList<>();//DB 리스트객체

    Button Memo;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_view);

        firebaseAuth = firebaseAuth.getInstance();

        FirebaseUser uid = firebaseAuth.getCurrentUser();
        //Toast.makeText(this,  uid.getEmail(), Toast.LENGTH_SHORT).show();

        setTitle("메인메뉴");
        //액션바 배경색 변경
        //getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));
        //홈버튼 표시
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);



       // designer = (Button) findViewById(R.id.designer);
        Memo = (Button) findViewById(R.id.memo);
        name = firebaseAuth.getUid();

      /*  mDatabase = FirebaseDatabase.getInstance().getReference("users");


        //DB객체 불러오기 및 리스트저장
        mDatabase.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                userDTOS.clear();
                //snpashot에 수만큼 실행
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    //리스트 객체에 snapshot 입력
                    //UserDTO user = snapshot.getValue(UserDTO.class);
                  //  userDTOS.add(user);
                }

               for(int i=0; i<userDTOS.size();i++)
                {
                    if(name.equals(userDTOS.get(i).userid))
                    {
                        admin = userDTOS.get(i).usertype;

                    }
                }
                if(admin==false)
                {
                    designer.setVisibility(View.GONE);
                }
                else if(admin==true)
                {
                    designer.setVisibility(View.VISIBLE);

                }


            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });*/




        //usercheck();

    }

    public void Memo(View v)
    {
        Intent intent = new Intent(getApplicationContext(), Memo.class);
        startActivity(intent);
    }

   /* public void usercheck()
    {

        if(admin==false)
        {
            designer.setVisibility(View.GONE);
        }
        else if(admin==true)
        {
            designer.setVisibility(View.VISIBLE);

        }

    }*/

    public void imagemanage(View v)
    {
        Intent intent = new Intent(getApplicationContext(), UserImage.class);
        startActivity(intent);

    }

    public void colormatch(View view)
    {
        Intent intent = new Intent(getApplicationContext(), Colormatch.class);
        startActivity(intent);
    }

    public void hairmatch(View v)
    {
        Intent intent = new Intent(getApplicationContext(), Hairmatch.class);
        startActivity(intent);

    }

    public  void mypage(View view)
    {
        Intent intent = new Intent(getApplicationContext(), Mypage.class);
        startActivity(intent);
    }

    public  void imggallery(View view)
    {
        Intent intent = new Intent(getApplicationContext(), ImageGallery.class);
        startActivity(intent);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu, menu);


        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.logout) {
            FirebaseAuth.getInstance().signOut();
            finish();
            Intent intent = new Intent(getApplicationContext(), Login.class);
            startActivity(intent);

            Toast.makeText(this, "로그아웃 되었습니다.", Toast.LENGTH_SHORT).show();
            return true;
        }




        return super.onOptionsItemSelected(item);
    }
}


