execute as @e[tag=rpg.pr.foe,distance=0..] run function rpg:prologue_i2/cut/kill_actor
function rpg:prologue_i2/music/end
scoreboard players set #state rpg_pr_i2 8
scoreboard players set #t rpg_pr_i2 0
scoreboard players set #cut rpg_pr_i2 6
function rpg:prologue_i2/cut/begin
