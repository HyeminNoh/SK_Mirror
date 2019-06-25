package com.example.mys.mirror;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.PopupMenu;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.OnProgressListener;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class UserImage extends AppCompatActivity {

    private Uri filePath;
    ImageView imageView;
    EditText imagename;
    String name;

    GridView listView;
    LinearLayout imagelistlayout;
    LinearLayout imageinfo;

    LinearLayout imagelayout;
    ArrayList<String> Imagelist;

    private DatabaseReference mDatabase;
    FirebaseAuth firebaseAuth;

    List<UserImageDTO> userImageDTOS= new ArrayList<>();
   // ArrayList itemArrayList = new ArrayList<>();

   public String furl;
   int pos;
   String imagetile;
   Button imagesesrch;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_image);
        setTitle("이미지관리");

       // getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));

        firebaseAuth = firebaseAuth.getInstance();
        FirebaseUser user = firebaseAuth.getCurrentUser();

        imageView = (ImageView)findViewById(R.id.userimage);
        imagename = (EditText) findViewById(R.id.imagename);
        listView = (GridView) findViewById(R.id.imagelist);
        imagelayout = (LinearLayout) findViewById(R.id.imagelayout);
        imagelistlayout = (LinearLayout) findViewById(R.id.imagelistlayout);
        imageinfo = (LinearLayout) findViewById(R.id.imageinfo);


        imagelayout.setVisibility(View.GONE);
        imagelistlayout.setVisibility(View.VISIBLE);
        //imageinfo.setVisibility(View.GONE);

        imagesesrch = (Button) findViewById(R.id.imagesesrch);

        Imagelist = new ArrayList<String>();

        //DB초기화
        mDatabase = FirebaseDatabase.getInstance().getReference("images");
        String id = user.getEmail();

        int result = id.indexOf("@");
        name= id.substring(0,result);

        //DB객체 불러오기 및 리스트저장
        mDatabase.child(name).addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Imagelist.clear();
                userImageDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    UserImageDTO userImageDTO = snapshot.getValue(UserImageDTO.class);
                    userImageDTOS.add(userImageDTO);
                    Imagelist.add(userImageDTO.img_file);
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
                intent.putExtra("filename", Imagelist.get(position));
                intent.putExtra("name",userImageDTOS.get(position).img_name);

                startActivity(intent);
            }
        });
        listView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {

                pos=position;
                final PopupMenu popupMenu = new PopupMenu(getApplication(),view);
                popupMenu.getMenuInflater().inflate(R.menu.imagepopup,popupMenu.getMenu());
                imagetile = userImageDTOS.get(pos).img_name;
                imagetile = imagetile.replace(".png","");

                popupMenu.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
                    @Override
                    public boolean onMenuItemClick(MenuItem item) {

                        if(item.getTitle().equals("수정"))
                        {
                            imagesesrch.performClick();
                            imagename.setText(imagetile);

                        }
                        else if (item.getTitle().equals("삭제")) {

                            mDatabase.child(name).child(imagetile).removeValue();

                        }
                        return false;
                    }

                });
                popupMenu.show();

                return false;
            }
        });




        //ImageList = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1,new ArrayList<String>()) ;
        //ImageList = new ArrayAdapter<String>(this,R.layout.image_list,new ArrayList<String>()) ;
        //listView.setAdapter(ImageList) ;

      /*  listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String s = ImageList.getItem(position);

                Intent show = new Intent(getApplicationContext(), Show_image.class);
                show.putExtra("filename",s);
                show.putExtra("name", name);
                startActivity(show);




            }
        });*/




    }

    public void updateimage()
    {
        //DB객체 불러오기 및 리스트저장
        mDatabase.child(name).addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Imagelist.clear();
                userImageDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    UserImageDTO userImageDTO = snapshot.getValue(UserImageDTO.class);
                    userImageDTOS.add(userImageDTO);
                    Imagelist.add(userImageDTO.img_file);
                    MyAdapter test = new MyAdapter(getApplicationContext(),R.layout.image_list, Imagelist);
                    listView.setAdapter(test);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        MyAdapter test = new MyAdapter(getApplicationContext(),R.layout.image_list, Imagelist);
        listView.setAdapter(test);
    }



    public void imagesearch(View v)
    {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent, "이미지를 선택하세요."), 0);
        imagelayout.setVisibility(View.VISIBLE);
       // imageinfo.setVisibility(View.VISIBLE);
        imagelistlayout.setVisibility(View.GONE);


    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 0 && resultCode == RESULT_OK) {
            filePath = data.getData();
            //Log.d(TAG, "uri:" + String.valueOf(filePath));

            try {
                //Uri 파일을 Bitmap으로 만들어서 ImageView에 집어 넣는다.
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), filePath);
                imageView.setImageBitmap(bitmap);

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    //upload the file
    public void uploadFile(View v) {



        if(imagename.getText().toString().equals(""))
        {
            Toast.makeText(getApplicationContext(),"이미지 이름을 입력해주세요.",Toast.LENGTH_LONG).show();
        }
        else
        {

            InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);

            imm.hideSoftInputFromWindow(imagename.getWindowToken(), 0);

            //업로드할 파일이 있으면 수행
            if (filePath != null) {
                //업로드 진행 Dialog 보이기
                final ProgressDialog progressDialog = new ProgressDialog(this);
                progressDialog.setTitle("업로드중...");
                progressDialog.show();

                //storage
                FirebaseStorage storage = FirebaseStorage.getInstance();



                final String filename = imagename.getText().toString() + ".png";
                final String fname = imagename.getText().toString();
                //storage 주소와 폴더 파일명을 지정해 준다.
                final StorageReference storageRef = storage.getReferenceFromUrl("gs://backup-c8eab.appspot.com").child("images/"+name+"/"+ filename);


                storageRef.putFile(filePath)
                        //성공시
                        .addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
                            @Override
                            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {

                                success();

                                progressDialog.dismiss(); //업로드 진행 Dialog 상자 닫기

                                Toast.makeText(getApplicationContext(), "업로드 완료!", Toast.LENGTH_SHORT).show();
                                imagelayout.setVisibility(View.GONE);
                                imagename.setText("");
                                //.setVisibility(View.GONE);

                            }
                        })
                        //실패시
                        .addOnFailureListener(new OnFailureListener() {
                            @Override
                            public void onFailure(@NonNull Exception e) {
                                progressDialog.dismiss();
                                Toast.makeText(getApplicationContext(), "업로드 실패!", Toast.LENGTH_SHORT).show();
                            }
                        })
                        //진행중
                        .addOnProgressListener(new OnProgressListener<UploadTask.TaskSnapshot>() {
                            @Override
                            public void onProgress(UploadTask.TaskSnapshot taskSnapshot) {
                                @SuppressWarnings("VisibleForTests")
                                double progress = (100 * taskSnapshot.getBytesTransferred()) / taskSnapshot.getTotalByteCount();
                                //dialog에 진행률을 퍼센트로 출력해 준다
                                progressDialog.setMessage("Uploaded " + ((int) progress) + "% ...");
                            }
                        });


            } else {
                Toast.makeText(getApplicationContext(), "파일을 먼저 선택하세요.", Toast.LENGTH_SHORT).show();
            }
        }
        updateimage();
    }

    //성공시 url을 받기위해 실행
    public void success()
    {


        FirebaseStorage storage = FirebaseStorage.getInstance();
        final String filename = imagename.getText().toString() + ".png";
        final String fname = imagename.getText().toString();
        //storage 주소와 폴더 파일명을 지정해 준다.
         StorageReference storageRef = storage.getReferenceFromUrl("gs://backup-c8eab.appspot.com").child("images/"+name+"/"+ filename);

        storageRef.getDownloadUrl().addOnSuccessListener(new OnSuccessListener<Uri>() {
            @Override
            public void onSuccess(Uri uri) {
                furl=String.valueOf(uri);
                UserImageDTO userImageDTO = new UserImageDTO();

                Date now = new Date();
                SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMHH_mmss");

                userImageDTO.img_name = filename;
                userImageDTO.img_file = String.valueOf(furl);
                userImageDTO.updated_at = formatter.format(now);
                //DB 입력
                mDatabase.child(name).child(fname).setValue(userImageDTO);

            }
        });



    }

    public void imageload(View v) {
        //imageinfo.setVisibility(View.GONE);
        imagelistlayout.setVisibility(View.VISIBLE);
        //DB객체 불러오기 및 리스트저장
        mDatabase.child(name).addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Imagelist.clear();
                userImageDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    UserImageDTO userImageDTO = snapshot.getValue(UserImageDTO.class);
                    userImageDTOS.add(userImageDTO);
                    Imagelist.add(userImageDTO.img_file);
                    MyAdapter test = new MyAdapter(getApplicationContext(),R.layout.image_list, Imagelist);
                    listView.setAdapter(test);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        MyAdapter test = new MyAdapter(getApplicationContext(),R.layout.image_list, Imagelist);
        listView.setAdapter(test);
    }

    class MyAdapter extends BaseAdapter {
        Context context;
        int layout;
        ArrayList<String> img ;
        LayoutInflater inf;
        public MyAdapter(Context context, int layout,  ArrayList<String> tttt) {
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

    public  void  usersearch(View view)
    {

        //DB객체 불러오기 및 리스트저장
        mDatabase.child(name).addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Imagelist.clear();
                userImageDTOS.clear();
                String search = imagename.getText().toString();
                //Toast.makeText(getApplicationContext(),search,Toast.LENGTH_LONG).show();

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
                        Imagelist.add(userImageDTO.img_file);
                    }
                    i++;
                    MyAdapter test = new MyAdapter(getApplicationContext(),R.layout.image_list, Imagelist);

                    listView.setAdapter(test);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        MyAdapter test = new MyAdapter(getApplicationContext(),R.layout.image_list, Imagelist);

        listView.setAdapter(test);
    }

}


