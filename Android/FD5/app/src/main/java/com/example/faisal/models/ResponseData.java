package com.example.faisal.models;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by faisal on 16/05/16.
 */
public class ResponseData {

    List<TruckItem> trucks;

    /*
    public ResponseData()
    {
        trucks = new ArrayList<TruckItem>();
    }
    */
    public List<TruckItem> getTrucks() {
        return trucks;
    }
}
