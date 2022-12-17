public class Permutations {
    private int[][] permutationsArray;
    
    /**
     * Prints the given array elements in format {elemnt1, element2, ...}
     * 
     * @param a the array to print elements of
     */
    private static void printArray(int[] a) {
        System.out.print("{");
        for (int i = 0; i < a.length; i++) {
            if (i == a.length-1)
                System.out.print(a[i]);
            else
                System.out.print(a[i] + ",");
        }
        System.out.println("}");
    }
    
    /**
     * Returns the given array elements in String format "{elemnt1, element2, ...}"
     * 
     * @param a the array 
     * @return string with the elements of the given array
     */
    private static String arrayToString(int[] a) {
        String output = "{";
        for (int i = 0; i < a.length; i++) {
            if (i == a.length-1) 
                output = output.concat(a[i] + "}");
            else
                output = output.concat(a[i] + ",");
        }
        return output;
    }
    
    /**
     * Returns a copy of the given array of arrays that points to a different memory address.
     * 
     * @param originalArray the original array to copy
     * @return a copy of the given originalArray
     */
    private static int[][] copyArrayOfArrays(int[][] originalArray) {
        int[][] newArray = new int[originalArray.length][originalArray[0].length];
        
        for (int i=0; i < originalArray.length; i++) {
            int[] copy = originalArray[i].clone();
            newArray[i] = copy;
        }
        
        return newArray;
    }
    
    /**
     * Returns the factorial of the given number. 
     * 
     * @param num the number to find it's factorial
     * @return factorial of given num.
     */
    private int getFactorial(int num) {
        int fac = 1;
        
        for (int i =2; i <= num; i++)
            fac *= i;
        return fac;
    }
    
    /**
     * Returns a single permuation of n!
     * 
     * @param n the number to create an n! permuation for.
     * @return single permuation of n!
     */
    private int[] generateFirstPermutation(int n) {
        int[] permutation = new int[n];
        for (int i = 0; i < n; i++)
            permutation[i] = i+1;
        return permutation;
    }
    
    /**
     * Returns an array with n+1 elements whos values are 0 to n. 
     * 
     * @param n the maximum number to get generated in the returned array
     * @returns an array with n+1 elements whos values are all numbers from 0 to n
     */
    private int[] generateIterationControlArray(int n) {
        int[] p = new int[n+1];
        for (int i = 0; i <= n; i++)
            p[i] = i;
        return p;
    }
    
    /**
     * Exchanges the values in the array at the given indexes.
     * 
     * @param array the array to swap values in
     * @param index1 the index whos new value is array[index2]
     * @param index2 the index whos new value is array[index1]
     */
    private static void exchange(int[] array, int index1, int index2) {
        int temp = array[index1];
        
        array[index1] = array[index2];
        array[index2] = temp;
    }
    
    /**
     * Constructor of Permutations, if no n is given will return permutation of 1!
     */
    public Permutations() {
        permutationsArray = new int[1][1];
        int[]element = {1};
        permutationsArray[0] = element;
    }
    
    /**
     * Constructor of Permutations. Fills the permutationsArray with all possible n! permutations.
     * 
     * @param n the number to create all n! permutations out of.
     */
    public Permutations(int n) {
        // intializing variables
        int factorN = getFactorial(n), tempElement, index = 1;
        permutationsArray = new int[factorN][n];
        boolean allPermutationsCreated = false;
        // intializing the first permutation
        int[] currentPermutation = generateFirstPermutation(n);
        
        
        // start of by adding the first permutation to the final result
        permutationsArray[0] = currentPermutation.clone();

        if (n > 1) {
            int[] iterationControlArray = generateIterationControlArray(n);
            int j, i = 1;
            // using QuickPerm Algorithm to find all permutations
            while (i < n) {
                iterationControlArray[i]--;
                
                if (i % 2 != 0)
                    j = iterationControlArray[i];
                else
                    j = 0;
                exchange(currentPermutation, j, i);
                // store each switch as a new permutation
                permutationsArray[index] = currentPermutation.clone();
                index++;
                
                i = 1;
                while (iterationControlArray[i] == 0) {
                    iterationControlArray[i] = i;
                    i++;
                }
            }
        }
    }
    
    /**
     * Returns a string representation of all permutations  
     * 
     * @override toString in class java.lang.Object
     * @return a string of all permutations For example: {1, 2} {2, 1}
     */
    public String toString() {
        String output = "";
        
        for (int[] permetation : permutationsArray) 
            output = output.concat(arrayToString(permetation) + " ");
        
        return output;
    }
    
    /**
     * Returns copy of the permutationsArray with a different memory address.
     * 
     * @return copy of the permutationsArray
     */
    public int[][] getPermutations() {
        return copyArrayOfArrays(permutationsArray);
    }
}