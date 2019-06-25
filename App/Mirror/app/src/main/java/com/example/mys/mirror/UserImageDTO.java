package com.example.mys.mirror;

public class UserImageDTO {

    public String img_name;
    public String img_file; //헤어이미지 url
    public String updated_at;
    public String imageurl;


    public String getImg_name() {
        return img_name;
    }

    public void setImg_name(String img_name) {
        this.img_name = img_name;
    }


    public String getImg_file() {
        return img_file;
    }

    public void setImg_file(String img_file) {
        this.img_file = img_file;
    }

    public String getUpdated_at() {
        return updated_at;
    }

    public void setUpdated_at(String updated_at) {
        this.updated_at = updated_at;
    }

    public String getImageurl() {
        return imageurl;
    }

    public void setImageurl(String imageurl) {
        this.imageurl = imageurl;
    }

}
