# new-challenge

[Problem](https://github.com/uclaacm/lactf-archive/tree/main/2023/misc/new-challenge)

This is actually not a writeup, but a supplement to the solution given by the challenge developer. I don't know bash at all.

Run the git command `git clone git://lac.tf:31152/new-challenge.git` given in the challenge description, and we get a git repository. There is a bash script called "pre-receive", cat it to see what's inside.

```bash
#!/bin/bash

set -e

declare -A LACTF_CHALL_WRITERS
LACTF_CHALL_WRITERS["Aplet123"]="aplet@lac.tf"
LACTF_CHALL_WRITERS["alec"]="burturt@lac.tf"
LACTF_CHALL_WRITERS["Alexander Zhang"]="alex@lac.tf"
LACTF_CHALL_WRITERS["Jason Liu"]="flamingsnowman@lac.tf"
LACTF_CHALL_WRITERS["Arc-blroth"]="arcblroth@lac.tf"
LACTF_CHALL_WRITERS["Benson Liu"]="bensonhliu@lac.tf"
LACTF_CHALL_WRITERS["Arnav Vora"]="avdestroyer@lac.tf"

HAS_BLIUTECH_COMMIT=false

while read oldrev newrev refname; do
  if echo "$oldrev" | grep -Eq '^0+$'; then
      commits=$(git rev-list $newrev --not --branches=*)
  else
      commits=$(git rev-list ${oldrev}..${newrev})
  fi
  for commit in $commits; do
    # access control: only allow LA CTF challenge writers
    name_email=("$(git show $commit --pretty=format:'%an' | sed '1!d')" "$(git show $commit --pretty=format:'%ae' | sed '1!d')")
    if [ "${LACTF_CHALL_WRITERS["${name_email[0]}"]}" != "${name_email[1]}" ]
    then
      echo >&2 "error: not an LA CTF challenge writer"
      exit 1
    fi
    if [ "${name_email[0]}" == "Benson Liu" ]
    then
      HAS_BLIUTECH_COMMIT=true
    fi
  done
done

if $HAS_BLIUTECH_COMMIT
then
  echo $FLAG
fi

# LA CTF: don't *actually* allow writing
echo "don't feel like talking to the disk today, sorry"
exit 1
```

It may be clearer to give an example of the [read](https://www.baeldung.com/linux/read-command) command.

```bash
$ read input1 input2 input3
baeldung is a cool tech site # what we type
$ echo "[$input1] [$input2] [$input3]"
[baeldung] [is] [a cool tech site]
```

"If the number of variables is lower than the words obtained, all the remaining words and their delimiters are crammed in the last variable. By default the read command splits the input into words, considering the \<space\>,\<tab\> and \<newline\> characters as word delimiters."

As for the git command, we can refer to the [documentation](https://git-scm.com/docs/git).

Although I can't fully understand it, according to:

```bash
if [ "${LACTF_CHALL_WRITERS["${name_email[0]}"]}" != "${name_email[1]}" ]
    then
      echo >&2 "error: not an LA CTF challenge writer"
      exit 1
    fi
if [ "${name_email[0]}" == "Benson Liu" ]
then
    HAS_BLIUTECH_COMMIT=true
fi
```

and:

```bash
if $HAS_BLIUTECH_COMMIT
then
  echo $FLAG
fi
```

The key logic of the script is that if we try to perform a push to the git remote repository as the "Benson Liu" user (email "bensonhliu@lac.tf"), we will get the flag.

The problem-solving script provided by the challenge developer is not long.

```bash
#/bin/bash

mkdir /tmp/new-challenge-solution
cd /tmp/new-challenge-solution
git clone "${1:-"git://lac.tf:31152/new-challenge.git"}" -q #
cd new-challenge

git -c user.name="Benson Liu" -c user.email="bensonhliu@lac.tf" -c commit.gpgsign=false commit -m "gimme flag" --allow-empty -q
git push --progress 2>&1 | sed "/^remote: lactf{/!d;s/^remote: //"

rm -r --interactive=never /tmp/new-challenge-solution
```

An example of [:-](https://unix.stackexchange.com/questions/286335/how-variables-inside-braces-are-evaluated) : "\${var:-val} is replaced by val if var is unset or null, \${var} otherwise (so val is a 'default value');". The \$ symbol in bash means to take a value. You can add or not add {}, and add it to increase readability and prevent ambiguity.

An example of -c in "git -c": "-c \<name\>=\<value\>: Pass a configuration parameter to the command. The value given will override values from configuration files. The \<name\> is expected in the same format as listed by git config (subkeys separated by dots)."

Run `git config --list` to view the key-value pairs.

[2>&1](https://stackoverflow.com/questions/818255/what-does-21-mean) means:

```
File descriptor 1 is the standard output (stdout).
File descriptor 2 is the standard error (stderr).

At first, 2>1 may look like a good way to redirect stderr to stdout. However, it will actually be interpreted as "redirect stderr to a file named 1".

& indicates that what follows and precedes is a file descriptor, and not a filename. Thus, we use 2>&1. Consider >& to be a redirect merger operator.
```

[SED](https://www.geeksforgeeks.org/sed-command-in-linux-unix-with-examples/) command in UNIX stands for stream editor and it can perform lots of functions on file like searching, find and replace, insertion or deletion. This is used to filter out the flag, and the flag can also be printed out without this command.

According to my experiment, the flag can also be obtained by simplifying the script as follows.

```bash
#/bin/bash

mkdir /tmp/new-challenge-solution
cd /tmp/new-challenge-solution
git clone "${1:-"git://lac.tf:31152/new-challenge.git"}"
cd new-challenge

git -c user.name="Benson Liu" -c user.email="bensonhliu@lac.tf" commit -m "gimme flag" --allow-empty -q
git push --progress
```

## Flag
> lactf{wh3n_th3_1mp0st3r_1s_5us}