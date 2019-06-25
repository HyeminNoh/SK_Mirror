package com.example.mys.mirror;

import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;
import java.util.List;

public class hairtypereplace extends AppCompatActivity {


    RadioGroup genderrg;
    RadioButton gendertxt;

    RadioGroup lengthrg;
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
    RadioButton scalptypetxt;

    Spinner ageSpinner;
    ArrayAdapter ageAdapter;

    private DatabaseReference mDatabase;

    List<UserDTO> userDTOS = new ArrayList<>();//DB 리스트객체

    FirebaseAuth firebaseAuth;

    public  String gender= null;
    public  String length= null;
    public  String hairtype= null;
    public  String thickness= null;
    public  String amount= null;
    public  String state= null;
    public  String scalptype= null;
    public String age;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_hairtypereplace);
        setTitle("정보변경");
       // getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));

        firebaseAuth = FirebaseAuth.getInstance();


        //연령 스피너
        ageSpinner = (Spinner)findViewById(R.id.spinner_age);
        ageAdapter = ArrayAdapter.createFromResource(this, R.array.age, android.R.layout.simple_spinner_item);
        ageAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line );



        ageSpinner.setAdapter(ageAdapter);

        mDatabase = FirebaseDatabase.getInstance().getReference();

        genderrg = (RadioGroup) findViewById(R.id.genderrg);
        lengthrg = (RadioGroup) findViewById(R.id.length);
        hairtyperg = (RadioGroup) findViewById(R.id.hairtype);
        thicknessrg = (RadioGroup) findViewById(R.id.thickness);
        amountrg = (RadioGroup) findViewById(R.id.amount);
        staterg = (RadioGroup) findViewById(R.id.state);
        scalptyperg = (RadioGroup) findViewById(R.id.scalptype);

        Intent intent = getIntent();
        age = intent.getExtras().getString("age");
        gender = intent.getExtras().getString("gender");
        length = intent.getExtras().getString("length");
        hairtype = intent.getExtras().getString("hairtype");
        thickness = intent.getExtras().getString("thickness");
        amount = intent.getExtras().getString("amount");
        state = intent.getExtras().getString("state");
        scalptype = intent.getExtras().getString("scalptype");
        gender = intent.getExtras().getString("gender");
        //Toast.makeText(getApplicationContext(),thickness, Toast.LENGTH_LONG).show();

        switch (age)
        {
            case "10대" :
                ageSpinner.setSelection(0);
                break;
            case "20대" :
                ageSpinner.setSelection(1);
                break;
            case "30대" :
                ageSpinner.setSelection(2);
                break;
            case "40대" :
                ageSpinner.setSelection(3);
                break;
            case "50대" :
                ageSpinner.setSelection(4);
                break;
            case "60대" :
                ageSpinner.setSelection(5);
                break;
                default:
                    ageSpinner.setSelection(1);

        }

        switch (gender)
        {
            case "남" :
                genderrg.check(findViewById(R.id.boy).getId());
                break;
            case "여" :
                genderrg.check(findViewById(R.id.gilr).getId());
                break;
                default:
                    genderrg.clearCheck();
        }

        switch (length)
        {
            case "단발" :
                lengthrg.check(findViewById(R.id.shorthair).getId());
                break;
            case "장발" :
                lengthrg.check(findViewById(R.id.longhair).getId());
                break;
            case "모름" :
                lengthrg.check(findViewById(R.id.non1).getId());
                break;
            default:
                lengthrg.clearCheck();
        }

        switch (hairtype)
        {
            case "지성" :
                hairtyperg.check(findViewById(R.id.Intelligence).getId());
                break;
            case "건성" :
                hairtyperg.check(findViewById(R.id.inattention).getId());
                break;
            case "중성" :
                hairtyperg.check(findViewById(R.id.neutrality).getId());
                break;
            case "민감성" :
                hairtyperg.check(findViewById(R.id.Sensitivity).getId());
                break;
            case "모름" :
                hairtyperg.check(findViewById(R.id.non2).getId());
                break;
            default:
                hairtyperg.clearCheck();
        }

        switch (thickness)
        {
            case "얇음" :
                thicknessrg.check(findViewById(R.id.tenuity).getId());
                break;
            case "보통" :
                thicknessrg.check(findViewById(R.id.nomal).getId());
                break;
            case "두꺼움" :
                thicknessrg.check(findViewById(R.id.Thick).getId());
                break;
            case "모름" :
                thicknessrg.check(findViewById(R.id.non3).getId());
                break;
            default:
                thicknessrg.clearCheck();
        }

        switch (amount)
        {
            case "적음" :
                amountrg.check(findViewById(R.id.low).getId());
                break;
            case "보통" :
                amountrg.check(findViewById(R.id.nomal2).getId());
                break;
            case "많음" :
                amountrg.check(findViewById(R.id.plenty).getId());
                break;
            case "모름" :
                amountrg.check(findViewById(R.id.non4).getId());
                break;
            default:
                amountrg.clearCheck();
        }

        switch (state)
        {
            case "손상" :
                staterg.check(findViewById(R.id.damaged).getId());
                break;
            case "보통" :
                staterg.check(findViewById(R.id.nomal3).getId());
                break;
            case "건강" :
                staterg.check(findViewById(R.id.health).getId());
                break;
            case "모름" :
                staterg.check(findViewById(R.id.non5).getId());
                break;
            default:
                staterg.clearCheck();
        }

        switch (scalptype)
        {
            case "지성" :
                scalptyperg.check(findViewById(R.id.Intelligence2).getId());
                break;
            case "건성" :
                scalptyperg.check(findViewById(R.id.inattention2).getId());
                break;
            case "민감성" :
                scalptyperg.check(findViewById(R.id.Sensitivity2).getId());
                break;
            case "모름" :
                scalptyperg.check(findViewById(R.id.non6).getId());
                break;
            default:
                scalptyperg.clearCheck();
        }

    }

    public void replacehairdata(View view)
    {

        //성별
        gendertxt = (RadioButton) findViewById(genderrg.getCheckedRadioButtonId());
        gender = gendertxt.getText().toString();

        //머리길이
        lengtytxt = (RadioButton) findViewById(lengthrg.getCheckedRadioButtonId());
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
        age = ageSpinner.getSelectedItem().toString();

        final UserDTO userDTO = new UserDTO();
        userDTO.userid = firebaseAuth.getUid();
       /* userDTO.gender = gender;
        userDTO.length = length;
        userDTO.hairtype = hairtype;
        userDTO.thickness = thickness;
        userDTO.amount = amount;
        userDTO.state = state;
        userDTO.scalptype = scalptype;
        userDTO.age = age;
        userDTO.usertype = false;*/

        mDatabase.child("users").child(firebaseAuth.getUid()).setValue(userDTO);
        Toast.makeText(getApplicationContext(),"저장되었습니다.",Toast.LENGTH_LONG).show();
        finish();
    }

    public void canceldata(View v)
    {
        finish();
    }
}
