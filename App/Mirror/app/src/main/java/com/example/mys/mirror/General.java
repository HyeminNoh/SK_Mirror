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
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.firebase.ui.auth.data.model.User;
import com.google.android.gms.tasks.OnCompleteListener;
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
import java.util.Iterator;
import java.util.List;

public class General extends AppCompatActivity {

    private DatabaseReference mDatabase;
// ...

   EditText Useridtxt;
   EditText Passwordtxt;
   EditText Passwordcheck;
   EditText Nicknametxt;
   EditText useraddress;

   RadioGroup genderrg;
   RadioButton gendertxt;

   /* RadioGroup lengthrg;
    RadioButton lengtytxt;

    RadioGroup hairtyperg;
    RadioButton hairtypetxt;

    RadioGroup thicknessrg;
    RadioButton thicknesstxt;

    RadioGroup amountrg;
    RadioButton amounttxt;

    RadioGroup staterg;
    RadioButton statetxt;

    RadioGroup scalptyperg;
    RadioButton scalptypetxt;*/

   Button Accept;


   public String Userid = null;
   public String Password= null;
  // public String Nickname= null;

   public  String gender= null;
   public  String length= null;
   public  String hairtype= null;
   public  String thickness= null;
   public  String amount= null;
   public  String state= null;
   public  String scalptype= null;
   public String age;
   public boolean joincheck = false;


    Spinner ageSpinner;
    ArrayAdapter ageAdapter;


    TextView usercheck;
    TextView checkpassword;

    List<UserDTO> userDTOS = new ArrayList<>();//DB 리스트객체

    FirebaseAuth firebaseAuth;



    boolean idbol = false;//아이디 중복유무체크
    boolean pasbol = false;//비밀번호 일치 유무체크



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_general);

        setTitle("일반회원가입");

        firebaseAuth = FirebaseAuth.getInstance();

       /*         //연령 스피너
        ageSpinner = (Spinner)findViewById(R.id.spinner_age);
        ageAdapter = ArrayAdapter.createFromResource(this, R.array.age, android.R.layout.simple_spinner_item);
        ageAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line );

        ageSpinner.setAdapter(ageAdapter);*/

        //DB초기화
        mDatabase = FirebaseDatabase.getInstance().getReference();

        //databse = FirebaseDatabase.getInstance();

        Accept = (Button) findViewById(R.id.accept);

        Useridtxt = (EditText) findViewById(R.id.userid); // 사용자 아이디
        usercheck = (TextView) findViewById(R.id.usercheck); // 아이디체크확인
        checkid(); // 아이디 중복확인

        Passwordtxt = (EditText) findViewById(R.id.password); //사용자 비밀번호
        Passwordcheck = (EditText) findViewById(R.id.password2); // 비밀번호확인
        checkpassword = (TextView) findViewById(R.id.passwordcheck);//비밀번호 일치확인
        useraddress = (EditText) findViewById(R.id.useraddress);
        checkpass();

        //Nicknametxt = (EditText)findViewById(R.id.nickname); // 사용자 닉네임
        //nickcehck = (TextView) findViewById(R.id.nickcheck); // 닉네임 체크 확인
        //checknickname(); // 닉네임 중복확인

       // genderrg = (RadioGroup) findViewById(R.id.genderrg);
        /*lengthrg = (RadioGroup) findViewById(R.id.length);
        hairtyperg = (RadioGroup) findViewById(R.id.hairtype);
        thicknessrg = (RadioGroup) findViewById(R.id.thickness);
        amountrg = (RadioGroup) findViewById(R.id.amount);
        staterg = (RadioGroup) findViewById(R.id.state);
        scalptyperg = (RadioGroup) findViewById(R.id.scalptype);*/


        //DB객체 불러오기 및 리스트저장
       /* mDatabase.getDatabase().getReference("users").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                userDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    //리스트 객체에 snapshot 입력
                    //UserDTO user = snapshot.getValue(UserDTO.class);
                   // userDTOS.add(user);
                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });*/


    }


    public void accept(View v)
    {




            // 아이디, 비밀번호 길이체크
            if (Useridtxt.getText().toString().length() < 4) {
                Toast.makeText(getApplicationContext(), "아이디가 너무 짧습니다.", Toast.LENGTH_LONG).show();
            }
            else if (Passwordtxt.getText().toString().length() < 5) {
                Toast.makeText(getApplicationContext(), "비밀번호가 너무 짧습니다.", Toast.LENGTH_LONG).show();

            }
            //아이디, 비밀번호 유효할시 가입
            else    if(idbol==true && pasbol==true) {

                Userid = Useridtxt.getText().toString(); // 아이디
                Password = Passwordtxt.getText().toString(); // 비밀번호
                // Nickname = Nicknametxt.getText().toString(); // 닉네임
                String uid = Useridtxt.getText().toString().trim();
                String pw = Passwordtxt.getText().toString().trim();




                //성별
               /* gendertxt = (RadioButton) findViewById(genderrg.getCheckedRadioButtonId());
                gender = gendertxt.getText().toString();*/

               //머리길이
               /* lengtytxt = (RadioButton) findViewById(lengthrg.getCheckedRadioButtonId());
                length = lengtytxt.getText().toString();

                //모발상태
                hairtypetxt = (RadioButton) findViewById(hairtyperg.getCheckedRadioButtonId());
                hairtype = hairtypetxt.getText().toString();

                //모발굵기
                thicknesstxt = (RadioButton) findViewById(thicknessrg.getCheckedRadioButtonId());
                thickness = thicknesstxt.getText().toString();

                //모량
                amounttxt = (RadioButton) findViewById(amountrg.getCheckedRadioButtonId());
                amount = amounttxt.getText().toString();

                //모발상태
                statetxt = (RadioButton) findViewById(staterg.getCheckedRadioButtonId());
                state = statetxt.getText().toString();

                //두피상태
                scalptypetxt = (RadioButton) findViewById(scalptyperg.getCheckedRadioButtonId());
                scalptype = scalptypetxt.getText().toString();

                //나이
                age = ageSpinner.getSelectedItem().toString();*/





                firebaseAuth.createUserWithEmailAndPassword(uid, pw).addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if(task.isSuccessful())
                        {

                            FirebaseUser user = task.getResult().getUser();
                            //사용자 정보객체 생성
                            final UserDTO userDTO = new UserDTO();
                            //DB삽입
                            userDTO.userid = user.getUid();

                            int result = Userid.indexOf("@");
                            String id = Userid.substring(0,result);
                            Toast.makeText(getApplicationContext(),  id, Toast.LENGTH_SHORT).show();

                            userDTO.password = Password ;
                            userDTO.address = useraddress.getText().toString();

                           /* userDTO.gender = gender;
                            userDTO.length = length;
                            userDTO.hairtype = hairtype;
                            userDTO.thickness = thickness;
                            userDTO.amount = amount;
                            userDTO.state = state;
                            userDTO.scalptype = scalptype;
                            userDTO.age = age;
                            userDTO.usertype = false;*/

                            mDatabase.child("users").child(id).setValue(userDTO);


                            Toast.makeText(getApplicationContext(), "가입완료되었습니다.", Toast.LENGTH_LONG).show();
                            General.this.finish();


                        }
                        else
                        {
                            Toast.makeText(getApplicationContext(), "이미 존재하는 이메일 입니다..", Toast.LENGTH_LONG).show();

                        }
                    }
                });




            }
            else if(idbol==false || pasbol==false)
            {
                Toast.makeText(getApplicationContext(),"아이디와 비밀번호를 확인해주세요",Toast.LENGTH_LONG).show();
            }


    }

    public void checkid()
    {

        Useridtxt.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

                if(android.util.Patterns.EMAIL_ADDRESS.matcher(Useridtxt.getText().toString()).matches())
                    {
                        usercheck.setText("사용할 수 있는 형식입니다.");
                        usercheck.setTextColor(Color.parseColor("#00FF00"));
                        idbol = true;
                    }
                    else if(!android.util.Patterns.EMAIL_ADDRESS.matcher(Useridtxt.getText().toString()).matches() )

                    {
                        usercheck.setText("사용할수 없는 형식입니다.");
                        usercheck.setTextColor(Color.parseColor("#FF0000"));
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
        Passwordcheck.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

                if(Passwordtxt.getText().toString().equals(Passwordcheck.getText().toString()))
                {
                    if(Passwordtxt.getText().toString().length()>5)
                    {
                        checkpassword.setText("비밀번호가 일치합니다");
                        checkpassword.setTextColor(Color.parseColor("#00FF00"));
                        pasbol = true;
                    }
                }
                else if(Passwordtxt.getText().toString().length()>5)
                {
                    checkpassword.setText("비밀번호가 불일치 합니다");
                    checkpassword.setTextColor(Color.parseColor("#FF0000"));
                    pasbol = false;
                }
                else if(Passwordtxt.getText().toString().length() < 6)
                {
                    checkpassword.setText("비밀번호가 너무 짧습니다");
                    checkpassword.setTextColor(Color.parseColor("#FF0000"));
                    pasbol = false;
                }


            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
    }



    public void searchaddress(View view)
    {
        Intent intent = new Intent(getApplicationContext(), DaumwebView.class);
        startActivity(intent);
    }

}
