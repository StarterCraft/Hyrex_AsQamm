package arsenii.hyrex_asqamm.Login;

import android.os.AsyncTask;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

import arsenii.hyrex_asqamm.R;

public class Login extends AppCompatActivity {

    String text = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        System.out.println(new AsyncRequest().execute("123", "/ajax", "foo=bar"));

    }
    class AsyncRequest extends AsyncTask<String, Integer, String> {

        @Override
        protected String doInBackground(String... arg) {
            URL yahoo = null;
            try {
                yahoo = new URL("http://www.yahoo.com/");
            } catch (MalformedURLException e) {
                e.printStackTrace();
            }
            URLConnection yc = null;
            try {
                yc = yahoo.openConnection();
            } catch (IOException e) {
                e.printStackTrace();
            }
            BufferedReader in = null;
            try {
                in = new BufferedReader(
                        new InputStreamReader(
                                yc.getInputStream()));
            } catch (IOException e) {
                e.printStackTrace();
            }
            String inputLine = "";
            String text = "";

            while (true) {
                try {
                    if (!((inputLine = in.readLine()) != null)) break;
                } catch (IOException e) {
                    e.printStackTrace();
                }
                text += inputLine;
            }
            try {
                in.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return text;
        }

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            text = s;
        }
    }

}
