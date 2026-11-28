tellraw @a[tag=rpg.pr.join4] {"text":"[序章] 战场区块迟迟没有载入，已取消。Could not load the battlefield.","color":"red"}
execute as @a[tag=rpg.pr.join4] run scoreboard players reset @s rpg_pr_g
execute as @a[tag=rpg.pr.join4,tag=rpg.ob] run function rpg:onboard/pro/after
tag @a remove rpg.pr.join4
function rpg:prologue_i4/cleanup
