package com.example.mys.mirror;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import com.beardedhen.androidbootstrap.TypefaceProvider;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.ApiException;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthCredential;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.GoogleAuthProvider;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.nhn.android.naverlogin.OAuthLogin;
import com.nhn.android.naverlogin.ui.view.OAuthLoginButton;

public class Login extends AppCompatActivity {

    public static OAuthLogin mOAuthLoginModule;
    OAuthLoginButton mOAuthLoginButton;


    FirebaseAuth firebaseAuth;

    private static final int RC_SIGN_IN = 9001;
    private GoogleSignInClient mGoogleSignInClient;

    DatabaseReference mDatabase;

     ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        setTitle("헤어스타일링 미러");
        //getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));
        TypefaceProvider. registerDefaultIconSets ();
        firebaseAuth = FirebaseAuth.getInstance();

        mDatabase = FirebaseDatabase.getInstance().getReference();

        if(firebaseAuth.getCurrentUser() != null){
            //이미 로그인 되었다면 이 액티비티를 종료함
            finish();
            //그리고 profile 액티비티를 연다.

           //String user = firebaseAuth.getUid();

            Intent intent = new Intent(getApplicationContext(), MainView.class);
            startActivity(intent);

            finish();
        }

        ImageView imageView = (ImageView) findViewById(R.id.main);
        imageView.setImageResource(R.drawable.back1);


        //setNaver();

        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestIdToken(getString(R.string.default_web_client_id))
                .requestEmail()
                .build();

        mGoogleSignInClient = GoogleSignIn.getClient(this, gso);


        SignInButton google = (SignInButton) findViewById(R.id.login_button);
        google.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent signInIntent = mGoogleSignInClient.getSignInIntent();
                startActivityForResult(signInIntent, RC_SIGN_IN);
            }
        });


    }



    public void join(View v)
    {
        Intent intent = new Intent(getApplicationContext(), General.class);
        startActivity(intent);


    }

    public void custom(View v)
    {
        Intent intent = new Intent(getApplicationContext(), LogGeneral.class);
        startActivity(intent);
    }

    //네이버로그인
    /*private void setNaver() {
        mOAuthLoginModule = OAuthLogin.getInstance();
        mOAuthLoginModule.init(this, "gxkXRjsCcagYmR7Jjlnl", "sa0Sy6CUmm", "Mirror");

        mOAuthLoginButton = findViewById(R.id.button_naverlogin);

        mOAuthLoginButton.setOAuthLoginHandler(mOAuthLoginHandler);
//        mOAuthLoginModule.startOauthLoginActivity(this, mOAuthLoginHandler);
    }

    //로그인성공실패
    private OAuthLoginHandler mOAuthLoginHandler = new OAuthLoginHandler() {
        @Override
        public void run(boolean success) {
            if (success) {
                String accessToken = mOAuthLoginModule.getAccessToken(getApplicationContext());
                String refreshToken = mOAuthLoginModule.getRefreshToken(getApplicationContext());
                long expiresAt = mOAuthLoginModule.getExpiresAt(getApplicationContext());
                String tokenType = mOAuthLoginModule.getTokenType(getApplicationContext());
                Intent intent = new Intent(getApplicationContext(), MainView.class);
                startActivity(intent);
            } else {
                String errorCode = mOAuthLoginModule.getLastErrorCode(getApplicationContext()).getCode();
                String errorDesc = mOAuthLoginModule.getLastErrorDesc(getApplicationContext());
                Toast.makeText(getApplicationContext(), "로그인실패 관리자에게 문의하세요", Toast.LENGTH_SHORT).show();

            }
        };
    };*/


    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        progressDialog = new ProgressDialog(this);
        progressDialog.setTitle("로그인중");
        progressDialog.show();

        // Result returned from launching the Intent from GoogleSignInApi.getSignInIntent(...);
        if (requestCode == RC_SIGN_IN) {
            Task<GoogleSignInAccount> task = GoogleSignIn.getSignedInAccountFromIntent(data);
            try {
                // Google Sign In was successful, authenticate with Firebase
                GoogleSignInAccount account = task.getResult(ApiException.class);
                firebaseAuthWithGoogle(account);
            } catch (ApiException e) {
                // Google Sign In failed, update UI appropriately
                // ...
            }
        }
    }

    private void firebaseAuthWithGoogle(GoogleSignInAccount acct) {

        AuthCredential credential = GoogleAuthProvider.getCredential(acct.getIdToken(), null);
        firebaseAuth.signInWithCredential(credential)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // Sign in success, update UI with the signed-in user's information
                            FirebaseUser user = firebaseAuth.getCurrentUser();
                            final UserDTO userDTO = new UserDTO();

                            userDTO.userid = user.getUid();
                            userDTO.address = "null";
                            String str= user.getEmail();

                            //userDTO.password = Password;
                            // userDTO.nickname = Nickname;

                            /*userDTO.gender = "미선택";
                            userDTO.length = "미선택";
                            userDTO.hairtype = "미선택";
                            userDTO.thickness = "미선택";
                            userDTO.amount = "미선택";
                            userDTO.state = "미선택";
                            userDTO.scalptype = "미선택";
                            userDTO.age = "미선택";

                            userDTO.usertype = false;*/


                            //이메일에서 아이디만 추출 (@이후 문자열제거)
                            int result = str.indexOf("@");
                            String id = str.substring(0,result);
                            //Toast.makeText(getApplicationContext(),  id, Toast.LENGTH_SHORT).show();

                            mDatabase.child("users").child(id).setValue(userDTO);


                            progressDialog.dismiss();

                            Intent intent = new Intent(getApplicationContext(), MainView.class);
                            startActivity(intent);



                        }
                        else {
                            progressDialog.dismiss();
                            Toast.makeText(getApplicationContext(),"로그인을 실패하였습니다.",Toast.LENGTH_LONG).show();
                        }


                        // ...
                    }
                });
    }


}

