package studio.bytesize.skrrtbot;

import java.util.Random;

public class Rand {
    public static Random r = new Random();

    public static int getRand(int min, int max) {
        return r.nextInt((max - min) + 1) + min;
    }
}
