function rpg:forge/wb/new
execute store result score #r rpg_fg run random value 0..7
execute store result storage rpg:forge nm.r int 1 run scoreboard players get #r rpg_fg
function rpg:forge/smelt/prefix with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 0 run function rpg:forge/smelt/m/sword_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 1 run function rpg:forge/smelt/m/axe_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 2 run function rpg:forge/smelt/m/mace_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 3 run function rpg:forge/smelt/m/bow_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 4 run function rpg:forge/smelt/m/crossbow_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 5 run function rpg:forge/smelt/m/head_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 6 run function rpg:forge/smelt/m/chest_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 7 run function rpg:forge/smelt/m/legs_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 8 run function rpg:forge/smelt/m/feet_plain with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 0 run function rpg:forge/smelt/m/sword_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 1 run function rpg:forge/smelt/m/axe_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 2 run function rpg:forge/smelt/m/mace_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 3 run function rpg:forge/smelt/m/bow_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 4 run function rpg:forge/smelt/m/crossbow_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 5 run function rpg:forge/smelt/m/head_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 6 run function rpg:forge/smelt/m/chest_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 7 run function rpg:forge/smelt/m/legs_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 8 run function rpg:forge/smelt/m/feet_brave with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 0 run function rpg:forge/smelt/m/sword_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 1 run function rpg:forge/smelt/m/axe_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 2 run function rpg:forge/smelt/m/mace_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 3 run function rpg:forge/smelt/m/bow_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 4 run function rpg:forge/smelt/m/crossbow_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 5 run function rpg:forge/smelt/m/head_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 6 run function rpg:forge/smelt/m/chest_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 7 run function rpg:forge/smelt/m/legs_epic with storage rpg:forge nm
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 8 run function rpg:forge/smelt/m/feet_epic with storage rpg:forge nm
scoreboard players operation #q0 rpg_fg = @s rpg_fg_mc
execute as @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] run function rpg:forge/init
summon minecraft:item ~ ~0.8 ~ {Item:{id:"minecraft:stone",count:1},Tags:["rpg.fg.out"],PickupDelay:10,Motion:[0.0,0.25,0.0]}
data modify entity @e[type=minecraft:item,tag=rpg.fg.out,limit=1,sort=nearest] Item set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item
tag @e[type=minecraft:item,tag=rpg.fg.out] remove rpg.fg.out
function rpg:forge/wb/close
particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.05 30
playsound minecraft:block.trial_spawner.eject_item block @a[distance=..16] ~ ~ ~ 1 0.8
scoreboard players operation #me rpg_fg = @s rpg_fg_eo
execute as @a if score @s rpg_fg_id = #me rpg_fg run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　成品出炉了","color":"#9C9A94","bold":false,"italic":false}]
kill @s
execute as @a if score @s rpg_fg_id = #me rpg_fg run function rpg:quest/hook/smelt
