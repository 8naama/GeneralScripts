# Generate n! Permutations 
This Class generates n! Permutations for a given n using QuickPerm algorithem.

## Prerequisites
You will need java v1.8.0_301

## Setup
1. Create instance of the Permutations class with the wanted n. For example:
```java
Permutations p = new Permutations(8);
```
2. You can print all permutations by printing the instance:
```java
System.out.println(p);
```
3. You can use the permutations by retreving the created object (an array of arrays), each sub-array holds a different permutation. Example:
```java
int[][] myPermutations = p.getPermutations();
```

## Note
Please note that the larger n is, the longer it will take to run. Some n values my be too large to handle (for example 15!)
