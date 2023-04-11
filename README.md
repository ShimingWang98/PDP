# Test practical privacy using DP-Sniper

In practical scenarios, there is gap between the theoretical guarantee $\epsilon$ and the and the adversary maximal gain $\xi^\ast$, so we use a practical attack method DP-Sniper to test practical privacy.



## Basic Usage

The following command tests the differential privacy of the original Laplace mechanism,
explained in detail in file [example.py](dpsniper/example.py):

```bash
python example.py --eps=0.1
```

This commands stores temporary outputs and log files to the folder
`example_outputs` of the current working directory.

If you want to test the ablation privacy study on varying $c$ of the practical Laplace mechanism, the command is as follow (c=0.05,c'=1):

```bash
python example.py --c_prime=0.1 --eps=2 --r=1.76
```

If you want to compare the privacy of practical Laplace mechanism and Gaussian mechanism with the same utility, you can use:

```bash
python example.py --eps=0.1 --c_prime=0.1 --eps=2 --r=1.76 --compare_gaussian=1
```

If you want to fix the number of samples the attacker can use instead of following the guideline 1, you can use:

```bash
python example.py --eps=0.1 --c_prime=0.1 --eps=2 --r=1.76 --N=10000
```



## Publication

These codes use the approach presented in the following research paper:

> B. Bichsel, S. Steffen, I. Bogunovic and M. Vechev. 2021.
> DP-Sniper: Black-Box Discovery of Differential Privacy Violations using Classifiers.
> In IEEE Symposium on Security and Privacy (SP 2021).

The main algorithms DD-Search and DP-Sniper from the paper can be found in
[search/ddsearch.py](dpsniper/search/ddsearch.py) and
[attack/dpsniper.py](dpsniper/attack/dpsniper.py), respectively.
