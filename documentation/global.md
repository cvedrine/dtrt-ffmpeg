# Fonctionnement général

`pod` transmet les ordres d'encodage à slurm en contactant la commande
`process` installée sur `hpc`.

# infrastructure globale

soient:

* django-pod l'instance de pod installée sur la machine `pod.example.com`
  et executée avec le compte django.
* hpc (`hpc.example.com`) la machine qui lance les jobs d'encoding sur
  une ferme slurm.

django-pod a été installé avec pydiploy, la commande a executer pour lancer une
tache d'encoding est configurée comme suit

    ENCODE_COMMAND = 'ssh hpc %s'

dans le fichier `~django/pod.example.com/current/pod_project/settings/prod.py`.
hpc doit être correctement configurée comme suit dans `~django/.ssh/config`

    host hpc
    hostname hpc.example.com
    user pod
    IdentityFile ~/.ssh/django

`hpc:.ssh/authorized_keys` comprendra la ligne

    command="bin/process" ssh-ed25519 AAAAC3N...

pour autoriser la clef django à se connecter.

En retour, `hpc:.ssh/config` contient

    host pod
    hostname pod.example.com
    IdentitiesOnly yes
    user django
    IdentityFile ~/.ssh/django

`pod:.ssh/authorized_keys` comprendra la ligne

    command="navigator-wrapper" ssh-ed25519 AAAAC3N...

# commandes manuelles pour test

pour encoder une video

    ssh hpc ${video_id}

# Troubleshooting

* est-ce que le job est arrivé sur hpc ?

    ssh hpc ls -d pod.${job_id}.\*

    entrer dans le repertoire

    doit afficher le nom des répertoires





















