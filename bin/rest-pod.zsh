. rest-base.zsh

TOKEN=${POD_REST_TOKEN?please set POD_REST_TOKEN variable} \
URL=${POD_REST_URL?please set POD_REST_URL variable}       \
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

overview_send () {
    scp $from $to
    pod PATCH "{ \"overview\": \"$to\" }" info $id }



