
# this is a base of a rest client using curl
# it should be copied in a local scope so
# you can extend it to handle a complete request
# rest() does it

REST_CLIENT_BASE=(
    curl -s
    -H "Content-Type:application/json"
    -H "Accept: application/json" )

# DEPRECATED! use set_rest_service
rest () {
    # create a local copy which would be modified by ...
    typeset -a rest_client
    rest_client=( $_rest_client )
    # ... the next wrapper you want
    "$@"
    $rest_client
}

route () {
    rest_client+=( ${1?route to contact for $URL} )
    shift
    "$@"
}

pass  () { rest_client+=( "$@" ) }
POST  () { rest_client+=( -X POST -d "$1" ) ; shift ;"$@" }
PATCH () { rest_client+=( -X PATCH -d "$1" ) ; shift ;"$@" }

# pod () {
#     local URL="https://pod-ws-test.u-strasbg.fr/webservice"
#     rest_client+=( -H "Authorization:Token 739168987f8b65829c0c4eb94620784ac9c2f750" )
#     "$@"
# }

set_rest_service () {
    local name=$1 ; shift
    test ${TOKEN:-} && set -- -H "Authorization:Token ${TOKEN}" "$@"
    eval $name'() {
        local URL='${(q)URL?the base URL of the web service}'
        local TOKEN='${(q)TOKEN:-}'
        typeset -a rest_client
        rest_client=('"${(@q)REST_CLIENT_BASE}" "${(q)@}"')
        "$@"
        if { ${DRYRUN:-false} } { echo ${rest_client} } else { ${rest_client} }
    }'
}

