touch $HOME/.rangerdir
alias 'r'='python3 $PWD/ranger/ranger.py'
alias 'ra'='python3 $PWD/ranger/ranger.py --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"'
