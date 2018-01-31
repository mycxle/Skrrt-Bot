package studio.bytesize.skrrtbot.util;

import java.io.BufferedReader;
import java.io.FileReader;

public class Secret {
    private static String TOKEN = "null";

    public static String getToken() {
        if(TOKEN.equals("null")) {
            try {
                BufferedReader br = new BufferedReader(new FileReader("token.txt"));
                try {
                    StringBuilder sb = new StringBuilder();
                    String line = br.readLine();

                    while(line != null) {
                        sb.append(line);
                        sb.append(System.lineSeparator());
                        line = br.readLine();
                    }
                    TOKEN = sb.toString();
                    TOKEN = TOKEN.substring(0, TOKEN.length() - 2);
                } finally {
                    br.close();
                }
            } catch(Exception e) {
                e.printStackTrace();
            }
        }

        return TOKEN;
    }
}
