execute as @e[tag=rpg.pr.foe,distance=0..] run function rpg:prologue_i4/cut/kill_actor
function rpg:prologue_i4/music/end
scoreboard players set #state rpg_pr_i4 8
scoreboard players set #t rpg_pr_i4 0
scoreboard players set #cut rpg_pr_i4 6
function rpg:prologue_i4/cut/begin
