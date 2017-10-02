# everything must be configuration
# ssh-argv0 must be used?

export POD=${POD:-pod}

add_encoding_for   () { ssh $POD add_encoding_for "${(q)@}" < $3 }
add_overview_for   () { ssh $POD add_overview_for "${(q)@}" < $2 }
add_mp3_for        () { ssh $POD add_overview_for "${(q)@}" < $2 }
set_thumbnails_for () { tar cf - "${(@)argv[2,5]}" | ssh $POD set_thumbnails_for $@ }
