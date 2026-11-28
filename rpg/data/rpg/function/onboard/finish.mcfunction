execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
# 教学完成：回到出生的位置，武器交到主手
scoreboard players set @s rpg_ob 100
tag @s remove rpg.ob
tag @s remove rpg.ob.hold
tag @s remove rpg.ob.wait
execute if entity @s[tag=rpg.ob.intro] run function rpg:onboard/intro/stop
function rpg:onboard/music/stop
effect clear @s
gamemode survival @s
execute if score @s rpg_ob_gm matches 1 run gamemode creative @s
execute if score @s rpg_ob_gm matches 2 run gamemode adventure @s
scoreboard players set @s rpg_ob_v 1
# 教学装备：格子原来空着就留在身上（武器进主手）；原来有东西的，教学装备掉在脚边，原物还回格子。
# 在原地还（下一行去故乡会传送，落点的区块不一定已经载入）
execute at @s run function rpg:onboard/stash/take with storage rpg:onboard tmp
function rpg:town/home/start
function rpg:onboard/welcome with storage rpg:onboard tmp
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.8 1
