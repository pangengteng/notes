package Java;

public class MultiThread {
    private static void task(String threadName, Object lock) {
        for (int i = 0; i < 3; i++) {
            synchronized (lock) {
                System.out.println("thread " + threadName + " " + i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                lock.notify();
                try {
                    lock.wait();
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            
        }
    }
    public static void main(String[] args) {
        Object lock = new Object();
		Thread a = new Thread(new Runnable() {

            @Override
            public void run() {
                task("A", lock);
            }
            
        });

        Thread b = new Thread(new Runnable() {

            @Override
            public void run() {
                
                task("B", lock);
            }
            
        });

        a.start();
        b.start();
	}
}
