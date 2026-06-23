# Artifact Appendix

**Paper title:** Beyond the Output: Inference Attacks on Private Set Union and
Multi-Key Private Matching

Requested Badge(s):
  - [x] **Available**
  - [x] **Functional**
  - [x] **Reproduced**

## Description

This repository contains the artifacts accompanying the paper "Beyond the Output: Inference Attacks on Private Set Union and Multi-Key Private Matching" by Andrea Raguso, Francesca Falzon, Tianxin Tang, and Kenneth Paterson, published at PETs 2026.
In the paper, we present several inference attacks, which allows an adversary that is allowed to interact with an ideal functionality to gain information about the non-adversarial inputs. We present attacks against the following functionalities: PSU, PSU-CA, the ideal functionality of Meta's multi-key PrivateID protocol (MK-PrivateID) $F_{MKPM}$, and the extended functionality of MK-PrivateID that includes additional protocol leakage $F_{L-MKPM}$.

This artifact repository contains implementations of said attacks and the corresponding functionalities, as well as a measurement infrastructure to evaluate the efficiency of our attacks. We measure both the attack runtimes, as well as the number of queries (ideal functionality evaluations) performed by the attack.

The artifact broadly has three stages: Data generation for the attacks against MK-PrivateID, performing measurements, and formatting data.
The final output of this artifact is a set of CSV files that contain the measurements we plot in our paper.

### Security/Privacy Issues and Ethical Concerns
Our artifact consists of simple measurements run locally on a single core (per experiment). Our attacks are run on synthetically generated data.
No security features are disabled and no sensitive data is being used.

## Basic Requirements

### Hardware Requirements
Our experiments can be carried out on any hardware with any number of cores.
To reduce the required runtime, we ran them on a server with the following specifications:
- 64 Core AMD EPYC 7742 2.25GHz Processor
- 512GB DDR4 3200MHz ECC Server Memory

**Paper Results:**
The full test suite we ran to obtain the results discussed in the paper requires 61 cores and used roughly 10GB of memory. 
The AMD EPYC 7742 processor has 64 physical and 128 logical cores, 
where the logical cores $i$ and $(i+64)$ are mapped to the same physical core.
We use this when assigning experiments to physical cores. 
Concretely, any given experiment is assigned to one physical core, i.e., the logical cores $i$ and $(i+64)$ for some $0\leq i\leq 60$ with `taskset -c <i>, <i+64> <command>`.

**Reduced Number of Cores**: Our test suite can run on any arbitrary number of cores $c$ at the cost of a less even distribution of the experiments. This approach also does not require the logical cores $i$ and $i+64$ to be mapped to the same physical core. However, it does require the logical cores $0,\dots,c$ to be available, see [Testing the Environment](#testing-the-environment).

### Software Requirements
1. **OS**: Our server has Ubuntu 24.04.4 LTS installed, although our experiment suite should run on other Linux installations as well.
The docker file we provide is based on Debian 13.5 "Trixie". 
2. **OS Packages**: We use `taskset` and `tmux` to assign the experiments to cores and keep sessions alive.
3. **Packaging**: We provide a Docker file with the necessary OS and Python packages installed. We use docker version 29.5.3.
4. **Programming language**: Our experiments are implemented in Python. We use Python 3.12.3.
5. **Packages**: We require the `Faker` package for generating synthetic data
6. **ML Models**: Our artifact requires no machine learning models.
7. **Data Sets**: Our data sets are generated synthetically and the script for doing so is contained in this artifact. However, since the generation takes some time, we include the data sets we used for our measurements in the artifact as well. They are located under `experiment_data/paper`.

### Estimated Time and Storage Consumption 
The artifact should consume no more than 1GB of disk space.
Assuming Docker is installed, the environment can be set up and verified in under 30 minutes.

Running the full measurement suite with the same number of iterations as we did in our paper takes 30 human-minutes and roughly 250 compute-hours.

We provide a reduced test suite which qualitatively reproduces our main results on smaller data sets and omits the experiments that are only discussed in the appendix of the paper. When executed in an environment with 16 cores, this takes roughly 30 human-minutes and 2 compute-hours.

## Environment

### Accessibility

This artifact is accessible from the public Github repository 
[https://github.com/deRaguso/mkpid-attacks-artifact](
https://github.com/deRaguso/mkpid-attacks-artifact/tree/main).

### Set up the environment

Start by cloning the repository and changing your current working directory to the repository.

```bash
git clone https://github.com/deRaguso/mkpid-attacks-artifact.git
cd mkpid-attacks-artifact
```

We provide a docker file with the necessary software dependencies, which should be built first. Please make sure that Docker is installed on your system.

```bash
docker build -t artifact_image .
```

launch the Docker container, attach the current working directory as a volume, set the context to be
that volume, and provide an interactive bash terminal.

```bash
docker run --rm -it -v ${PWD}:/workspaces/artifact \
    -w /workspaces/artifact \
    --entrypoint bash artifact_image
```

If you want to run the full (expensive) test suite, no further configuration is necessary. Should you want to run the experiments on a reduced number of cores, please set environment variable `NUM_CORES` to your preferred number of cores, e.g., $16$.

```bash
export NUM_CORES=16
```

To switch to the full test suite again, simply unset this variable with `unset NUM_CORES`.

### Testing the Environment
#### Full Test Suite
If you want to run the full experiment suite, please verify the environment by running `test_paper.sh`.

```bash
./test_paper.sh
```
The test script will first check that the logical CPUs 0-60 and 64-124 are available and that processes can be bound to them.
Next, it checks that tmux is functional by starting a dummy session that terminates instantly.
It then generates a range of small data sets, which are stored under `experiment_data/small`. Finally, our measurement suite is run on said data sets. 
The experiments are run sequentially, but each experiment is bound to the same processor as it's real (large) counterpart.
To ensure that any Python exceptions are clearly visible, we run the experiments without any informational console outputs apart from some rudimentary progress indicators. 
This should only take a few minutes, and you should see no error messages or exceptions.

#### Reduced Number of Cores
To verify that your environment is set up correctly to run the suite on a reduced number of cores, please execute

```bash
./test.sh
```

The script checks whether the environment variable `NUM_CORES` is set and if the cores 0, ..., (`NUM_CORES`-1) are available.
It then generates a range of small test data sets as in the previous section and executes the whole test suite on these small sets. You should see no warnings or errors. This should only take a few minutes, and you should see no error messages or exceptions.

The measurements are stored under `measurements/small`. There should be six CSV files, corresponding to the six attacks shown in the evaluation section of the paper, and one log file `cores.log`, see the outline below.
Finally, format the data with:

```bash
python3 format_measurements.py measurements/small
```

This should result in the file tree shown below. The directory `measurements/small` should contain 161 files. 

```
measurements/small
├── Baseline.csv
├── cores.log
├── MKPSI.csv
├── PSU.csv
├── PSUCA.csv
├── RecordEnumeration.csv
├── Snake.csv
└── formatted
    └── MKPSI_queries_over_mr
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── MKPSI_queries_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── MKPSI_recovery_over_QB
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── MKPSI_time_over_MR
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── MKPSI_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── PSUCA_queries_over_mr
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSUCA_queries_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── PSUCA_recovery_over_QB
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSUCA_time_over_MR
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSUCA_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── PSU_time_over_mr
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSU_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── recon_time_over_MR
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── recon_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
```

## Artifact Evaluation 

Our artifact should confirm the time and query measurements presented in Section 8 ("Experimental Evaluation") and Appendix H ("Additional Evaluation Results") in our paper. 
Since all experiments are executed simultaneously, we present this as one claim and describe our measurement suite as one large experiment.

### Main Results and Claims

#### Main Result: Attack Efficiency and Behavior

The main result we show with this artifact is that our attacks can be carried out efficiently, i.e., with only a small overhead on top of the normal protocol executions, and that the runtime and performed number of queries follow our theoretical predictions. For all attacks, we measure the runtime for varying parameters, see the experiment description below for more details.
For the attacks that perform an adaptive number of queries (ideal functionality evaluations), 
we additionally measure the number of queries, as well as the performance of the attack under limited query budgets.

In our work, we show the following plots, which we group by attack for this document. 

1. **PSU-Diff**: Runtimes largely follow from Python's implementation of set operations.
   1. Runtime over intersection ratio $\rho = |T\cap Y| / |T|$ (Figure 9a).
   2. Runtime over target set size $|T|$ (Figure 9b).
2. **PSU-CA-SearchTree**
   1. Number of queries over target set size $|T|$ (Figure 10a). Grows linearly.
   2. Runtime over intersection ratio $\rho$ (Figure 11a). Symmetric w.r.t. values of $\rho$: values of $\rho$ close to $0$ or $1$ yield smaller runtime measurements, values close to $0.5$ yield higher measurements.
   3. Runtime over target set size $|T|$ (Figure 11c). Grows linearly.
   4. Number of queries over intersection ratio $\rho$ (Figure 18a). Same behavior as in point 2.2.
   5. Recovered fraction of the intersection, difference, and total inferred membership information over allocated query budget (Figure 19) 
3. **MKPM-SearchTree** (called MKPSI in this artifact)
   1. Number of queries over target set size $|T|$ (Figure 10b). Grows linearly. 
   2. Runtime over match rate $\eta$ (Figure 11b). See PSU-CA-SearchTree, point 2.2.
   3. Runtime over target set size $|T|$ (Figure 11d). Grows linearly.
   4. Number of queries over match rate $\eta$ (Figure 18b). Same behavior as in points 2.2, 2.4, and 3.2.
4. **$T$-Reconstruction attacks** (Baseline, EnumAttack, SnakeAttack)
   1. Runtime over match rate $\eta$ (Figure 10a). Runtimes remain roughly constant.
   2. Runtime over target set size $|T|$ (Figure 10b). Grows linearly.

#### Experiment: Run Full Measurement Suite
This runs all measurements we present in the paper on the same data sets that we used to obtain our results. This is resource and time intensive, see [Experiment: Run Reduced Suite](#experiment-run-reduced-suite) for instructions on how to run the test suite on a smaller number of cores and how to the compute-time.
- Time: 20 human-minutes + 250 compute-hours. To shorten the compute-time, reduce the number of iterations (currently 50) in lines 6 and 13 in `run_experiments.sh`.

The experiment runs our measurement suite as described above on the data sets described in the paper.
For our attacks against the PSU and PSU-CA functionalities, the experiment data consists of a recovery set $Y$ of a fixed size and
a target set $T$ whose size we vary from $50\%$ to $150\%$ of $|Y|$ in $10\%$ increments. Both sets contain randomly sampled integers (without replacement).
Furthermore, we vary the intersection ratio $\rho := |T \cap Y|/|T|$ from $0\%$ to $100\%$, also in $10\%$ increments. For the attack against PSU-CA, we further vary the allocated query budget from $10\%$ to $100\%$ of the theoretical upper bound of queries in $10\%$ increments. This is not necessary for the attack against PSU, since it always performs two queries.
We set $|Y|=10^6$ for the attack against PSU and $|Y|=10^4$ for the attack against PSU-CA.

The data for the attacks against $F_{\textsf{L-MKPM}}$ is generated very similarly, with the exception that instead of simple sets, we now consider the sets of records located under `experiment_data/paper`. They were generated using

```bash
python3 gen_MKPID_data.py <destination_directory> 2 10000
```

Correspondingly, we vary the slightly more complicated match rate $\eta$ instead of the intersection ratio $\rho$, see Section 8 of the paper.
We set $|Y| = 10^4$.
For the MKPM-SearchTree attack (called MKPSI in this artifact),
we again vary the allocated query budget as described above.
Since the reconstruction attacks all only make a single query,
there is no need to limit their query budgets.

To start the experiments, run:
```bash
./run_experiments.sh
```

The measurement scripts repeat each experiment $50$ times. The raw measurements are stored in `measurements/large`.
This will take a long time. Once the command `tmux ls` shows no sessions of the form `mpmc-chunk<i>` or `PSU<i>`, all individual experiments are completed. 
You can then format the measured data.

```bash
python3 format_measurements.py measurements/large
```

The result is a similar file tree as shown in [Testing the Environment](#testing-the-environment).
The measurement data reported within those (formatted) files (in `measurements/large/formatted`) can be directly compared to the measurement data we use for the plots in our paper, which we provide in `measurements/paper`. 
However, this is a superset of the relevant data, as not all CSV files have a corresponding plot in the paper. The relevant files that do are the following:

```
measurements/paper/
   └── PSUCA_queries_over_mr,              (Figure 18a, Appendix H.1)
       MKPSI_queries_over_mr               (Figure 18b, Appendix H.1)
        ├── V10000T5000.csv
        ├── V10000T10000.csv
        └── V10000T15000.csv
   └── PSUCA_queries_over_n,               (Figure 10a, Section 8.3)
       MKPSI_queries_over_n                (Figure 10b, Section 8.3)
        ├── V10000MR0.0.csv
        ├── V10000MR0.1.csv
            ...
        └── V10000MR0.5.csv
   └── PSU_time_over_MR,                   (Figure 9a, Section 8.2)
       PSUCA_time_over_MR,                 (Figure 11a, Section 8.3)
       MKPSI_time_over_MR                  (Figure 11b, Section 8.3)
        ├── V10000T5000.csv
        ├── V10000T10000.csv
        └── V10000T15000.csv
   └── recon_time_over_MR/V10000T10000.csv (Figure 12a, Section 8.4)
   └── PSU_time_over_n,                    (Figure 9b, Section 8.2)
       PSUCA_time_over_n,                  (Figure 11c, Section 8.3)
       MKPSI_time_over_n,                  (Figure 11d, Section 8.3)
        ├── V10000MR0.0.csv
        ├── V10000MR0.1.csv
            ...
        └── V10000MR0.5.csv
   └── recon_time_over_n/V10000MR0.5.csv   (Figure 12b, Section 8.4)
   └── PSUCA_recovery_over_QB              (Figure 19, Appendix H.2)
        ├── V10000T5000.csv
        ├── V10000T10000.csv
        └── V10000T15000.csv
```

Since each experiment is repeated $50$ times and we report the average, we do not expect any large deviations from the provided results.
However, we did not run our experiments within a docker container, see the [Limitations](#limitations)

#### Experiment: Run Reduced Suite
- Time: 20 human-minutes + 2 compute-hours. 

Since our experiments are quite expensive, we provide instructions for running a reduced test suite on a smaller number of cores in this section. Concretely, the reduced test suite omits the experiments that are only discussed in the appendix of the paper, namely, the recovered fractions of the recovery set $Y$ by the PSU-CA and MKPID attacks under limited query budgets and the performance comparison of the alternative heuristics $p^-$ and $p^*$. Only the heuristic $p^+$, which is also discussed in the main body, is measured.

Execute the following instructions within the docker container.
Start by generating data sets of medium size:
```bash
python3 gen_MKPID_data.py --silent experiment_data/medium 2 1000
```

The data is generated in the same manner as described in the previous section, with the difference that $|Y|=10^3$.

Make sure that `NUM_CORES` is still configured (in case you terminated the container and started a fresh one): `export NUM_CORES=<#availble cores>`.
Run the experiments using the `run_artifact.sh` script. 
The `-e` and `-o` flags point the script to the experiment data and the output directory. 
`--m_PSU` and `--m_PSUCA` configure the size of the recovery set $|Y|$ for the PSU and PSU-CA experiments. 
`-r` specifies the number of iterations per experiment. 
Finally, if the `--omit_appendix` flag is set, the suite only runs the experiments that are discussed in the main body of the paper. This reduces the compute-time significantly, since some of the omitted experiments are quite expensive. 

```bash
./run_artifact.sh \
        -e experiment_data/medium/ \
        -o measurements/medium \
        --m_PSU 100000 \
        --m_PSUCA 1000 \
        -r 50 \
        --omit_appendix
```
You can check, which cores have terminated by either running `tmux ls` or examining the file `measurements/medium/cores.log`.

The measurements can then be formatted:
```bash
python3 format_measurements.py measurements/medium
```

As in the last section, this results in a file tree similar to the one shown in [Testing the Environment](#testing-the-environment). The files with corresponding plots in the main body of the paper are:

```
measurements/medium/
   └── PSUCA_queries_over_n,               (Figure 10a, Section 8.3)
       MKPSI_queries_over_n                (Figure 10b, Section 8.3)
        ├── V10000MR0.0.csv
        ├── V10000MR0.1.csv
           ...
        └── V10000MR0.5.csv
   └── PSU_time_over_MR,                   (Figure 9a, Section 8) 
       PSUCA_time_over_MR,                 (Figure 11a, Section 8) 
       MKPSI_time_over_MR,                 (Figure 11b, Section 8)
        ├── V10000T5000.csv
        ├── V10000T10000.csv
        └── V10000T15000.csv
   └── recon_time_over_MR/V10000T10000.csv (Figure 12a, Section 8), 
   └── PSU_time_over_n,                    (Figure 9b, Section 8)
       PSUCA_time_over_n,                  (Figure 11c, Section 8)
       MKPSI_time_over_n                   (Figure 11d, Section 8)
        ├── V10000MR0.0.csv
        ├── V10000MR0.1.csv
            ...
        └── V10000MR0.5.csv
   └── recon_time_over_n/V10000MR0.5.csv   (Figure 12b, Section 8)
```
Note that since the experiments were run on smaller data sets, the results described in [Main Result: Attack Efficiency](#main-result-attack-efficiency) are reproduced qualitatively, but cannot be quantitatively compared with the measurements from the paper, which we provide in `measurements/paper`.
However, we provide our results for running this reduced experiment in `measurements/medium_expected`.

## Limitations
For the measurements reported in the paper, we did not run our experiments in a docker container, but on the server's OS (Ubuntu 24.04.4 LTS) directly. While we do not expect it, this may result in differences in the runtime measurements. These are hard to estimate without re-running the experiments.

## Notes on Reusability
Our measurement infrastructure is flexible with respect to the considered input sizes. Running the attacks against MK-PrivateID with larger inputs can be done by generating larger data sets using `gen_MKPID_data.py`. 

Configuring the environment variable `NUM_CORES` and using the script `run_artifact.sh` allows our infrastructure to be run on an arbitrary number of cores and choosing the number of iterations per experiment, the data sets to be used for the experiments with the leakage-based attacks, and the recovery set sizes in the experiments with the PSU and PSU-CA attacks.

Our infrastructure includes code to measure the runtime and required number of queries for any attack, as well as re-usable implementations of the relevant ideal functionalities we consider in the paper. New attacks can therefore be added by placing their implementation in the `attacks` folder and extending the measurement scripts accordingly. 