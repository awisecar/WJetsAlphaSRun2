==> received 9/28/18, 14:25


Hello Andrew,

I used the table you sent me, d03-x01-y01.tab.gz, also for some
tests of subprocess decomposition. I'm not sure which fastnlo toolkit
version you are exactly using, but if you use this one

http://ekpwww.etp.kit.edu/~rabbertz/fastNLO_LHC/fastnlo_toolkit-2.3.1pre-2550.tar.gz

for the evaluation you can use the attached python script in order
to make some nice plots, see the attachment.

The syntax for these plots is:


sp_contrib_flexible.py -t d03-x01-y01.tab.gz -o 0 -n 0 -s gq gaq q\!aq q=aq q\!q q=q gg
sp_contrib_flexible.py -t d03-x01-y01.tab.gz -o 1 -n 1 -s gq gaq q\!aq q=aq q\!q q=q gg
and
sp_contrib_flexible.py -t d03-x01-y01.tab.gz -o 0 -n 1 -s gq gaq q\!aq q=aq q\!q q=q gg

The white area in the third plot corresponds to the k factor.
Contributions below zero like from gg correspond to negative x section
corrections from interference terms involving loops first appearing at NLO.

sp_contrib_flexible.py -h
gives you some short explanation of the syntax.

Parton-parton subprocess categories can be grouped like all
qq, but also q=q meaning identical quark flavours and e.g. q!aq meaning
unequal quark-antiquark flavours. (The \! might be necessary for escaping the ! interpretation in some shells like tcsh.)

With your 121 tables you can also do uu or dg ...

Have fun,
Klaus



