execute as @e[tag=rpg.pr.foe,distance=0..] run function rpg:prologue_i1/cut/kill_actor
function rpg:prologue_i1/music/end
scoreboard players set #state rpg_pr_i1 8
scoreboard players set #t rpg_pr_i1 0
scoreboard players set #cut rpg_pr_i1 6
function rpg:prologue_i1/cut/begin
