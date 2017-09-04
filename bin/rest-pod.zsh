. rest-base.zsh

URL=https://pod-ws-test.u-strasbg.fr/webservice \
    TOKEN=739168987f8b65829c0c4eb94620784ac9c2f750 \
    set_rest_service pod

info () {
    rest_client+=("$URL/podspod/${1?id of the video}.json")
    shift
    "$@"
}

encoding_in_progress () {
    rest_client+=( -XPATCH -d '{ "encoding_in_progress" : '$1'  }' )
    shift
    "$@"
}

pod_encodingtypes        () { route $URL/coreencodingtype "$@" }
pod_encodings            () { route $URL/podsencodingpods "$@" }
select_pod_encodingtypes () { jq " .results[] | select( ${1?selector} ) " }

as_height_id () {
        jq --raw-output ' .[]
        # | select( .output_height == 1080 )
        | @text "\(.output_height) \(.id)" '
}



