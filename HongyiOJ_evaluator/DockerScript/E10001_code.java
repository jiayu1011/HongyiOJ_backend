import java.util.Scanner;

public class E10001_code {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        Solution(n);

    }

    public static void Solution(int n){
        if(n==0){
            System.out.println(n);
            return;
        }

        int temp = Math.abs(n);

        int sum = 0;
        while(temp>0){
            int cur = temp%10;
            temp /= 10;
            sum = sum*10 + cur;
        }

        if(n>0){
            System.out.println(sum);
        } else {
            System.out.println(-sum);
        }

    }
}
