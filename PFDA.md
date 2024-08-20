# Running AMPL on Precision FDA

## Requirements

- Account on pFDA / DNANexus
- Access to Workstations
- Access to `AMPL on pFDA` shared Space

## Running Jupyter Notebook

1. Create .env file with the following configuration:

```shell
export ENV=1.6.1                        # Any published version tag
export IMAGE_REPO=atomsci/atomsci-ampl  # Name of the dockerhub repository
export JUPYTER_PORT=8080                # Port 8080 is open by default on pFDA
export PLATFORM=cpu                     # Can be cpu / gpu
export WORK_DIR=work/                   # Working directory to use
export MODAC_USER=my-modac-username     # Username to https://modac.cancer.gov/
export MODAC_PASS=my-modac-pass         # Password to https://modac.cancer.gov/
```

2. Upload this to your Files section:

![.env](https://i.imgur.com/Jw8BLVp.png)

3. Launch the `pfda-ttyd` Workstation (located in Featured) with the latest `pfda-ttyd-ampl` snapshot

![Select pfda-ttyd Workstation](https://i.imgur.com/AOKH9dZ.png)
![Load Snapshot](https://i.imgur.com/xoveFH2.png)

4. Wait for the Workstation to start. It takes a few minutes for it to reach the `Running` state. Click on `Open Workstation`.

5. Run the `./start` command

![Run start_pfda](https://imgur.com/pAh8GQG.png)

**_Note:_** The start command can take ~5m to run, depending on which instance type is used. The GPU docker image is approx 8GB so it will take longer.

6. Copy the Jupyter Notebook URL

![Jupyter Notebook](https://i.imgur.com/PuXkrmx.png)

7. Replace `127.0.0.1` with the workstation host and add `:8080` to the end. Enter this into the browser URL.

**_Note:_** The Precision FDA Environment has a very short lived session. If you have a slow network connection, you may be logged out before the

## Importing Existing Models

There are a couple options for importing an pre-trained model. Most models come in the form of a `.tar.gz`. The first steps will be to create a workstation using the instruction above. Once this workstation is running, and open (Step 4), proceed as follows:

1. Upload trained models to pFDA using the Files interface. Click on the `Add Files` button and follow the dialog to upload to pFDA.

![Pre-trained model example](https://i.imgur.com/W7rfzaD.png)

2. In the Workstation tab, cd into a directory called `work/` by running the following:

```
cd work
```

![mkdir command](https://i.imgur.com/4Xq9WPc.png)

3. Download the model to the Workstation inside the `work/` directory, and return to the home directory

```
pfda download <name_of_model.tar.gz>
cd ..
```

![pfda download command](https://i.imgur.com/lvbYRRi.png)

4. Continue from Step 5 above to run your notebook

# Updating the AMPL Snapshot on Precision FDA

There are 2 scripts which are used to help with installing and running AMPL on pFDA:

- [install_pfda](./install_pfda)
  This script was used to bootstrap the initial snapshot. The only major requirement for running pFDA is Docker. Hopefully this script should not need to updated, but in the event that it does, you will want to append any necessary commands to this script so that we can track it. Once the script has been updated, copy it from version control, and paste it into the Workstation. After running all commands, create a new snapshot with a new version.
- [start_pfda](./start_pfda)
  This is the script which is instructed to the end-user to run once they've downloaded all the files which they need for their Workstation. The purpose of this script is to download a fresh docker image and clone the latest `master` for AMPL before starting the Jupyter Notebook. Because of the way this script will call `make`, some parts can be updated in version control. Similarly to the other script, once changes have been made, a new snapshot will be necessary.

# Other Notes about pFDA

## Re-attaching to a running Workstation

![Getting Logged Out](https://imgur.com/UqxlHay.png)

PrecisionFDA has a very short lived session. If you get logged out at any point, you should be able to login again and attach to your Workstation.

1. You can safely close any tabs with an old session
2. Login to pFDA
3. Connect to the running Workstation
4. Run the following command:

```shell
docker ps
```

5.  If your output shows no running containers, it will look like this:
    ![No Running Containers](https://imgur.com/I7qNx2K.png)

You can restart the notebook by running

```shell
cd AMPL/
. .env                    # Required to load configuration
make jupyter-notebook
```

![Restarting Jupyter Notebook](https://imgur.com/WV41mJq.png)

Otherwise if you have a running container, your `docker ps` output will look something like this:
![Running container](https://imgur.com/noyeNUM.png)

Then we can simply output the logs from it by running the following:
docker logs:

```
docker logs $(docker ps -q)
```

From here we can copy the URL for the Jupyter Notebook
![Get connection information for running container](https://imgur.com/DKz11Ri.png)
