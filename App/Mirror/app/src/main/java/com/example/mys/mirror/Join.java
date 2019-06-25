package com.example.mys.mirror;

import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class Join extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_join);

        setTitle("회원가입");
        //getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));

    }

    public void general(View v)
    {
        Intent intent = new Intent(getApplicationContext(), General.class);
        startActivity(intent);
        this.finish();
    }

   /* public void shop(View v)
    {
        Intent intent = new Intent(getApplicationContext(), Shop.class);
        startActivity(intent);
        this.finish();
    }*/
}
