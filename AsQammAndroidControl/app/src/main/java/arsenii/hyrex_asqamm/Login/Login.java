package arsenii.hyrex_asqamm.Login;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Color;
import android.icu.text.UnicodeSetSpanner;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.io.*;
import java.net.*;

import arsenii.hyrex_asqamm.R;

public class Login extends AppCompatActivity {

    int l1;
    int l2;
    String text = "";

    EditText login;
    EditText password;
    Button sign;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
        login = findViewById(R.id.login);
        password = findViewById(R.id.password);
        sign = findViewById(R.id.sign);

        ConnectivityManager cm = (ConnectivityManager)getApplicationContext().getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo nInfo = cm.getActiveNetworkInfo();
        if (nInfo != null && nInfo.isAvailable() && nInfo.isConnected()) {
            try{
                URL url=new URL("http://www.javatpoint.com/java-tutorial");
                URLConnection urlcon=url.openConnection();
                Toast.makeText(getApplicationContext(), "Я подключился!", Toast.LENGTH_LONG).show();
                InputStream stream=urlcon.getInputStream();
                Toast.makeText(getApplicationContext(), "Input stream", Toast.LENGTH_LONG).show();

                int i;
                while((i=stream.read())!=-1){
                    text += (char)i;
                }
            }catch(Exception e){Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();}
            Toast.makeText(getApplicationContext(), text, Toast.LENGTH_LONG).show();
        } else {
            Toast.makeText(getApplicationContext(), "Сервер не доступен, проверьте подключение к интернету", Toast.LENGTH_LONG).show();
        }
    }
}
