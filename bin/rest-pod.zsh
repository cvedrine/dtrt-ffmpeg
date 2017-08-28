. rest-base.zsh

info () {
    rest_client+=("$WS/podspod/${1?id of the video}.json")
    shift
    "$@"
}

encoding_in_progress () {
    rest_client+=( -XPATCH -d '{ "encoding_in_progress" : '$1'  }' )
    shift
    "$@"
}


