execute as @e[tag=rpg.pr.foe] run function rpg:prologue/cut/kill_actor
function rpg:prologue/music/end
scoreboard players set #state rpg_pr 8
scoreboard players set #t rpg_pr 0
scoreboard players set #cut rpg_pr 6
function rpg:prologue/cut/begin
