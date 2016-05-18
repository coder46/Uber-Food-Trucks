package com.example.faisal.interfaces;

import com.example.faisal.models.ResponseData;
import com.example.faisal.models.TruckItem;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;


/**
 * Created by faisal on 16/05/16.
 */
public interface RestApi {

    @GET("trucks")
    Call<TruckItem[]> getTrucks(@Query("latLng") String latLng, @Query("rad") String rad, @Query("q") String q);
}
