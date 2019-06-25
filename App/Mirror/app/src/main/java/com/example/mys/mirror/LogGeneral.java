package com.example.mys.mirror;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
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

public class LogGeneral extends AppCompatActivity {


    EditText idtxt;
    EditText passwordtxt;
    Button logingbt;

    FirebaseAuth firebaseAuth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_general);
        setTitle("E-Mail로그인");
        //getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));


        idtxt = (EditText) findViewById(R.id.id);
        passwordtxt = (EditText) findViewById(R.id.password);
        logingbt = (Button) findViewById(R.id.login);

        firebaseAuth = firebaseAuth.getInstance();






    }

    public void Logincheck(View v) {

        final ProgressDialog progressDialog = new ProgressDialog(this);
        progressDialog.setTitle("로그인중");
        progressDialog.show();

        String id = idtxt.getText().toString().trim();
        String pw = passwordtxt.getText().toString().trim();

        firebaseAuth.signInWithEmailAndPassword(id, pw).addOnCompleteListener(LogGeneral.this, new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if(task.isSuccessful())
                {
                    progressDialog.dismiss();
                    Intent intent = new Intent(getApplicationContext(), MainView.class);


                        startActivity(intent);
                        LogGeneral.this.finish();


                }
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                passwordtxt.setText("");
                progressDialog.dismiss();
                Toast.makeText(getApplicationContext(), "아이디 또는 비밀번호를 확인해 주세요", Toast.LENGTH_LONG).show();

            }
        });



    }
}
