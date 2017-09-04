setopt nounset warncreateglobal extendedglob braceccl

use_slurm=false use_cuvid=false
output_template='${input:t:r}_${width}x${height}.${input:e}'

video_codec_name () {
    ffprobe -v error -select_streams v:0 \
        -show_entries stream=codec_name  \
        -of default=noprint_wrappers=1:nokey=1 \
        "$@"
}

is_h264 () { test h264 = "$( video_codec_name ${1?path of the media to test} )" }

encoder=( ffmpeg  -v error -nostats )
available_sizes=(
    320.240
    720.480
    1280.720
    1920.1080 )

workdir=.

# outch ... doesn't work with old versions of zsh :(
# alias @='for it'
# alias @-='while {read it}'

# TODO: XDG support ?
for it ( ~/.dtrt-ffpmeg(N) ) . $it


