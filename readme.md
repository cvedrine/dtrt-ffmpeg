# ffmpeg to do the right thing

this repo means to be a collection of high level commands on the top of ffmpeg.

# installation

just be sure the content of the bin directory is available somewhere in the `$PATH`.

Also, [zsh](http://www.zsh.org) and [mkxh](https://github.com/eiro/mkxh) are
required by some scripts so you need to install them too.

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
* some parameters to test/show

    # -c:v h264_nvenc -qmin 25 -qmax 27 -profile:v high
    # -preset fast # qualité inferieure? 2 passes ?
    # -profile:v high -pixel_format yuv420p
    # -c:a libfdk_aac -ar 48000 -ac 2 -ab 192
    # -movflags faststart -y output.mp4 # obligation pour streamer (moove atoms au début du fichier)
    # -vf scale_npp=320:240 -movflags faststart $1_240p.mp4

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

    # get the server keys if it's your first connection
    { for it ( hpc www ) ssh-keyscan -H $it } >> ~/.ssh/known_hosts

    # generate a service key for your app
    ssh-keygen -t ed25519 -N '' -C 'django@www' -f ffmpod

    # install the key with a restricted shell on hpc

    sed '/^ssh-/s/^/command="ffmpod" /' django.pub | ssh-copy-id -i hpc

    # TODO: configure ssh to avoid execution of remote commands with this key
    # good start:
    # https://serverfault.com/questions/726519/replacement-for-scponly-on-debian

    ssh-copy-id -i django.pub www

