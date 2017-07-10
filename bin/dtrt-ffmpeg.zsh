setopt nounset warncreateglobal extendedglob braceccl

use_slurm=false use_cuvid=false
output_template='${input:t:r}_${width}x${height}.${input:e}'

encoder=( ffmpeg )
available_sizes=(
    320.240
    720.480
    1280.720
    1920.1080
)

workdir=.

# outch ... doesn't work with old versions of zsh :(
# alias @='for it'
# alias @-='while {read it}'

# TODO: XDG support ?
for it ( ~/.dtrt-ffpmeg(N) ) . $it
