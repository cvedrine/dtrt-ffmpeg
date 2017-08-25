# this is a base of a rest client using curl
# it should be copied in a local scope so
# you can extend it to handle a complete request
# rest() does it

_rest_client=(
    curl
    -s
    -H "Content-Type:application/json"
    -H "Accept: application/json" )

rest () {
    # create a local copy which would be modified by ...
    typeset -a rest_client
    rest_client=( $_rest_client )

    # ... the next wrapper you want
    "$@"

    $rest_client
}

pass () { rest_client+=( "$@" ) }

