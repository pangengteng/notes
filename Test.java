import java.util.ArrayList;
import java.util.List;

public class Test {
    public List<String> readBinaryWatch(int num) {
        List<String> res = new ArrayList<>();
        dfs(res, num, 0, 0, 0);
        return res;
    }

private void dfs(List<String> res, int num, int start, int hour, int minute) {
    if (num == 0) {
        if (hour < 12 && minute < 60) {
            res.add(String.format("%d:%02d", hour, minute));
        }
        return;
    }
    for (int i = start; i < 10; i++) {
        if (i < 4) {
            dfs(res, num - 1, i + 1, hour + (1 << i), minute);
        } else {
            dfs(res, num - 1, i + 1, hour, minute + (1 << (i - 4)));
        }
    }
}

    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.readBinaryWatch(2));
    }
}