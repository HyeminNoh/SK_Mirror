package com.example.mys.mirror;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.PopupMenu;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class Memo extends AppCompatActivity {

    private DatabaseReference mDatabase;

    List<MemoDTO> memoDTOS = new ArrayList<>();

    String name;
    EditText memoinput;
    String count;
    ArrayList<String> Memolist;
    LinearLayout memolayout ;
    LinearLayout listlayout;
    ListView listview;
    FirebaseAuth firebaseAuth;

    int stat = 0;
    int pos;
    int size;
    int chtest=0;
    Button blist;


    String memotile;
    boolean mcehck;
    InputMethodManager imm;
    MemoAdapter memoAdapter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_memo);
        setTitle("메모");
        //getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF66CCFF));

        firebaseAuth = firebaseAuth.getInstance();
        FirebaseUser user = firebaseAuth.getCurrentUser();


        //DB초기화
        mDatabase = FirebaseDatabase.getInstance().getReference("memos");
        String id = user.getEmail();

        int result = id.indexOf("@");
        name= id.substring(0,result);

        listview = (ListView) findViewById(R.id.List) ;
        memoinput = (EditText) findViewById(R.id.memoinput);
        memolayout = (LinearLayout) findViewById(R.id.memolayout);
        memolayout.setVisibility(View.GONE);
        listlayout = (LinearLayout) findViewById(R.id.listlayout);

        blist = (Button) findViewById(R.id.blist);
        Memolist = new ArrayList<String>();
        //DB객체 불러오기 및 리스트저장
        mDatabase.child(name).addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                Memolist.clear();
                memoDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    MemoDTO memoDTO = snapshot.getValue(MemoDTO.class);
                    memoDTOS.add(memoDTO);
                    Memolist.add(memoDTO.write);

                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        ltemclick();





    }

    class MemoAdapter extends BaseAdapter {
        Context context;
        int layout;
        ArrayList<String> img ;
        LayoutInflater inf;
        public MemoAdapter(Context context, int layout, ArrayList<String> tttt) {
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
        public View getView(final int position, View convertView, ViewGroup parent) {
            if (convertView==null)
                convertView = inf.inflate(layout,null);



            TextView iv = (TextView) convertView.findViewById(R.id.txt);
            iv.setText(img.get(position));
            Switch sw = (Switch) convertView.findViewById(R.id.switch1);
            sw.setFocusable(false);


            if(memoDTOS.get(position).tomirror.equals("true"))
            {
                sw.setChecked(true);

            }
            else if(memoDTOS.get(position).tomirror.equals("false"))
            {
                sw.setChecked(false);

            }
            sw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

                        mirrorcheck(isChecked,position);
                }
            });

            return convertView;

        }

    }

    public void ltemclick()
    {
        listview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, final View view, int position, long id) {

                pos=position;
                PopupMenu popupMenu = new PopupMenu(getApplication(),view);
                popupMenu.getMenuInflater().inflate(R.menu.momopopup,popupMenu.getMenu());
                memotile = memoDTOS.get(pos).time;
                //Toast.makeText(getApplicationContext(),memoDTOS.get(position).write,Toast.LENGTH_LONG).show();

                popupMenu.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
                    @Override
                    public boolean onMenuItemClick(MenuItem item) {

                        if(item.getTitle().equals("수정"))
                        {
                            memolayout.setVisibility(View.VISIBLE);
                            memoinput.setText(memoDTOS.get(pos).write);
                            memoinput.setFocusable(true);
                            stat = 1;

                        }
                        else if (item.getTitle().equals("삭제")) {

                            mDatabase.child(name).child(memotile).removeValue();

                        }
                        else if (item.getTitle().equals("미러등록"))
                        {
                            MemoDTO memoDTO = new MemoDTO();
                            memoDTO.userid = memoDTOS.get(pos).userid;
                            memoDTO.write = memoDTOS.get(pos).write;
                            memoDTO.tomirror = "true";
                            memoDTO.time = memoDTOS.get(pos).time;

                            //mDatabase.child(name).child(memotile).removeValue();
                            mDatabase.child(name).child(memotile).setValue(memoDTO);
                        }
                        else if (item.getTitle().equals("미러해제"))
                        {
                            MemoDTO memoDTO = new MemoDTO();
                            memoDTO.userid = memoDTOS.get(pos).userid;
                            memoDTO.write = memoDTOS.get(pos).write;
                            memoDTO.tomirror = "false";
                            memoDTO.time = memoDTOS.get(pos).time;

                            //mDatabase.child(name).child(memotile).removeValue();
                            mDatabase.child(name).child(memotile).setValue(memoDTO);
                        }
                        return false;
                    }

                });
                popupMenu.show();
            }
        });

    }

    public void memoview(View v)
    {
        listview.setVisibility(View.VISIBLE);
       // memoAdapter = new ImageAdapter(getApplicationContext(),R.layout.memoview, ImageList);
       // listview.setAdapter(memoAdapter);
        updatememo();
    }

    public void writememo(View v)
    {
        memolayout.setVisibility(View.VISIBLE);
    }

    public void addmemo(View v)
    {


        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd_hh:mm:ss");

       if(stat==0) {
           size = memoDTOS.size();
           //Toast.makeText(getApplicationContext(),String.valueOf(size),Toast.LENGTH_LONG).show();
           //count = String.valueOf(size+1);
           MemoDTO memoDTO = new MemoDTO();


           if (memoinput.getText().toString().equals("")) {
               Toast.makeText(getApplicationContext(), "메모가 없습니다.", Toast.LENGTH_LONG).show();

           } else {
               long now = System.currentTimeMillis();
               Date date = new Date(now);
               //count = String.valueOf(memoDTOS.size()+1);
               memoDTO.userid = name;
               memoDTO.write = memoinput.getText().toString();
               memoDTO.tomirror = "false";
               memoDTO.time = sdf.format(date);



               //String getTime = sdf.format(date);



               mDatabase.child(name).child(sdf.format(date)).setValue(memoDTO);

               memoinput.setText("");
               //memoinput.setVisibility(View.INVISIBLE);

               memolayout.setVisibility(View.GONE);

               Toast.makeText(getApplicationContext(), "등록되었습니다.", Toast.LENGTH_LONG).show();



           }
       }

       if (stat==1)
       {


           MemoDTO memoDTO = new MemoDTO();
           memoDTO.userid = name;
           memoDTO.write = memoinput.getText().toString();
           memoDTO.tomirror = "false";
           memoDTO.time = memotile;

           //mDatabase.child(name).child(memotile).removeValue();
           mDatabase.child(name).child(memotile).setValue(memoDTO);

           memoinput.setText("");
           //memoinput.setVisibility(View.INVISIBLE);

           memolayout.setVisibility(View.GONE);

           Toast.makeText(getApplicationContext(), "수정되었습니다.", Toast.LENGTH_LONG).show();
           stat=0;
           memoAdapter = new MemoAdapter(getApplicationContext(),R.layout.memoview, Memolist);
           listview.setAdapter(memoAdapter);
       }

        imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
        imm.showSoftInput(memoinput, 0);
        imm.hideSoftInputFromWindow(memoinput.getWindowToken(), 0);
       //listview.invalidate();
        updatememo();

    }


    public void mirrorcheck(boolean mcehck, int position)
    {
        memotile = memoDTOS.get(position).time;

        if (mcehck==true)
        {
            MemoDTO memoDTO = new MemoDTO();
            memoDTO.userid = memoDTOS.get(position).userid;
            memoDTO.write = memoDTOS.get(position).write;
            memoDTO.tomirror = "true";
            memoDTO.time = memoDTOS.get(position).time;

            mDatabase.child(name).child(memotile).setValue(memoDTO);
        }
        else if (mcehck==false)
        {
            MemoDTO memoDTO = new MemoDTO();
            memoDTO.userid = memoDTOS.get(position).userid;
            memoDTO.write = memoDTOS.get(position).write;
            memoDTO.tomirror = "false";
            memoDTO.time = memoDTOS.get(position).time;

            mDatabase.child(name).child(memotile).setValue(memoDTO);



        }
    }

    public void updatememo()
    {
        mDatabase.child(name).addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                Memolist.clear();
                memoDTOS.clear();
                //snpashot에 수만큼 실행
                for(DataSnapshot snapshot : dataSnapshot.getChildren())
                {
                    MemoDTO memoDTO = snapshot.getValue(MemoDTO.class);
                    memoDTOS.add(memoDTO);
                    Memolist.add(memoDTO.write);

                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        memoAdapter = new MemoAdapter(getApplicationContext(),R.layout.memoview, Memolist);
        listview.setAdapter(memoAdapter);

    }
}
