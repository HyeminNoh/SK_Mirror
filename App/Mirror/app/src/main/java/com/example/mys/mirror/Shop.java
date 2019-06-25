package com.example.mys.mirror;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

public class Shop extends AppCompatActivity {


    List<UserDTO> userDTOS = new ArrayList<>();//DB 리스트객체

    private DatabaseReference mDatabase;

    EditText shopid;
    EditText shoppassword;
    TextView shopidcheck;
    TextView shoppasswordcheck;
    EditText shoppassword2;
    boolean idbol;
    boolean pasbol;
    boolean shopbol;

    EditText shopname;
    TextView shopnamecheck;

    String Userid;
    String Password;
    String Shopname;
    String Number;

    EditText number;

    FirebaseAuth firebaseAuth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_shop);
        setTitle("업체회원가입");
        //getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));

        firebaseAuth = FirebaseAuth.getInstance();


        shopid = (EditText) findViewById(R.id.shopid);
        shoppassword = (EditText) findViewById(R.id.shoppassword);

        shopidcheck = (TextView) findViewById(R.id.shopidcheck);
        shoppasswordcheck = (TextView) findViewById(R.id.shoppaswordcheck);

        shoppassword2 = (EditText) findViewById(R.id.shoppassword2);


        shopname = (EditText) findViewById(R.id.shopname);
        shopnamecheck = (TextView) findViewById(R.id.shopnamecheck);

        number = (EditText) findViewById(R.id.number);

        mDatabase = FirebaseDatabase.getInstance().getReference();

        //DB객체 불러오기 및 리스트저장
        mDatabase.getDatabase().getReference("users").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                userDTOS.clear();

                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    //리스트 객체에 snapshot 입력
                    UserDTO user = snapshot.getValue(UserDTO.class);
                    userDTOS.add(user);
                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        checkshopname();
        checkid();
        checkpass();

    }

    public void search(View v)
    {
        Intent intent = new Intent(getApplicationContext(), DaumwebView.class);
        startActivity(intent);
    }


    public void checkshopname()
    {

        shopname.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {


               /* for (int i=0; i<userDTOS.size(); i++) {
                    if (shopname.getText().toString().equals(userDTOS.get(i).shopname)) {

                        shopnamecheck.setText("이미 존재하는 업체명 입니다.");
                        shopnamecheck.setTextColor(Color.parseColor("#FF0000"));
                        shopbol = false;
                        return;
                    }
                    else if(shopname.getText().toString().length()>=4  )

                    {
                        shopnamecheck.setText("사용할 수 있는 업체명 입니다. ");
                        shopnamecheck.setTextColor(Color.parseColor("#00FF00"));
                        shopbol = true;
                    }
                    else if(shopname.getText().toString().length()<5  )

                    {
                        shopnamecheck.setText("업체명이 너무 짧습니다.");
                        shopnamecheck.setTextColor(Color.parseColor("#FF0000"));
                        shopbol = false;

                    }


                }*/


            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });


    }

    public void checkid()
    {

        shopid.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {



                    if(android.util.Patterns.EMAIL_ADDRESS.matcher(shopid.getText().toString()).matches() )

                    {
                        shopidcheck.setText("사용할 수 있는 형식 입니다. ");
                        shopidcheck.setTextColor(Color.parseColor("#00FF00"));
                        idbol = true;
                    }
                    else if(!android.util.Patterns.EMAIL_ADDRESS.matcher(shopid.getText().toString()).matches()  )

                    {
                        shopidcheck.setText("사용할 수 없는 형식 입니다.");
                        shopidcheck.setTextColor(Color.parseColor("#FF0000"));
                        idbol = false;

                    }





            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });


    }

    public void  checkpass()
    {
        shoppassword2.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

                if(shoppassword.getText().toString().equals(shoppassword2.getText().toString()))
                {
                    if(shoppassword.getText().toString().length()>4)
                    {
                        shoppasswordcheck.setText("비밀번호가 일치합니다");
                        shoppasswordcheck.setTextColor(Color.parseColor("#00FF00"));
                        pasbol = true;
                    }
                }
                else if(shoppassword.getText().toString().length()>4)
                {
                    shoppasswordcheck.setText("비밀번호가 불일치 합니다");
                    shoppasswordcheck.setTextColor(Color.parseColor("#FF0000"));
                    pasbol = false;
                }
                else if(shoppassword.getText().toString().length() < 5)
                {
                    shoppasswordcheck.setText("비밀번호가 너무 짧습니다");
                    shoppasswordcheck.setTextColor(Color.parseColor("#FF0000"));
                    pasbol = false;
                }


            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
    }


    public void acceptshop(View v)
    {




        // 비밀번호 길이체크

      if (shoppassword.getText().toString().length() < 5) {
            Toast.makeText(getApplicationContext(), "비밀번호가 너무 짧습니다.", Toast.LENGTH_LONG).show();

        }
        else  if(shopname.getText().toString().length()<5)
        {
            Toast.makeText(getApplicationContext(), "업체명을 확인해주세요.", Toast.LENGTH_LONG).show();

        }
        //아이디, 비밀번호 유효할시 가입
        else    if(idbol==true && pasbol==true && shopbol==true) {

            Userid = shopid.getText().toString(); // 아이디
            Password = shoppassword.getText().toString(); // 비밀번호
            Shopname = shopname.getText().toString();
          String uid = shopid.getText().toString().trim();
          String pw = shoppassword.getText().toString().trim();


          firebaseAuth.createUserWithEmailAndPassword(uid, pw).addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
              @Override
              public void onComplete(@NonNull Task<AuthResult> task) {
                  FirebaseUser user = task.getResult().getUser();
                  //사용자 정보객체 생성
                  final UserDTO userDTO = new UserDTO();

                  //DB삽입
                  userDTO.userid = user.getUid();
                  /*//userDTO.password = Password;
                  // userDTO.nickname = Nickname;
                  userDTO.shopname = Shopname;
                  userDTO.number = Number;

                  userDTO.usertype = true;*/


                  mDatabase.child("users").child(user.getUid()).setValue(userDTO);


                  Toast.makeText(getApplicationContext(), "가입완료되었습니다.", Toast.LENGTH_LONG).show();
                  Shop.this.finish();

              }
          }).addOnFailureListener(new OnFailureListener() {
              @Override
              public void onFailure(@NonNull Exception e) {
                  Toast.makeText(getApplicationContext(), "이미 존재하는 이메일 입니다..", Toast.LENGTH_LONG).show();

              }
          });


        }


    }

}

