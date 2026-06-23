# README
This repository contains the artifacts accompanying the paper "Beyond the Output: Inference Attacks on Private Set Union and Multi-Key Private Matching" by Andrea Raguso, Francesca Falzon, Tianxin Tang, and Kenneth Paterson, published at PETs 2026.
In the paper, we present several inference attacks, which allows an adversary that is allowed to interact with an ideal functionality to gain information about the non-adversarial inputs. We present attacks against the following functionalities: PSU, PSU-CA, the ideal functionality of Meta's multi-key PrivateID protocol (MK-PrivateID) $F_{MKPM}$, and the extended functionality of MK-PrivateID that includes additional protocol leakage $F_{L-MKPM}$.

This repository contains implementations of said attacks and the corresponding functionalities, as well as a measurement infrastructure to evaluate the efficiency of our attacks. We measure both the attack runtimes, as well as the number of queries (ideal functionality evaluations) performed by the attack.

The artifact broadly has three stages: Data generation for the attacks against MK-PrivateID, performing measurements, and formatting data.
The final output of this artifact is a set of CSV files that contain the measurements we plot in our paper.

## Hardware Requirements
Our experiments can be carried out on any hardware with any number of cores.
To reduce the required runtime, we ran them on a server with the following specifications:
- 64 Core AMD EPYC 7742 2.25GHz Processor
- 512GB DDR4 3200MHz ECC Server Memory

## Software Requirements
The software in this repository was tested on Ubuntu 24.04.4 LTS, but should be executable on any Linux installation meeting the following requirements:
* Python 3.12
* `Faker` package for Python
* `tmux`
* `taskset`

We provide a Docker file meeting these requirements. If you use it, please make sure that Docker is installed on your system. We tested the code on Docker version 29.5.3.

## Installation
Download the repository and build the docker file:

```bash
git clone https://github.com/deRaguso/mkpid-attacks-artifact.git

cd mkpid-attacks-artifact

docker build -t artifact_image .
```

The experiments can be distributed over multiple cores. To configure the number of cores to be used, set the environment variable `NUM_CORES` accordingly:

```bash
export NUM_CORES=16 # distribute the different experiments over 16 cores
```

Verify your installation with the `test.sh` script. This will take a few minutes, since it executes all experiments on small test data sets. You should see no errors or warnings in the console.

```bash
./test.sh
```

## Running the Experiments
Start by generating data sets of an appropriate size using the `gen_MKPID_data.py` script. The script synthesizes pairs user data sets of different sizes and a varying fraction of shared information. We recommend data sets of size 1000 to keep the compute-time manageable.

```bash
python3 gen_MKPID_data.py --silent experiment_data/medium 2 1000
```

You can then run the experiments using `run_artifact.sh`. The script has the following configurations:

| Parameter                           | Description                                                  | Recommended Value        | Paper Value             |
| ----------------------------------- | ------------------------------------------------------------ | ------------------------ | ----------------------- |
| `-e`| Directory where the generated data sets are stored.           | `experiment_data/medium` | `experiment_data/paper` (provided) |
| `-o`| Location where measurement data should be stored.            | `measurements/medium`    | `measurements/paper`</br>(provided, do not overwrite)    |
| `--m_PSU`                           | Recovery set size $\|Y\|$ for PSU experiments                  | `100000`                   | `1000000`                 |
| `--m_PSUCA`                         | Recovery set size $\|Y\|$ for PSU-CA experiments               | `1000`                     | `10000`                   |
| `-r`  | Number of iterations per experiment                          | `50`                       | `50`                      |
| `--omit_appendix` | If present, some expensive experiments that are only discussed in the paper's appendix are omitted | set                  | not set             |

Note that running the experiments with the parameter set used for the results shown in the paper and without the `--omit_appendix` flag takes a very long time.
In our case, we distributed the experiments among 61 cores and the measurements required roughly 250 compute-hours per core.

Using the recommended values yields the command shown below. Make sure that the environment variable `NUM_CORES` is still set, in case you have terminated the container and started a fresh one in the mean time.

``` bash
./run_artifact.sh \
        -e experiment_data/medium/ \
        -o measurements/medium \
        --m_PSU 100000 \
        --m_PSUCA 1000 \
        -r 50 \
        --omit_appendix
```
This will take a while. With 16 cores on our server (see above), this took roughly 2 hours. If you do not use the `--omit_appendix` flag, the runtime will be drastically increased. You can check which cores are finished by either running `tmux ls` or inspecting the file `measurements/medium/cores.log`.
The raw measurements are stored in `measurements/medium`. You can format them into CSV files for plotting as follows:

```bash
python3 format_measurements.py measurements/medium
```

We provide the expected results for the parameters used above, as well as for the parameters used for the paper as indicated in the table, in `measurements/medium_expected` and `measurements/paper` correspondingly. 

Please consult [ARTIFACT-APPENDIX.md](ARTIFACT-APPENDIX.md) for more information on which values are being varied during the generation of data sets, which measurements are being performed, and how the formatted measurement data corresponds to the plots discussed in the paper.