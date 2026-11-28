execute as @e[tag=rpg.pr.foe,distance=0..] run function rpg:prologue_i3/cut/kill_actor
function rpg:prologue_i3/music/end
scoreboard players set #state rpg_pr_i3 8
scoreboard players set #t rpg_pr_i3 0
scoreboard players set #cut rpg_pr_i3 6
function rpg:prologue_i3/cut/begin
