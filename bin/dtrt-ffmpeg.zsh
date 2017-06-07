setopt nounset warncreateglobal

use_slurm=false
use_cuvid=false
workdir=.

alias @='for it'
alias @-='while {read it}'

@ ( ~/.dtrt-ffpmeg(N) ) . $it

