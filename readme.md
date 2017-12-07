# ffmpeg to do the right thing

in the current documentation, pod and pod machines refers
to `pod.example.com` and `pod.example.com` as they appear
in the synopsis.

# synopsis

say we have 2 machines

* `pod.example.com` which runs an instance of esup pod.
* `pod.example.com` which can run jobs to a slurm farm

    +----------------------------------------+
    | pod.example.com                        |
    | +--------------+ +------------------+  |
    | | pod fcgi     | | navigator-wrapper|  |
    | |             <---                  |  |
    | | (1)          | |                  |  |
    | +-|------------+ +-------^----------+  |
    +---|----------------------|-------------+
        |                      |
    +---|----------------------|-------------+
    | +-v------------+ +-------|-------+     |
    | | process      | |       (3)     |     |
    | |          (2) --->              |     |
    | |              | |  dtrt-ffmpeg  |     |
    | +--------------+ +---------------+     |
    | pod.example.com                    |
    +----------------------------------------+

when a video is uploaded to `pod`:

the fcgi contact the `process` program via ssh

    ssh pod.example.com ${video_id}

`process` creates a directory named after

    pod.${video_id}.${date_of_creation}.${random_key}

this directory where all the artefacts for the script
will be created by `dtrt-ffmpeg`. as example

    pod.19050.2017-10-17.09:29.RpNU/
        X                 # the arguments passed to process
        1621491_700p.mp4  # the original videos
        log.stderr        # capture of standard error
        log.stdout        # capture of standard output
        pod.json          # json from the pod instance
        videos/
            command       # encoding command actually run by slurm
            downscaled    # the sizes to be downscaled
            strips/       # the strips used for overview
            overview.jpg  # the overview of the video
            1621491_700p_320x240.mp4  # actual artefacts
            1621491_700p_1280x720.mp4

# requirements

## ssh access

both pod and encoder must be available

    for it ( encoder pod ) {
        # get the server keys if it's your first connection
        ssh-keyscan -H $it } >> ~/.ssh/known_hosts
        # authorize your key on the server
        ssh-copy-id $it
    }

## on pod

* must be installed with the same user than the django application one
  (virtualenv available)
* `zsh` (at least version `5.0.2`) available (don't need to be the login shell)
* `~/bin` as a part of your `$PATH`

## on encoder

* `zsh` (at least version `5.0.2`) available (don't need to be the login shell)
* `~/bin` as a part of your `$PATH`
* ffmpeg available in your `$PATH`

    # generate a service key for your app
    ssh-keygen -t ed25519 -N '' -C 'django@www' -f ffmpod

    # install the key with a restricted shell on hpc

    sed '/^ssh-/s/^/command="ffmpod" /' ffmpod.pub | ssh pod ''

# installation


## agenda

* make sure the pod service is available from pod
    * copy the service public key on pod
    * setup a `host pod` in the pod
    * authorize the service key in pod

* make sure the encoder service is available from pod
    * copy the service public key on pod
    * setup a `host encoder` in the pod
    * authorize the service key in encoder

* make sure the content of `bin/` is available in the `$PATH` of both machines.



# extra notes

## Using slurm

create a wrapper for the commands you need using the SBATCH instructions.

    #SBATCH -p standardqueue  # our standard queue
    #SBATCH -N 1-1            # min-max nodes to use
    #SBATCH -t 24:00:00       # estimated time (helps the scheduler)
    #SBATCH --gres=gpu:1      # we need *at least* 1 GPU
    #SBATCH -o log.stdout
    #SBATCH -e log.stderr
    #SBATCH # can send emails too!

## Using modules

you probably should edit your ̀`.mkshrc` or your `.zshenv`

    . /usr/local/Modules/latest/init/ksh
    module load encoding/ffmpeg

# documentation

is written using the POD format in the scripts themselves so please use `perldoc` to read them.

# todo

* improve documentation
* do some benchmarks to compare CPU, GPU and slurm solutions
* do some benchmarks to compare slurm with one process by downscale
* very desapointed by GPU perfomance, `nvidia-smi` seems to show that GPU is underused.
* autodect GPU environment to use the best option it could
* use of fallback strategies when encoding failed
* some parameters to test/show
* add a flag to force the reencoding of files
* add a param to change the output folder
* add a --help option
* add a --verbose option

# ssh configuration (restricted shell)

let's say i want to install ffmpod and you start with those lines in your `~/.ssh/config` file

    host www
    hostname www.example.com
    user django

    host hpc
    hostname hpc.example.com
    user django

* django is running with django@www.example.com
* ffmpod is running with ffmpod@hpc.example.com
* your personnal keys are authorized for these 2 accounts


    # TODO: configure ssh to avoid execution of remote commands with this key
    # good start:
    # https://serverfault.com/questions/726519/replacement-for-scponly-on-debian

## With Slurm

create a wrapper for the commands you need using the SBATCH instructions.

    #SBATCH -p standardqueue  # our standard queue
    #SBATCH -N 1-1            # min-max nodes to use
    #SBATCH -t 24:00:00       # estimated time (helps the scheduler)
    #SBATCH --gres=gpu:1      # we need *at least* 1 GPU
    #SBATCH -o log.stdout
    #SBATCH -e log.stderr
    #SBATCH # can send emails too!

### Using modules

you probably should edit your ̀`.mkshrc` or your `.zshenv`

    . /usr/local/Modules/latest/init/ksh
    module load encoding/ffmpeg

## Without Slurm

*WARNING* please don't try another shell than `zsh` (at least version `5.0.2`)

* add `bin` in your `$PATH`
* export those 2 variables with the values relevant to your site

# dtrt-ffmeg-downscale

consult the POD of each commands for more details.

# test from pod

    ssh -o IdentitiesOnly=yes -i ~/.ssh/django hpc  19314
    Submitted batch job 3185644

# global infrastructure in french (WIP)

see [documentation/global.md](documentation/global.md)

