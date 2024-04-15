touch -p $HOME/.rangerdir
alias 'r'='python3 $PWD/ranger.py'
alias 'ra'='python3 $PWD/ranger.py --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"
