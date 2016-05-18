package com.example.faisal.fd5;

import android.content.res.ColorStateList;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.Typeface;
import android.net.Uri;
import android.preference.PreferenceActivity;
import android.support.annotation.NonNull;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.support.v7.widget.SearchView;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import com.example.faisal.interfaces.RestApi;
import com.example.faisal.models.MetaData;
import com.example.faisal.models.ResponseData;
import com.example.faisal.models.TruckData;
import com.example.faisal.models.TruckItem;
import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.BooleanResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.UiSettings;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.Circle;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;


public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private UiSettings mUiSettings;
    private SupportMapFragment mapFragment;
    private SeekBar seekBar;
    private TextView textView;
    private RestApi restApi;
    private SearchView searchView;
    private String query;
    private LatLng prevCenter;
    private double progressVal;
    private Marker lastOpened = null;
    private Call<TruckItem[]> responseData;
    private Double topLat, botLat, leftLon, rightLon; //For maps boundaries

    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.

        //Initialize variables
        mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        textView = (TextView) findViewById(R.id.tv1);
        seekBar = (SeekBar) findViewById(R.id.sb1);
        searchView = (SearchView) findViewById(R.id.action_search);
        searchView.setHovered(true);
        mapFragment.getMapAsync(this);
        query = "";
        progressVal = 0;

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();


        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query2) {
                //Toast.makeText(getApplicationContext(), query, Toast.LENGTH_SHORT).show();
                searchView.clearFocus();
                query = query2;
                actionSearch();
                return true;
            }

            @Override
            public boolean onQueryTextChange(String newText) {
                query = newText;
                if (responseData != null)
                {
                    responseData.cancel();
                }
                return true;
            }
        });

        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                progressVal = progress;
                textView.setText(String.valueOf(progressVal/1000) + " KM" );
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

                actionSearch();
            }
        });

        //Retrofit integration

        Gson gson = new GsonBuilder().create();

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://46.101.87.96:8000/api/v1/")
                .addConverterFactory(GsonConverterFactory.create(gson))
                .build();

        restApi = retrofit.create(RestApi.class);


    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {

        mMap = googleMap;

        mUiSettings = mMap.getUiSettings();

        mUiSettings.setZoomControlsEnabled(true);
        mUiSettings.setScrollGesturesEnabled(true);
        mUiSettings.setZoomGesturesEnabled(true);
        mUiSettings.setTiltGesturesEnabled(true);
        mUiSettings.setRotateGesturesEnabled(true);

        mMap.moveCamera( CameraUpdateFactory.newLatLngZoom(new LatLng(37.773511230574215 , -122.41908721625805) , 14.0f) );

        LatLng curCent = mMap.getCameraPosition().target;

        mMap.addMarker(new MarkerOptions().position(curCent).title("YOU ARE HERE !").icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_VIOLET)));

        prevCenter = curCent;

        mMap.setOnCameraChangeListener(new GoogleMap.OnCameraChangeListener() {
            @Override
            public void onCameraChange(CameraPosition cameraPosition) {
                LatLngBounds bounds = mMap.getProjection().getVisibleRegion().latLngBounds;

                topLat = bounds.northeast.latitude;
                botLat = bounds.southwest.latitude;

                leftLon = bounds.southwest.longitude;
                rightLon = bounds.northeast.longitude;


                LatLng newCenter = mMap.getCameraPosition().target;



                if (!query.isEmpty() || progressVal!=0 || !newCenter.equals(prevCenter)) {
                    actionSearch();
                }

                prevCenter = newCenter;
            }


        });

        mMap.setOnMarkerClickListener(new GoogleMap.OnMarkerClickListener() {
            public boolean onMarkerClick(Marker marker) {
                // Check if there is an open info window
                if (lastOpened != null) {
                    // Close the info window
                    lastOpened.hideInfoWindow();

                    // Is the marker the same marker that was already open
                    if (lastOpened.equals(marker)) {
                        // Nullify the lastOpened object
                        lastOpened = null;
                        // Return so that the info window isn't opened again
                        return true;
                    }
                }

                // Open the info window for the marker
                marker.showInfoWindow();
                // Re-assign the last opened such that we can close it later
                lastOpened = marker;

                // Event was handled by our code do not launch default behaviour.
                return true;
            }
        });

        mMap.setInfoWindowAdapter(new GoogleMap.InfoWindowAdapter() {

            @Override
            public View getInfoWindow(Marker arg0) {
                return null;
            }

            @Override
            public View getInfoContents(Marker marker) {

                LinearLayout info = new LinearLayout(getApplicationContext());
                info.setOrientation(LinearLayout.VERTICAL);

                TextView title = new TextView(getApplicationContext());
                title.setTextColor(Color.BLACK);
                title.setGravity(Gravity.CENTER);
                title.setTypeface(null, Typeface.BOLD);
                title.setText(marker.getTitle());

                TextView snippet = new TextView(getApplicationContext());
                snippet.setTextColor(Color.GRAY);
                snippet.setText(marker.getSnippet());

                info.addView(title);
                info.addView(snippet);

                return info;
            }
        });



    }


    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Maps Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://com.example.faisal.fd5/http/host/path")
        );
        AppIndex.AppIndexApi.start(client, viewAction);
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Maps Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://com.example.faisal.fd5/http/host/path")
        );
        AppIndex.AppIndexApi.end(client, viewAction);
        client.disconnect();
    }


    private void actionSearch () {
        /**
         *Given Current LatLng, search radius, search query ,
         *populate the map with markers where Food Trucks are present
         *that satisfy parameters
         *
         *This method is triggered when any of the below actions occur:
         * -> User enters query
         * -> Search range is changed
         * -> Current screen bounds of the map are changed
         **/


        // Cancel any ongoing requests by Retrofit
        if(responseData != null)
        {
            responseData.cancel();
        }
        query = query.trim();



        mMap.clear();
        LatLng curCent = mMap.getCameraPosition().target;

        mMap.addCircle(new CircleOptions().center(curCent).radius(progressVal).strokeColor(Color.BLUE).fillColor(0x5586c5da).strokeWidth(0));

        mMap.addMarker(new MarkerOptions().position(curCent).title("YOU'R HERE !").icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_VIOLET)));



        if (!query.isEmpty())
        {
            query = query.replaceAll("[^A-Za-z0-9]", ",");
        }

        String latLng = String.valueOf(curCent.latitude)+","+String.valueOf(curCent.longitude);
        String rad = String.valueOf(progressVal/1000);

        responseData = restApi.getTrucks(latLng, rad, query);

        responseData.enqueue(new Callback<TruckItem[]>() {
            @Override
            public void onResponse(Call<TruckItem[]> call, Response<TruckItem[]> response) {

                TruckItem[] items = response.body();

                if (items.length == 0)
                {
                    Toast.makeText(getApplicationContext(), "No food here!", Toast.LENGTH_SHORT).show();
                }


                for(int i=0; i<items.length; i++)
                {
                    MetaData meta = items[i].getMeta();
                    TruckData data = items[i].getData();

                    LatLng place = new LatLng(Double.parseDouble(data.getLat()), Double.parseDouble(data.getLon()));
                    String isOpen = meta.getIsOpen();

                    String snippet = "Address: " + data.getAddress() + "\n" + "Timings: " + data.getDaysHours()
                            + "\n" + "Serves: " + data.getFoodItems();

                    if (isOpen.equals("YES"))
                    {
                        mMap.addMarker(new MarkerOptions().position(place).title(String.valueOf(data.getApplicant())).snippet("OPEN NOW!" + "\n" + snippet).icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN)));
                    }
                    else
                    {
                        mMap.addMarker(new MarkerOptions().position(place).title(String.valueOf(data.getApplicant())).snippet("CLOSED!" + "\n" + snippet).icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED)));
                    }
                }


            }

            @Override
            public void onFailure(Call<TruckItem[]> call, Throwable t) {

                if(call.isCanceled())
                {
                }
                else
                {
                    Toast.makeText(getApplication(), "No response received from server", Toast.LENGTH_SHORT).show();
                }
            }


        });

    }
}
