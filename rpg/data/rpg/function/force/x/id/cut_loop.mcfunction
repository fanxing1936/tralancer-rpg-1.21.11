execute unless data storage rpg:force r.l[0] run return 0
data modify storage rpg:force r.c set from storage rpg:force r.l[0]
data remove storage rpg:force r.l[0]
data modify storage rpg:force r.c.n set string storage rpg:force r.c.id 10
function rpg:force/x/id/cut_one
function rpg:force/x/id/cut_loop
